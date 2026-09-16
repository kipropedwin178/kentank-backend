from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.init_db import init_db
from app.routes.auth import router as auth_router
from app.routes.tanks import router as tanks_router
from app.routes.tank_images import router as tank_images_router
from app.routes.contacts import router as contacts_router
from app.routes.public_contact import router as public_contact_router
from app.routes.dashboard import router as dashboard_router
from app.routes.public_tanks import router as public_tanks_router


app = FastAPI(
    title="Kentank Deliveries API",
    version="1.0.0",
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://your-frontend-domain.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# DATABASE STARTUP
# ==========================================

@app.on_event("startup")
def startup():
    init_db()


# ==========================================
# STATIC UPLOADS
# ==========================================

upload_directory = Path("uploads")
upload_directory.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(directory=upload_directory),
    name="uploads",
)


# ==========================================
# ROUTES
# ==========================================

app.include_router(auth_router)
app.include_router(tanks_router)
app.include_router(tank_images_router)
app.include_router(contacts_router)
app.include_router(public_contact_router)
app.include_router(public_tanks_router)
app.include_router(dashboard_router)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Welcome to Kentank Deliveries API"
    }