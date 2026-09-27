from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# Create FastAPI router
hospitals_bp = APIRouter(
    prefix="",
    tags=["Hospitals"]
)


# Templates
templates = Jinja2Templates(directory="templates")


# ==========================================
# Sample Hospital Database
# ==========================================

HOSPITALS_DATABASE = [

    {
        "id": "hosp_01",
        "name": "City Care Super Specialty Hospital",
        "address": "M.G. Road, Near Central Plaza, Mumbai",
        "contact": "+91 22 2890 1122",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "type": "General Hospital"
    },

    {
        "id": "hosp_02",
        "name": "Sunrise Multi-Specialty Clinic",
        "address": "Station Road, Opp. Metro Gate 2, Mumbai",
        "contact": "+91 22 2511 4455",
        "latitude": 19.0850,
        "longitude": 72.8900,
        "type": "Clinic"
    },

    {
        "id": "hosp_03",
        "name": "Apex Medical & Research Center",
        "address": "Highway Junction, Civil Lines, Mumbai",
        "contact": "+91 22 2772 9900",
        "latitude": 19.0500,
        "longitude": 72.8400,
        "type": "Specialty Center"
    }

]


# ==========================================
# Hospitals Page
# ==========================================

@hospitals_bp.get(
    "/hospitals",
    response_class=HTMLResponse
)
async def hospitals_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="hospitals.html",
        context={
            "request": request
        }
    )


# ==========================================
# Hospital Search API
# ==========================================

@hospitals_bp.get("/api/hospitals/search")
async def search_hospitals(
    q: str | None = Query(
        default=None,
        description="Hospital name, area, or city"
    ),
    lat: float | None = Query(
        default=None,
        description="User latitude"
    ),
    lng: float | None = Query(
        default=None,
        description="User longitude"
    )
):

    results = HOSPITALS_DATABASE.copy()


    # ------------------------------------------
    # Search by hospital name/address
    # ------------------------------------------

    if q:

        query_lower = q.lower().strip()

        results = [
            hospital
            for hospital in results
            if (
                query_lower in hospital["name"].lower()
                or query_lower in hospital["address"].lower()
                or query_lower in hospital["type"].lower()
            )
        ]


    return {
        "status": "success",
        "count": len(results),
        "data": results
    }