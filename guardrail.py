from state import AgentState
from config import EMERGENCY_KEYWORDS


def check_emergency(state: AgentState) -> AgentState:
    
    user_text = state.user_input.lower()
    
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in user_text:
            state.is_emergency = True
            
            state.final_response = (
                "🚨 **هشدار اورژانسی** 🚨\n\n"
                "علائم ذکر شده توسط شما ممکن است نشان‌دهنده یک وضعیت پزشکی اورژانسی باشد.\n"
                "لطفاً فوراً با اورژانس (۱۱۵) تماس بگیرید یا به نزدیک‌ترین مرکز درمانی مراجعه کنید.\n\n"
                "⚠️ این سیستم هوشمند قادر به مدیریت شرایط اورژانسی نیست."
            )
            
            state.supervisor_approved = True
            
            break
            
    return state