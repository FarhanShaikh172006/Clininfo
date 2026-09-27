"""
services/emergency_service.py
Handles SOS Emergencies, Ambulance Dispatching, Blood Bank Requests, and Realtime Statistics.
"""

import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class EmergencyService:

    # 9. Ambulance Request & 14. Emergency Request Management
    @staticmethod
    def create_emergency_sos(
        uid: str,
        patient_name: str,
        phone: str,
        latitude: float,
        longitude: float,
        emergency_type: str = "Medical General"
    ) -> Dict[str, Any]:
        """Creates a critical SOS alert broadcast payload with a unique alert ID."""
        timestamp = datetime.now(timezone.utc)
        alert_id = f"sos_{uid}_{int(timestamp.timestamp())}"
        
        try:
            lat = float(latitude)
            lng = float(longitude)
        except (ValueError, TypeError):
            lat, lng = 0.0, 0.0

        return {
            "alert_id": alert_id,
            "uid": uid,
            "patient_name": patient_name or "Unknown Patient",
            "phone": phone or "",
            "latitude": lat,
            "longitude": lng,
            "emergency_type": emergency_type,
            "status": "active",  # active | dispatched | resolved | cancelled
            "assigned_ambulance_id": None,
            "created_at": timestamp.isoformat(),
            "priority": "CRITICAL"
        }

    # 10. Ambulance Availability / Location Tracking
    @staticmethod
    def format_ambulance_unit(
        vehicle_number: str,
        driver_name: str,
        driver_phone: str,
        current_lat: float,
        current_lng: float,
        is_available: bool = True
    ) -> Dict[str, Any]:
        """Formats real-time ambulance tracking payload."""
        sanitized_vehicle = re.sub(r'[^a-zA-Z0-9]', '_', vehicle_number or "").lower().strip('_')
        ambulance_id = f"amb_{sanitized_vehicle}" if sanitized_vehicle else "amb_unknown"

        try:
            lat = float(current_lat)
            lng = float(current_lng)
        except (ValueError, TypeError):
            lat, lng = 0.0, 0.0

        return {
            "ambulance_id": ambulance_id,
            "vehicle_number": vehicle_number,
            "driver_name": driver_name or "Unassigned Driver",
            "driver_phone": driver_phone or "",
            "latitude": lat,
            "longitude": lng,
            "is_available": is_available,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    # 12. Blood Bank Information
    @staticmethod
    def format_blood_bank_stock(
        bank_id: str,
        bank_name: str,
        address: str,
        contact: str,
        units_available: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """Formats blood bank inventory records."""
        return {
            "bank_id": bank_id,
            "bank_name": bank_name,
            "address": address,
            "contact": contact,
            "inventory": units_available if isinstance(units_available, dict) else {},
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    # 6. Clinic Dashboard & 15. Basic Appointment & Emergency Statistics
    @staticmethod
    def calculate_clinic_metrics(
        appointments: Optional[List[Dict[str, Any]]] = None,
        emergencies: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Computes high-level clinical operational statistics for dashboard rendering.
        """
        safe_appointments = appointments if isinstance(appointments, list) else []
        safe_emergencies = emergencies if isinstance(emergencies, list) else []

        total_appointments = len(safe_appointments)
        scheduled_count = sum(1 for a in safe_appointments if isinstance(a, dict) and a.get("status") in ("scheduled", "pending"))
        completed_count = sum(1 for a in safe_appointments if isinstance(a, dict) and a.get("status") == "completed")
        cancelled_count = sum(1 for a in safe_appointments if isinstance(a, dict) and a.get("status") == "cancelled")

        total_emergencies = len(safe_emergencies)
        active_sos = sum(1 for e in safe_emergencies if isinstance(e, dict) and e.get("status") == "active")
        dispatched_sos = sum(1 for e in safe_emergencies if isinstance(e, dict) and e.get("status") == "dispatched")
        resolved_sos = sum(1 for e in safe_emergencies if isinstance(e, dict) and e.get("status") == "resolved")

        return {
            "appointments_summary": {
                "total": total_appointments,
                "scheduled": scheduled_count,
                "completed": completed_count,
                "cancelled": cancelled_count,
            },
            "emergencies_summary": {
                "total": total_emergencies,
                "active_sos": active_sos,
                "dispatched": dispatched_sos,
                "resolved": resolved_sos
            },
            "system_health": "OPTIMAL",
            "computed_at": datetime.now(timezone.utc).isoformat()
        }