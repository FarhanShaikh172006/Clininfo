"""
services/patient_service.py
Handles Patient Management, Appointments, Search, Reminders, and Clinical Directory.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class PatientService:

    # 1. Patient Registration
    @staticmethod
    def create_patient_profile(
        uid: str,
        name: str,
        email: str,
        phone: str,
        blood_group: str,
        age: int,
        gender: str,
        address: Optional[str] = None
    ) -> Dict[str, Any]:
        """Formats and validates patient registration profile payload."""
        return {
            "uid": uid,
            "full_name": name,
            "email": email,
            "phone": phone,
            "blood_group": blood_group.upper(),
            "age": age,
            "gender": gender,
            "address": address or "",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "active"
        }

    # 2. Appointment Booking & 3. Scheduling
    @staticmethod
    def create_appointment(
        patient_uid: str,
        patient_name: str,
        doctor_id: str,
        doctor_name: str,
        department: str,
        appointment_date: str,
        time_slot: str,
        reason: str
    ) -> Dict[str, Any]:
        """Creates a structured appointment booking entry."""
        appointment_id = f"apt_{patient_uid[:6]}_{int(datetime.now().timestamp())}"
        return {
            "appointment_id": appointment_id,
            "patient_uid": patient_uid,
            "patient_name": patient_name,
            "doctor_id": doctor_id,
            "doctor_name": doctor_name,
            "department": department,
            "appointment_date": appointment_date,
            "time_slot": time_slot,
            "reason": reason,
            "status": "scheduled",  # scheduled | confirmed | completed | cancelled
            "booked_at": datetime.now(timezone.utc).isoformat()
        }

    # 4. Appointment Status Update
    @staticmethod
    def update_appointment_status(appointment_id: str, new_status: str) -> Dict[str, Any]:
        """Validates and updates status transitions (scheduled -> confirmed/completed/cancelled)."""
        valid_statuses = {"scheduled", "confirmed", "completed", "cancelled"}
        if new_status.lower() not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        return {
            "appointment_id": appointment_id,
            "status": new_status.lower(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

    # 5. Follow-up Reminders
    @staticmethod
    def create_followup_reminder(
        patient_uid: str,
        doctor_name: str,
        reminder_date: str,
        notes: str
    ) -> Dict[str, Any]:
        """Generates a follow-up reminder notification payload."""
        return {
            "reminder_id": f"rem_{patient_uid[:6]}_{int(datetime.now().timestamp())}",
            "patient_uid": patient_uid,
            "doctor_name": doctor_name,
            "reminder_date": reminder_date,
            "notes": notes,
            "is_sent": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

    # 7. Basic Visit History
    @staticmethod
    def format_visit_record(
        patient_uid: str,
        doctor_name: str,
        diagnosis: str,
        prescription: List[str],
        follow_up_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Formats a clinical visit history record."""
        return {
            "visit_id": f"vst_{int(datetime.now().timestamp())}",
            "patient_uid": patient_uid,
            "doctor_name": doctor_name,
            "diagnosis": diagnosis,
            "prescription": prescription,
            "follow_up_date": follow_up_date,
            "visited_at": datetime.now(timezone.utc).isoformat()
        }

    # 8. Patient Search
    @staticmethod
    def build_patient_search_query(term: str) -> Dict[str, str]:
        """Normalizes patient search parameters for querying Firestore or RTDB."""
        cleaned_term = term.strip().lower()
        return {
            "search_term": cleaned_term,
            "is_phone": cleaned_term.isdigit() and len(cleaned_term) >= 10,
            "is_email": "@" in cleaned_term
        }

    # 11. Blood Group Search & Donors
    @staticmethod
    def filter_donors_by_blood_group(blood_group: str, donors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters blood donors based on required group and availability."""
        target_group = blood_group.strip().upper()
        return [
            d for d in donors 
            if d.get("blood_group") == target_group and d.get("is_available", True)
        ]

    # 13. Nearby Hospital / Clinic Information
    @staticmethod
    def format_facility_info(
        facility_id: str,
        name: str,
        facility_type: str,  # Hospital, Clinic, Urgent Care
        address: str,
        contact_number: str,
        latitude: float,
        longitude: float,
        services: List[str]
    ) -> Dict[str, Any]:
        """Formats clinic or hospital profile info."""
        return {
            "facility_id": facility_id,
            "name": name,
            "facility_type": facility_type,
            "address": address,
            "contact_number": contact_number,
            "latitude": latitude,
            "longitude": longitude,
            "services": services,
            "is_open_24x7": True
        }