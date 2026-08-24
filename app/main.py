from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

app = FastAPI(title="Wordistan Backend")

# Mobil (React Native / Expo) veya web isteklerinin CORS hatası almaması için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında her yerden gelen isteğe izin verir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


# Render ve tarayıcı testi için kök endpoint
@app.get("/")
def root():
    return {"message": "Wordistan API is running successfully!", "status": "ok"}