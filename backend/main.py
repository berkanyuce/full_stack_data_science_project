import fastapi as _fastapi
from fastapi import File, UploadFile
import fastapi.security as _security
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import services as _services
import schemas as _schemas
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from roboflow import Roboflow
import shutil
from fastapi.responses import JSONResponse
import statsmodels.api as sm

app = _fastapi.FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Power verisini oku
power = pd.read_csv('power_usage_2016_to_2020.csv')
n = power.shape[0]
p1 = pd.Series(range(n), pd.period_range('2016-06-01 00:00:00', freq='1H', periods=n))
power['DateTime'] = p1.to_frame().index
power = power.set_index('DateTime')
daily_power = power.resample('D').sum()
daily_power.index.name = 'Date'

# Weather verisini oku
weather = pd.read_csv('weather_2016_2020_daily.csv')
m = weather.shape[0]
p2 = pd.Series(range(m), pd.period_range('2016-06-01', freq='1D', periods=m))
weather['Date'] = p2.to_frame().index
weather = weather[:1498]
weather = weather.set_index('Date')

# Daily_power veri setindeki sütunları weather veri setine ekle
weather = weather.join(daily_power, how='left', lsuffix='_weather', rsuffix='_power')

weather['HDD'] = weather['Temp_avg'].apply(lambda Tm: max(65 - Tm, 0))
weather['CDD'] = weather['Temp_avg'].apply(lambda Tm: max(Tm - 65, 0))

# Independent features
X = weather[['Temp_max', 'Temp_avg', 'Temp_min', 'Dew_max', 'Dew_avg', 'Dew_min',
          'Hum_max', 'Hum_avg', 'Hum_min', 'Wind_max', 'Wind_avg', 'Wind_min',
          'Press_max', 'Press_avg', 'Press_min', 'Precipit', 'day_of_week_weather', 'HDD', 'CDD']]

# Dependent features. It calculates for HDD and CDD seperately
Y = weather[['Value (kWh)']]



# Function for backward elimination
def backward_elimination(Y, X):
    # Add constant term
    X = sm.add_constant(X)
    # Create the model
    model = sm.OLS(Y, X).fit()
    # Get p-values
    p_values = model.pvalues
    # Threshold value
    threshold = 0.05
    # Drop the feature if the largest p-value is greater than the threshold
    while p_values.max() > threshold:
        max_p_value_index = p_values.argmax()
        X = X.drop(X.columns[max_p_value_index], axis=1)
        model = sm.OLS(Y, X).fit()
        p_values = model.pvalues
    return model

# Build the model and check p-values (for HDD)
model = backward_elimination(Y, X)

# Get the values ​​predicted by the model
predicted_values = model.predict()

# Get actual values
actual_values = Y.values

@app.post("/api/analysis/image")
async def upload_image(image: UploadFile = File(...)):
    # Save the uploaded image to a temporary location
    temp_file_path = f"/tmp/{image.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Initialize Roboflow
    rf = Roboflow(api_key="IDb2X2qwfoHmjEljfIOb")
    project = rf.workspace().project("classificationbee-cat-dog-monkey-yn7fw")
    model = project.version(3).model

    # Run the model prediction
    prediction = model.predict(temp_file_path, confidence=40, overlap=30).json()

    # Extract the class information from the prediction
    if prediction['predictions']:
        predicted_class = prediction['predictions'][0]['class']
    else:
        predicted_class = "No prediction"

    # Return only the class
    return JSONResponse(content={"class": predicted_class})

# Correlation matrix endpoint
@app.get("/api/analysis/weather")
async def get_correlation():
    # Korelasyon matrisini hesapla
    correlation_matrix = weather.corr()
    
    # Grafik oluştur
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)
    plt.title("Korelasyon Matrisi")

    # Grafik verisini base64 formatına çevir
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    buffer.close()
    
    
# Regresyon grafiği oluştur
    plt.figure(figsize=(10, 6))
    plt.scatter(actual_values, predicted_values, color='blue', alpha=0.5)
    plt.plot(actual_values, actual_values, color='red', linestyle='--')
    plt.title('Gerçek vs. Tahmin Edilen Değerleri')
    plt.xlabel('Gerçek Değerleri')
    plt.ylabel('Tahmin Edilen Değerleri')
    plt.grid(True)

    # Regresyon grafiğini base64 formatına çevir
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    regression_img_str = base64.b64encode(buffer.read()).decode()
    buffer.close()

    # Base64 formatındaki veriyi döndür
    return {
        "correlation_image": img_str,
        "regression_image": regression_img_str,
        "predicted_values": predicted_values.tolist(),
        "actual_values": actual_values.tolist(),
        "remaining_features": model.model.exog_names
    }


@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.get("/api")
async def root():
    return {"message": "Full Stack Data Science Project"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
