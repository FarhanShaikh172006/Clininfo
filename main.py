import json

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.hospitals import hospitals_bp

# Services
from services.firebase_service import FirebaseService
from services.patient_service import PatientService
from services.emergency_service import EmergencyService


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="Clininfo Platform"
)


# ==========================================
# Static Files
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ==========================================
# Templates
# ==========================================

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# Firebase Configuration
# ==========================================

FIREBASE_CONFIG = FirebaseService.get_config()


def get_template_context(request: Request):

    return {
        "request": request,
        "firebase_config_json": json.dumps(FIREBASE_CONFIG)
    }


# ==========================================
# Register Hospital Router
# ==========================================

app.include_router(hospitals_bp)


# ==========================================
# Main Pages
# ==========================================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=get_template_context(request)
    )


@app.get("/login")
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=get_template_context(request)
    )


@app.get("/register")
async def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=get_template_context(request)
    )


@app.get("/dashboard")
async def dashboard_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=get_template_context(request)
    )


@app.get("/emergency")
async def emergency_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="emergency.html",
        context=get_template_context(request)
    )


@app.get("/admin")
async def admin_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context=get_template_context(request)
    )


@app.get("/blood-bank")
async def blood_bank_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="blood_bank.html",
        context=get_template_context(request)
    )