import uuid
from datetime import datetime
from typing import Dict, List, Optional
from database import get_db_connection, init_database


class PatientProfile:
    
    @staticmethod
    def create_patient(
        name: str,
        age: int,
        gender: str,
        weight: Optional[float] = None,
        height: Optional[float] = None,
        blood_type: Optional[str] = None,
        medical_history: Optional[str] = None,
        allergies: Optional[str] = None,
        medications: Optional[str] = None,
        lifestyle: Optional[str] = None
    ) -> str:
        """
        Create a new patient profile and return patient_id.
        
        Args:
            name: Patient's full name (required)
            age: Patient's age (required)
            gender: Patient's gender (required)
            weight: Weight in kg (optional)
            height: Height in cm (optional)
            blood_type: Blood type like A+, B-, etc. (optional)
            medical_history: Previous medical conditions (optional)
            allergies: Known allergies (optional)
            medications: Current medications (optional)
            lifestyle: Lifestyle information like smoking, exercise (optional)
            
        Returns:
            str: Unique patient_id for the created profile
        """
        init_database()
        
        patient_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO patients 
                (patient_id, name, age, gender, weight, height, blood_type, 
                 medical_history, allergies, medications, lifestyle, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id, name, age, gender, weight, height, blood_type,
                medical_history, allergies, medications, lifestyle, now, now
            ))
            conn.commit()
            conn.close()
            
            print(f"Patient created: {name} (ID: {patient_id})")
            return patient_id
            
        except Exception as e:
            print(f"Error creating patient: {e}")
            return None
    
    @staticmethod
    def get_patient(patient_id: str) -> Optional[Dict]:
   
        try:
            conn = get_db_connection()
            cursor = conn.execute(
                "SELECT * FROM patients WHERE patient_id = ?", 
                (patient_id,)
            )
            patient = cursor.fetchone()
            conn.close()
            
            if patient:
                return dict(patient)
            return None
            
        except Exception as e:
            print(f"Error retrieving patient: {e}")
            return None
    
    @staticmethod
    def update_patient(patient_id: str, **kwargs) -> bool:
     
        try:
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values()) + [datetime.now().isoformat(), patient_id]
            
            conn = get_db_connection()
            conn.execute(f"""
                UPDATE patients 
                SET {set_clause}, updated_at = ?
                WHERE patient_id = ?
            """, values)
            conn.commit()
            conn.close()
            
            print(f"Patient {patient_id} updated successfully")
            return True
            
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False
    
    @staticmethod
    def get_all_patients() -> List[Dict]:
     
        try:
            conn = get_db_connection()
            cursor = conn.execute(
                "SELECT patient_id, name, age, gender, created_at FROM patients ORDER BY created_at DESC"
            )
            patients = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return patients
            
        except Exception as e:
            print(f"Error retrieving patients: {e}")
            return []
    
    @staticmethod
    def delete_patient(patient_id: str) -> bool:

        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            conn.commit()
            conn.close()
            
            print(f"Patient {patient_id} deleted successfully")
            return True
            
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False