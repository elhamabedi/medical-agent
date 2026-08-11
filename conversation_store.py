import uuid
from datetime import datetime
from typing import Dict, List, Optional
from database import get_db_connection, init_database


class ConversationStore:
    
    @staticmethod
    def save_conversation(
        patient_id: str,
        user_message: str,
        assistant_response: str,
        is_emergency: bool = False,
        urgency_level: str = "non-emergency"
    ) -> Optional[str]:
    
        init_database()
        
        conversation_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO conversations 
                (conversation_id, patient_id, user_message, assistant_response, 
                 is_emergency, urgency_level, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                conversation_id, patient_id, user_message, assistant_response,
                int(is_emergency), urgency_level, now
            ))
            conn.commit()
            conn.close()
            
            print(f" Conversation saved: {conversation_id} for patient {patient_id}")
            return conversation_id
            
        except Exception as e:
            print(f" Error saving conversation: {e}")
            return None
    
    @staticmethod
    def get_patient_conversations(
        patient_id: str, 
        limit: int = 50
    ) -> List[Dict]:
    
        try:
            conn = get_db_connection()
            cursor = conn.execute("""
                SELECT * FROM conversations 
                WHERE patient_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (patient_id, limit))
            
            conversations = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return conversations
            
        except Exception as e:
            print(f"Error retrieving conversations: {e}")
            return []
    
    @staticmethod
    def get_conversation_stats(patient_id: str) -> Dict:
     
        try:
            conn = get_db_connection()
            
            cursor = conn.execute(
                "SELECT COUNT(*) as total FROM conversations WHERE patient_id = ?",
                (patient_id,)
            )
            total = cursor.fetchone()['total']
            
            cursor = conn.execute(
                "SELECT COUNT(*) as emergency_count FROM conversations WHERE patient_id = ? AND is_emergency = 1",
                (patient_id,)
            )
            emergency_count = cursor.fetchone()['emergency_count']
            
            cursor = conn.execute(
                "SELECT MAX(created_at) as last_conversation FROM conversations WHERE patient_id = ?",
                (patient_id,)
            )
            last_conversation = cursor.fetchone()['last_conversation']
            
            conn.close()
            
            return {
                "total_conversations": total,
                "emergency_conversations": emergency_count,
                "last_conversation": last_conversation
            }
            
        except Exception as e:
            print(f" Error getting stats: {e}")
            return {
                "total_conversations": 0,
                "emergency_conversations": 0,
                "last_conversation": None
            }
    
    @staticmethod
    def get_recent_emergencies(limit: int = 10) -> List[Dict]:
    
        try:
            conn = get_db_connection()
            cursor = conn.execute("""
                SELECT c.*, p.name as patient_name 
                FROM conversations c
                JOIN patients p ON c.patient_id = p.patient_id
                WHERE c.is_emergency = 1
                ORDER BY c.created_at DESC
                LIMIT ?
            """, (limit,))
            
            emergencies = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return emergencies
            
        except Exception as e:
            print(f"Error retrieving emergencies: {e}")
            return []