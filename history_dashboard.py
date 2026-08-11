import streamlit as st
import pandas as pd
from datetime import datetime
from conversation_store import ConversationStore
from patient_profile import PatientProfile


def render_history_dashboard():
    
    st.title("Conversation History Dashboard")
    st.markdown("View and analyze patient conversation history.")
    
    if 'current_patient_id' not in st.session_state or st.session_state.current_patient_id is None:
        st.warning("Please create or select a patient profile first from the 'Patient Profile' page.")
        st.info("Tip: Go to the 'Patient Profile' tab, create a patient, and then come back here.")
        return
    
    patient_id = st.session_state.current_patient_id
    patient_data = PatientProfile.get_patient(patient_id)
    
    if patient_data:
        st.subheader(f"Patient: {patient_data['name']} (ID: `{patient_id}`)")
    
    st.divider()

    
    st.subheader("📈 Overview Statistics")
    
    stats = ConversationStore.get_conversation_stats(patient_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Conversations", stats['total_conversations'])
    
    with col2:
        st.metric("Emergency Cases", stats['emergency_conversations'])
    
    with col3:
        if stats['last_conversation']:
        
            last_date = datetime.fromisoformat(stats['last_conversation']).strftime("%Y-%m-%d %H:%M")
            st.metric(" Last Conversation", last_date)
        else:
            st.metric("Last Conversation", "N/A")
    
    st.divider()
    
    st.subheader("Detailed Conversation History")
    
    conversations = ConversationStore.get_patient_conversations(patient_id, limit=50)
    
    if conversations:
        
        df = pd.DataFrame(conversations)
        
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime("%Y-%m-%d %H:%M:%S")
        df['is_emergency'] = df['is_emergency'].apply(lambda x: " Yes" if x else "No")
       
        display_df = df[[
            'created_at', 
            'user_message', 
            'assistant_response', 
            'is_emergency', 
            'urgency_level'
        ]].copy()
        
        display_df.columns = [
            'Time', 
            'User Message', 
            'Assistant Response', 
            'Emergency?', 
            ' Urgency Level'
        ]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download History as CSV",
            data=csv,
            file_name=f"patient_{patient_id}_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No conversations recorded yet for this patient. Start a chat to generate history.")
    
    st.divider()
    
    st.subheader("Recent Conversation Timeline")
    
    if conversations:
        
        for conv in reversed(conversations[:5]):  
            timestamp = datetime.fromisoformat(conv['created_at']).strftime("%Y-%m-%d %H:%M")
            emergency_icon = "🚨" if conv['is_emergency'] else "💬"
            
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**{timestamp}**")
                with col2:
                    st.markdown(f"{emergency_icon} **User:** {conv['user_message'][:100]}{'...' if len(conv['user_message']) > 100 else ''}")
                    st.markdown(f" **Assistant:** {conv['assistant_response'][:100]}{'...' if len(conv['assistant_response']) > 100 else ''}")
                st.divider()
    else:
        st.info("No conversations to display in the timeline.")