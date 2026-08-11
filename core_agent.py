import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv  
from state import AgentState
from config import SYSTEM_PROMPT, SYSTEM_PROMPT_RAG, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from medical_rag import generate_context_for_llm

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def generate_draft_response(state: AgentState) -> AgentState:
 
    if state.is_emergency:
        return state
    
    
    medical_context = generate_context_for_llm([state.user_input])
    
    if "Medical Guidelines" in medical_context:
        current_system_prompt = SYSTEM_PROMPT_RAG
    else:
        current_system_prompt = SYSTEM_PROMPT
    
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": current_system_prompt}
    ]
    
    if "Medical Guidelines" in medical_context:
        messages.append({
            "role": "system", 
            "content": f"[MEDICAL CONTEXT FROM KNOWLEDGE BASE]:\n{medical_context}"
        })
    
    messages.extend(state.conversation_history)
    
    messages.append({"role": "user", "content": state.user_input})
    
    try:
        if API_KEY != "sk-dummy-key-for-demo":
         
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            state.draft_response = response.choices[0].message.content
        else:
        
            state.draft_response = _generate_mock_response(state.user_input)
            
    except Exception as e:
        print("="*50)
        print(f"خطای دقیق API: {e}")
        print(f" API Key استفاده شده: {API_KEY[:15]}...")
        print(f" Base URL: {BASE_URL}")
        print(f" Model: {MODEL_NAME}")
        print("="*50)
        
        state.draft_response = (
            "متأسفانه در برقراری ارتباط با سرویس هوش مصنوعی خطایی رخ داد.\n"
            "لطفاً دوباره تلاش کنید یا با پزشک مشورت نمایید."
        )
    return state


def supervisor_validation(state: AgentState) -> AgentState:
  
    if state.is_emergency:
        return state
    
    disclaimer_keywords = [
        "جایگزین مراجعه به پزشک نیست",
        "مشورت با پزشک",
        "مراجعه به پزشک"
    ]
    
    has_disclaimer = any(keyword in state.draft_response for keyword in disclaimer_keywords)
    
    if has_disclaimer:
      
        state.supervisor_approved = True
        state.final_response = state.draft_response
    else:

        state.supervisor_approved = True
        state.final_response = (
            state.draft_response + 
            "\n\n **تذکر مهم:** این توصیه‌ها صرفاً جنبه اطلاع‌رسانی دارند و جایگزین مراجعه به پزشک نیستند."
        )
    
    return state


def _generate_mock_response(user_input: str) -> str:

    return (
        f"پاسخ به سوال شما: '{user_input}'\n\n"
        " **وضعیت کلی:** بر اساس اطلاعات ارائه شده و پایگاه دانش پزشکی، نیاز به بررسی بیشتر وجود دارد.\n\n"
        " **سطح اورژانسی:** غیراورژانسی (اما نیاز به پیگیری دارد)\n\n"
        " **اقدامات اولیه پیشنهادی:**\n"
        "- استراحت کافی\n"
        "- مصرف مایعات\n"
        "- پایش علائم\n\n"
        " **آزمایش‌های پیشنهادی:**\n"
        "- در صورت تداوم علائم: آزمایش خون کامل (CBC)\n\n"
        " **توصیه نهایی:** این توصیه‌ها جایگزین مراجعه به پزشک نیست. "
        "لطفاً برای بررسی دقیق‌تر به پزشک عمومی مراجعه کنید."
    )