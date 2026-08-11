import streamlit as st
from patient_profile import PatientProfile


def render_profile_page():
    
    st.title("Patient Profile Management")
    st.markdown("Create and manage patient profiles for better medical assistance.")
    
    st.divider()

    
    with st.expander("Create New Patient Profile", expanded=True):
        with st.form("new_patient_form", clear_on_submit=True):
            st.subheader("Personal Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *", placeholder="Enter patient name", help="Required field")
                age = st.number_input("Age *", min_value=0, max_value=120, step=1, help="Required field")
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"], help="Required field")
                blood_type = st.selectbox(
                    "Blood Type", 
                    ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
                )
            
            with col2:
                weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, step=0.1, format="%.1f")
                height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1, format="%.1f")
                lifestyle = st.text_area(
                    "Lifestyle", 
                    placeholder="Smoking, alcohol, exercise habits, diet...",
                    height=100
                )
            
            st.subheader("Medical Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                medical_history = st.text_area(
                    "Medical History", 
                    placeholder="Previous conditions, surgeries, chronic diseases...",
                    height=100
                )
                allergies = st.text_area(
                    "Allergies", 
                    placeholder="Drug allergies, food allergies, etc.",
                    height=80
                )
            
            with col2:
                medications = st.text_area(
                    "Current Medications", 
                    placeholder="List all current medications with dosages...",
                    height=100
                )
            
            st.divider()
            
            submitted = st.form_submit_button(" Create Patient Profile", use_container_width=True, type="primary")
            
            if submitted:
            
                if not name or not age or not gender:
                    st.error("Name, Age, and Gender are required fields.")
                else:
                    patient_id = PatientProfile.create_patient(
                        name=name,
                        age=int(age),
                        gender=gender,
                        weight=weight if weight > 0 else None,
                        height=height if height > 0 else None,
                        blood_type=blood_type if blood_type != "Unknown" else None,
                        medical_history=medical_history if medical_history else None,
                        allergies=allergies if allergies else None,
                        medications=medications if medications else None,
                        lifestyle=lifestyle if lifestyle else None
                    )
                    
                    if patient_id:
                        st.success(f"Patient profile created successfully!")
                        st.info(f"**Patient ID:** `{patient_id}` (Save this ID for future reference)")
                        
                        # Store in session state for immediate use
                        st.session_state.current_patient_id = patient_id
                        st.session_state.current_patient_name = name
                    else:
                        st.error("Failed to create patient profile. Please try again.")
    
    st.divider()

    
    st.subheader("Existing Patient Profiles")
    
    patients = PatientProfile.get_all_patients()
    
    if patients:
        patient_options = {f"{p['name']} (ID: {p['patient_id']})": p['patient_id'] for p in patients}
        selected_patient_label = st.selectbox(
            "Select Patient", 
            list(patient_options.keys()),
            help="Choose a patient to view their profile"
        )
        
        if selected_patient_label:
            patient_id = patient_options[selected_patient_label]
            patient_data = PatientProfile.get_patient(patient_id)
            
            if patient_data:
                st.session_state.current_patient_id = patient_id
                st.session_state.current_patient_name = patient_data['name']
                
                st.success(f"Active Patient: **{patient_data['name']}** (ID: `{patient_id}`)")
                
                st.divider()
                
                st.subheader("Patient Overview")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Name", patient_data['name'])
                with col2:
                    st.metric("Age", f"{patient_data['age']} years")
                with col3:
                    st.metric("Gender", patient_data['gender'])
                with col4:
                    st.metric("Blood Type", patient_data['blood_type'] or "Unknown")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(" Physical Information")
                    
                    if patient_data['weight']:
                        st.write(f"**Weight:** {patient_data['weight']} kg")
                    
                    if patient_data['height']:
                        st.write(f"**Height:** {patient_data['height']} cm")
                        
                        if patient_data['weight'] and patient_data['height']:
                            bmi = patient_data['weight'] / ((patient_data['height']/100) ** 2)
                            st.write(f"**BMI:** {bmi:.1f}")
                            
                            if bmi < 18.5:
                                st.caption(" Underweight")
                            elif bmi < 25:
                                st.caption(" Normal weight")
                            elif bmi < 30:
                                st.caption(" Overweight")
                            else:
                                st.caption(" Obese")
                    
                    if patient_data['blood_type']:
                        st.write(f"**Blood Type:** {patient_data['blood_type']}")
                
                with col2:
                    st.subheader(" Medical Information")
                    
                    if patient_data['medical_history']:
                        st.warning(f"**Medical History:** {patient_data['medical_history']}")
                    
                    if patient_data['allergies']:
                        st.error(f"**Allergies:** {patient_data['allergies']}")
                    
                    if patient_data['medications']:
                        st.info(f"**Current Medications:** {patient_data['medications']}")
                
                if patient_data['lifestyle']:
                    st.divider()
                    st.subheader("Lifestyle")
                    st.write(patient_data['lifestyle'])
                
                st.divider()
                
                st.caption(f"**Created:** {patient_data['created_at']}")
                st.caption(f"**Last Updated:** {patient_data['updated_at']}")
                
                if st.button("Edit Profile", use_container_width=True):
                    st.info("Edit functionality will be available in Phase 3.")
    
    else:
        st.info(" No patient profiles created yet. Create your first patient using the form above.")