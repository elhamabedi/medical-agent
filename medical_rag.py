from typing import Dict, List


MEDICAL_KNOWLEDGE = {
    "سردرد": {
        "causes": ["استرس", "کم‌آبی بدن", "خستگی", "میگرن", "فشار خون بالا", "مشکلات بینایی"],
        "recommendations": [
            "استراحت در اتاق تاریک و ساکت",
            "مصرف مایعات فراوان",
            "استفاده از مسکن‌های ساده مثل استامینوفن",
            "کمپرس سرد روی پیشانی"
        ],
        "red_flags": [
            "سردرد ناگهانی و بسیار شدید (مثل صاعقه)",
            "همراه با تب بالا و سفتی گردن",
            "همراه با ضعف یا بی‌حسی در یک طرف بدن",
            "همراه با اختلال در بینایی یا گفتار"
        ],
        "tests": ["CBC (آزمایش خون کامل)", "CT Scan (در صورت نیاز)", "MRI (در موارد خاص)"],
        "specialist": "مغز و اعصاب (Neurologist)"
    },
    
    "تب": {
        "causes": ["عفونت ویروسی (مثل سرماخوردگی)", "عفونت باکتریایی", "التهاب", "واکسیناسیون اخیر"],
        "recommendations": [
            "استراحت کافی",
            "مصرف مایعات فراوان (آب، آبمیوه طبیعی)",
            "پاشویه با آب ولرم",
            "استفاده از استامینوفن یا ایبوپروفن (با مشورت پزشک)"
        ],
        "red_flags": [
            "تب بالای ۳۹ درجه سانتیگراد",
            "تب همراه با تشنج",
            "تب بیش از ۳ روز بدون بهبود",
            "همراه با بثورات پوستی (راش)"
        ],
        "tests": ["CBC", "CRP (پروتئین واکنش‌گر C)", "کشت خون (در صورت نیاز)", "تست‌های ویروسی"],
        "specialist": "داخلی (Internal Medicine) یا عفونی (Infectious Disease)"
    },
    
    "درد قفسه سینه": {
        "causes": ["مشکلات قلبی (آنژین، سکته قلبی)", "مشکلات ریوی (آمبولی)", "مشکلات گوارشی (رفلاکس)", "استرس و اضطراب"],
        "recommendations": [
            " مراجعه فوری به اورژانس",
            "استراحت مطلق",
            "عدم انجام فعالیت بدنی",
            "جویدن آسپرین (فقط با دستور اورژانس)"
        ],
        "red_flags": [
            "درد فشارنده یا سنگین",
            "انتشار درد به دست چپ، فک یا پشت",
            "همراه با تنگی نفس شدید",
            "همراه با عرق سرد و تهوع"
        ],
        "tests": ["ECG (نوار قلب)", "Troponin (آنزیم قلبی)", "Chest X-ray", "Echocardiography", "Angiography"],
        "specialist": "قلب و عروق (Cardiologist)",
        "emergency": True
    },
    
    "سرفه": {
        "causes": ["عفونت تنفسی (سرماخوردگی، برونشیت)", "آلرژی", "آسم", "رفلاکس معده", "سیگار"],
        "recommendations": [
            "مصرف مایعات گرم (چای، سوپ)",
            "استفاده از دستگاه بخور",
            "عسل و لیمو (برای بزرگسالان)",
            "استراحت و پرهیز از محرک‌ها"
        ],
        "red_flags": [
            "سرفه خونی",
            "همراه با تنگی نفس شدید",
            "سرفه بیش از ۳ هفته",
            "همراه با کاهش وزن ناگهانی"
        ],
        "tests": ["Chest X-ray", "Spirometry (تست عملکرد ریه)", "CBC", "تست آلرژی"],
        "specialist": "ریه (Pulmonologist)"
    },
    
    "دیابت": {
        "management": [
            "کنترل منظم قند خون",
            "رژیم غذایی کم‌کربوهیدرات",
            "ورزش منظم (حداقل ۳ دقیقه در روز)",
            "مصرف منظم داروهای تجویزشده"
        ],
        "monitoring": [
            "HbA1c هر ۳ ماه",
            "قند خون ناشتا روزانه",
            "بررسی کلیه (کراتینین) سالانه",
            "معاینه چشم (رتینوپاتی) سالانه"
        ],
        "complications": ["رتینوپاتی (آسیب چشم)", "نفروپاتی (آسیب کلیه)", "نوروپاتی (آسیب عصبی)", "بیماری قلبی-عروقی"],
        "specialist": "غدد (Endocrinologist)"
    },
    
    "فشار خون": {
        "management": [
            "کاهش مصرف نمک",
            "ورزش منظم",
            "کاهش استرس",
            "مصرف منظم داروهای ضد فشار خون"
        ],
        "monitoring": [
            "اندازه‌گیری فشار خون روزانه",
            "آزمایش کلیه و الکترولیت‌ها هر ۶ ماه",
            "ECG سالانه"
        ],
        "red_flags": [
            "فشار خون بالای ۱۸۰/۱۲۰ (بحران فشار خون)",
            "همراه با سردرد شدید",
            "همراه با تاری دید",
            "همراه با درد قفسه سینه"
        ],
        "tests": ["فشار خون ۲۴ ساعته (Holter)", "آزمایش کلیه", "ECG", "Echocardiography"],
        "specialist": "قلب و عروق (Cardiologist)"
    },
    
    "کمردرد": {
        "causes": ["آسیب عضلانی", "دیسک کمر", "آرتروز", "پوکی استخوان", "وضعیت بد نشستن"],
        "recommendations": [
            "استراحت نسبی (نه مطلق)",
            "کمپرس گرم یا سرد",
            "ورزش‌های کششی ملایم",
            "استفاده از مسکن‌های ضدالتهابی"
        ],
        "red_flags": [
            "همراه با بی‌حسی یا ضعف در پاها",
            "همراه با اختلال در کنترل ادرار یا مدفوع",
            "درد شدید و ناگهانی بعد از ضربه",
            "همراه با تب"
        ],
        "tests": ["X-ray کمر", "MRI (در صورت نیاز)", "آزمایش تراکم استخوان (DEXA)"],
        "specialist": "ارتوپد (Orthopedist) یا مغز و اعصاب (Neurologist)"
    },
    
    "تهوع و استفراغ": {
        "causes": ["مسمومیت غذایی", "ویروس گوارشی", "بارداری", "میگرن", "عوارض دارویی"],
        "recommendations": [
            "مصرف مایعات به مقدار کم ولی مکرر",
            "پرهیز از غذاهای چرب و سنگین",
            "استراحت در وضعیت نیمه‌نشسته",
            "استفاده از زنجبیل (برای تهوع خفیف)"
        ],
        "red_flags": [
            "استفراغ خونی یا به رنگ قهوه‌ای تیره",
            "همراه با درد شدید شکم",
            "عدم توانایی در نگه داشتن مایعات بیش از ۲۴ ساعت",
            "علائم کم‌آبی شدید (خشکی دهان، کاهش ادرار)"
        ],
        "tests": ["CBC", "الکترولیت‌ها", "آنزیم‌های کبدی", "سونوگرافی شکم (در صورت نیاز)"],
        "specialist": "داخلی (Internal Medicine) یا گوارش (Gastroenterologist)"
    }
}


def retrieve_medical_info(symptoms: List[str]) -> Dict:

    relevant_info = {}
    
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        
        for keyword, info in MEDICAL_KNOWLEDGE.items():
            if keyword in symptom_lower or symptom_lower in keyword:
                relevant_info[keyword] = info
    
    return relevant_info


def generate_context_for_llm(symptoms: List[str]) -> str:
 
    info = retrieve_medical_info(symptoms)
    
    if not info:
        return "No specific medical guidelines found for these symptoms. Use general medical knowledge."
    
    context = "## Medical Guidelines from Knowledge Base:\n\n"
    
    for symptom, details in info.items():
        context += f"### {symptom}:\n"
        
        if "causes" in details:
            context += f"- علل احتمالی: {', '.join(details['causes'])}\n"
        
        if "recommendations" in details:
            context += f"- توصیه‌ها: {', '.join(details['recommendations'])}\n"
        
        if "red_flags" in details:
            context += f"- ⚠️ علائم خطر: {', '.join(details['red_flags'])}\n"
        
        if "tests" in details:
            context += f"- آزمایش‌های پیشنهادی: {', '.join(details['tests'])}\n"
        
        if "specialist" in details:
            context += f"- متخصص مرتبط: {details['specialist']}\n"
        
        if details.get("emergency"):
            context += "- **این وضعیت ممکن است اورژانسی باشد!**\n"
        
        context += "\n"
    
    return context


def get_all_medical_topics() -> List[str]:

    return list(MEDICAL_KNOWLEDGE.keys())