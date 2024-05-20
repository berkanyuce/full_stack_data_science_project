import fastapi as _fastapi
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

# Veriyi yükle
data = pd.read_csv('/Users/berkanyuce/Desktop/Workintech/Kişisel Projeler/interview1/ML/weather_2016_2020_daily.csv')
data['HDD'] = data['Temp_avg'].apply(lambda Tm: max(65 - Tm, 0))
data['CDD'] = data['Temp_avg'].apply(lambda Tm: max(Tm - 65, 0))


# Korelasyon matrisi endpoint'i
@app.get("/api/analysis/weather")
async def get_correlation():
    # Korelasyon matrisini hesapla
    correlation_matrix = data.corr()
    
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

    # Base64 formatındaki veriyi döndür
    return {"image": img_str}


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
