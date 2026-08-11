import streamlit as st
from state import AgentState
from guardrail import check_emergency
from core_agent import generate_draft_response, supervisor_validation
from conversation_store import ConversationStore

from profile_page import render_profile_page
from history_dashboard import render_history_dashboard


st.set_page_config(
    page_title="Medical Assistant Agent - Phase 2",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


page = st.sidebar.radio(
    "Navigation",
    ["Chat Assistant", " Patient Profile", "History Dashboard"]
)


if page == "Chat Assistant":
    st.title("AI Medical Assistant Agent")
    st.caption("Phase 2 | Intelligent Medical Assistant with Patient Management")
    
    if 'current_patient_id' not in st.session_state or st.session_state.current_patient_id is None:
        st.warning("Please create or select a patient profile first from the 'Patient Profile' page.")
    else:
        st.success(f"Active Patient: **{st.session_state.get('current_patient_name', 'Unknown')}** (ID: `{st.session_state.current_patient_id}`)")
    
    st.divider()
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if "last_state" not in st.session_state:
        st.session_state.last_state = AgentState()
    
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Describe your symptoms or ask a medical question..."):
        
        if 'current_patient_id' not in st.session_state or st.session_state.current_patient_id is None:
            st.error("Please select a patient profile first!")
        else:
            st.session_state.history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            current_state = AgentState(
                patient_id=st.session_state.current_patient_id, # Phase 2: Link to patient
                user_input=prompt,
                conversation_history=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.history[:-1]
                ]
            )
            
            with st.chat_message("assistant"):
                with st.spinner("🔍 Analyzing symptoms and checking medical guidelines..."):
                    
                    current_state = check_emergency(current_state)
                    
                    if not current_state.is_emergency:
                        current_state = generate_draft_response(current_state)
                    
                    current_state = supervisor_validation(current_state)
                    
                    st.markdown(current_state.final_response)
                    
                    st.session_state.history.append({
                        "role": "assistant", 
                        "content": current_state.final_response
                    })
                    
                    ConversationStore.save_conversation(
                        patient_id=st.session_state.current_patient_id,
                        user_message=prompt,
                        assistant_response=current_state.final_response,
                        is_emergency=current_state.is_emergency,
                        urgency_level="emergency" if current_state.is_emergency else "non-emergency"
                    )
            
            st.session_state.last_state = current_state
    
    with st.sidebar:
        st.divider()
        st.header("Controls")
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        
        st.divider()
        st.header("System Status (Debug)")
        last = st.session_state.last_state
        if last.is_emergency:
            st.error("Emergency Mode: ACTIVE")
        else:
            st.success("Emergency Mode: Inactive")
        
        if last.supervisor_approved:
            st.success("Supervisor: Approved")
        else:
            st.warning("Supervisor: Pending")

elif page == " Patient Profile":
    render_profile_page()

elif page == "History Dashboard":
    render_history_dashboard()