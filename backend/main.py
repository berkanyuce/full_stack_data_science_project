import fastapi as _fastapi
from fastapi import File, UploadFile
import fastapi.security as _security
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware
import services as _services
import schemas as _schemas
from roboflow import Roboflow
import shutil
from fastapi.responses import JSONResponse
import pickle
import json

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

# Verileri pickle dosyasından yükle
with open('processed_data.pkl', 'rb') as f:
    weather = pickle.load(f)

# Independent features
X = weather[['Temp_max', 'Temp_avg', 'Temp_min', 'Dew_max', 'Dew_avg', 'Dew_min',
             'Hum_max', 'Hum_avg', 'Hum_min', 'Wind_max', 'Wind_avg', 'Wind_min',
             'Press_max', 'Press_avg', 'Press_min', 'Precipit', 'day_of_week_weather', 'HDD', 'CDD']]

# Dependent features
Y = weather[['Value (kWh)']]

# Load model from pickle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


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
    
    # Get the values predicted by the model
    predicted_values = model.predict()

    # Get actual values
    actual_values = Y.values
    actual_values = actual_values.reshape(1498,)

    # Korelasyon matrisini hesapla
    correlation_matrix = weather.corr()

    # Convert correlation matrix to JSON
    correlation_json = correlation_matrix.to_json()

    # Prepare data for regression plot
    regression_data = {
        "actual_values": actual_values.tolist(),
        "predicted_values": predicted_values.tolist()
    }

    # Convert regression data to JSON
    regression_json = json.dumps(regression_data)

    return {
        "correlation_matrix": correlation_json,
        "regression_plot_data": regression_json,
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