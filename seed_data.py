from patient_profile import PatientProfile
from conversation_store import ConversationStore
from database import init_database


def seed_sample_patients():
    
    print("Seeding sample patients...")
    
    patient1_id = PatientProfile.create_patient(
        name="علی رضایی",
        age=45,
        gender="Male",
        weight=82.5,
        height=175,
        blood_type="A+",
        medical_history="دیابت نوع  (تشخیص ۵ سال پیش)، فشار خون خفیف",
        allergies="پنی‌سیلین",
        medications="متفورمین ۵۰۰mg (روزانه دو بار)، لوزارتان ۵۰mg",
        lifestyle="سیگاری (۱۰ نخ در روز)، ورزش منظم ندارد، رژیم غذایی نامنظم"
    )
    print(f" Created: {patient1_id} - علی رضایی")
    
    patient2_id = PatientProfile.create_patient(
        name="مریم احمدی",
        age=28,
        gender="Female",
        weight=62,
        height=165,
        blood_type="O+",
        medical_history="آسم (از کودکی)، آلرژی فصلی",
        allergies="گرد و غبار، گرده گیاهان",
        medications="اسپری سالبوتامول (هنگام نیاز)، اسپری فلوتیکازون (روزانه)",
        lifestyle="ورزشکار (یوگا ۳ بار در هفته)، غیرسیگاری، رژیم گیاهخواری"
    )
    print(f" Created: {patient2_id} - مریم احمدی")
    
    patient3_id = PatientProfile.create_patient(
        name="حسن کریمی",
        age=67,
        gender="Male",
        weight=78,
        height=170,
        blood_type="B+",
        medical_history="بypass قلب (۳ سال پیش)، کلسترول بالا، آرتروز زانو",
        allergies="ندارد",
        medications="آسپرین ۸۱mg، آتورواستاتین ۲۰mg، متوپرولول ۵۰mg",
        lifestyle="بازنشسته، پیاده‌روی روزانه ۳۰ دقیقه، رژیم کم‌نمک"
    )
    print(f" Created: {patient3_id} - حسن کریمی")
    
    return [patient1_id, patient2_id, patient3_id]


def seed_sample_conversations(patient_ids):
    """Create sample conversations for demo."""
    
    print("\n Seeding sample conversations...")
    
    if len(patient_ids) >= 1:
    
        ConversationStore.save_conversation(
            patient_id=patient_ids[0],
            user_message="سردرد و سرگیجه دارم، قند خونم هم بالاست",
            assistant_response="با توجه به سابقه دیابت شما، این علائم می‌تواند نشان‌دهنده نوسان قند خون باشد. توصیه می‌شود: ۱) قند خون را اندازه بگیرید ۲) مایعات بنوشید ۳) اگر قند بالای ۳۰۰ است، با پزشک تماس بگیرید. این توصیه‌ها جایگزین مراجعه به پزشک نیست.",
            is_emergency=False,
            urgency_level="non-emergency"
        )
        print(f" Saved conversation for patient {patient_ids[0]}")
        
        ConversationStore.save_conversation(
            patient_id=patient_ids[0],
            user_message="درد قفسه سینه دارم و نفس کم میارم",
            assistant_response="هشدار اورژانسی: با توجه به علائم شما و سابقه قلبی، لطفاً فوراً با اورژانس (۱۱۵) تماس بگیرید. این سیستم قادر به مدیریت شرایط اورژانسی نیست.",
            is_emergency=True,
            urgency_level="emergency"
        )
        print(f" Saved emergency conversation for patient {patient_ids[0]}")
    
    if len(patient_ids) >= 2:
      
        ConversationStore.save_conversation(
            patient_id=patient_ids[1],
            user_message="سرفه و تنگی نفس دارم، فکر می‌کنم آلرژی فصلی شروع شده",
            assistant_response="با توجه به سابقه آسم و آلرژی شما، این علائم می‌تواند ناشی از حساسیت فصلی باشد. توصیه: ۱) از اسپری سالبوتامول استفاده کنید ۲) آنتی‌هیستامین مصرف کنید ۳) از محرک‌ها دوری کنید. اگر تنگی نفس شدید شد، به اورژانس مراجعه کنید. این توصیه‌ها جایگزین مراجعه به پزشک نیست.",
            is_emergency=False,
            urgency_level="non-emergency"
        )
        print(f"   Saved conversation for patient {patient_ids[1]}")
    
    if len(patient_ids) >= 3:
    
        ConversationStore.save_conversation(
            patient_id=patient_ids[2],
            user_message="زانویم درد می‌کند و کمی تورم دارد",
            assistant_response="با توجه به سابقه آرتروز شما، این درد احتمالاً ناشی از التهاب مفصل است. توصیه: ۱) استراحت نسبی ۲) کمپرس سرد ۳) مسکن ضدالتهابی (با مشورت پزشک). اگر درد شدید یا ناگهانی است، به ارتوپد مراجعه کنید. این توصیه‌ها جایگزین مراجعه به پزشک نیست.",
            is_emergency=False,
            urgency_level="non-emergency"
        )
        print(f" Saved conversation for patient {patient_ids[2]}")


def main():
    
    print("=" * 60)
    print("Medical Assistant Agent - Database Seeding Script")
    print("=" * 60)
    print()
    
    init_database()
    
    patient_ids = seed_sample_patients()
    
    seed_sample_conversations(patient_ids)
    
    print()
    print("=" * 60)
    print("Seeding completed successfully!")
    print(f"Total patients created: {len(patient_ids)}")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Run: streamlit run app.py")
    print("  2. Go to 'Patient Profile' page to see the sample patients")
    print("  3. Select a patient and start chatting")
    print("  4. Check 'History Dashboard' to see conversation history")


if __name__ == "__main__":
    main()