"""
Yoshlar Innovatsiya Markazi — Database Seed Script
Barcha jadvallarni chiroyli namuna ma'lumotlar bilan to'ldiradi.
"""
import os
import sys
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from accounts.models import User
from dashboard.models import (
    Laboratory, Program, Event, Project,
    Partner, News, SiteSetting
)


def seed():
    print("=" * 60)
    print("  YIM Database Seed — boshlandi...")
    print("=" * 60)

    # ──────────────────────────────────
    # SITE SETTINGS
    # ──────────────────────────────────
    print("\n[1/8] Sayt sozlamalari...")
    site = SiteSetting.get_settings()
    site.site_name = "Yoshlar innovatsiya markazi"
    site.slogan = "Kelajak texnologiyalari — yoshlar qo'lida"
    site.about_text = (
        "Yoshlar innovatsiya markazi — bu zamonaviy texnologiyalar, robototexnika, sun'iy intellekt, "
        "dasturlash va boshqa innovatsion yo'nalishlar bo'yicha yoshlarni o'qitish hamda ularning "
        "g'oyalarini amalga oshirishga ko'maklashuvchi markaz. Bizning maqsadimiz — har bir yosh "
        "avlod vakilining texnologik salohiyatini ro'yobga chiqarish va ularni kelajak kasblariga "
        "tayyorlash. Markaz 2023-yilda tashkil etilgan bo'lib, qisqa vaqt ichida mamlakatdagi "
        "eng ilg'or ta'lim muassasalaridan biriga aylandi."
    )
    site.phone = "+998 (71) 200-30-40"
    site.email = "info@yim.uz"
    site.address = "Toshkent shahri, Mirzo Ulug'bek tumani, Innovatsiya ko'chasi, 15-uy"
    site.telegram_link = "https://t.me/yim_uz"
    site.instagram_link = "https://instagram.com/yim_uz"
    site.youtube_link = "https://youtube.com/@yim_uz"
    site.working_hours = "Dushanba – Shanba: 09:00 – 18:00"
    site.map_embed = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2996.0234567890!2d69.2790!3d41.3111!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDHCsDE4JzQwLjAiTiA2OcKwMTYnNDQuNCJF!5e0!3m2!1suz!2s!4v1700000000000!5m2!1suz!2s" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
    site.save()
    print("   ✓ Sayt sozlamalari yangilandi")

    # ──────────────────────────────────
    # USERS (students)
    # ──────────────────────────────────
    print("\n[2/8] Foydalanuvchilar...")
    students_data = [
        {"username": "jasur_k", "first_name": "Jasur", "last_name": "Karimov", "email": "jasur@yim.uz"},
        {"username": "malika_r", "first_name": "Malika", "last_name": "Rahimova", "email": "malika@yim.uz"},
        {"username": "sardor_a", "first_name": "Sardor", "last_name": "Alimov", "email": "sardor@yim.uz"},
        {"username": "dildora_n", "first_name": "Dildora", "last_name": "Nazarova", "email": "dildora@yim.uz"},
        {"username": "bobur_t", "first_name": "Bobur", "last_name": "Toshmatov", "email": "bobur@yim.uz"},
        {"username": "nodira_s", "first_name": "Nodira", "last_name": "Sultonova", "email": "nodira@yim.uz"},
        {"username": "otabek_m", "first_name": "Otabek", "last_name": "Mirzayev", "email": "otabek@yim.uz"},
        {"username": "zilola_u", "first_name": "Zilola", "last_name": "Usmonova", "email": "zilola@yim.uz"},
    ]
    students = []
    for sd in students_data:
        user, created = User.objects.get_or_create(
            username=sd["username"],
            defaults={
                "first_name": sd["first_name"],
                "last_name": sd["last_name"],
                "email": sd["email"],
                "role": "student",
            }
        )
        if created:
            user.set_password("student123")
            user.save()
        students.append(user)
    print(f"   ✓ {len(students)} ta talaba yaratildi")

    # ──────────────────────────────────
    # LABORATORIES
    # ──────────────────────────────────
    print("\n[3/8] Laboratoriyalar...")
    labs_data = [
        {
            "name": "Robototexnika laboratoriyasi",
            "icon": "robot",
            "description": "Arduino, Raspberry Pi, dronlar va sanoat robotlari bilan ishlash laboratoriyasi. Bu yerda talabalar mexatronika, elektronika va avtomatlashtirish asoslarini amaliy o'rganadilar. Laboratoriya eng zamonaviy 3D printerlar, CNC stanoklar va lazer kesish uskunalari bilan jihozlangan.",
            "order": 1,
        },
        {
            "name": "Sun'iy intellekt laboratoriyasi",
            "icon": "gpu-card",
            "description": "Machine Learning, Deep Learning, Computer Vision va NLP yo'nalishlari bo'yicha tadqiqot va amaliy loyihalar uchun yuqori quvvatli GPU serverlar bilan jihozlangan laboratoriya. TensorFlow, PyTorch va NVIDIA CUDA texnologiyalaridan foydalaniladi.",
            "order": 2,
        },
        {
            "name": "Dasturlash laboratoriyasi",
            "icon": "code-slash",
            "description": "Full-Stack veb dasturlash, mobil ilovalar va tizimli dasturlash uchun zamonaviy ish stantsiyalari bilan jihozlangan laboratoriya. Python, JavaScript, C++, Java va Kotlin tillarida amaliy mashg'ulotlar o'tkaziladi.",
            "order": 3,
        },
        {
            "name": "IoT va elektronika laboratoriyasi",
            "icon": "cpu",
            "description": "Internet of Things (IoT) qurilmalari, sensorlar, mikrokontrollerlar va aqlli uy tizimlari ustida ishlash uchun maxsus laboratoriya. ESP32, STM32 va turli sensor modullari bilan amaliy loyihalar yaratiladi.",
            "order": 4,
        },
        {
            "name": "Kiberxavfsizlik laboratoriyasi",
            "icon": "shield-check",
            "description": "Tarmoq xavfsizligi, penetration testing, kriptografiya va axborot himoyasi bo'yicha amaliy mashg'ulotlar uchun mo'ljallangan laboratoriya. Ethical hacking va SOC monitoring tizimlari o'rgatiladi.",
            "order": 5,
        },
        {
            "name": "3D modellash va prototiplash",
            "icon": "box",
            "description": "CAD dasturlari (SolidWorks, Fusion 360), 3D printerlar, lazer gravirka va CNC frezer uskunalari yordamida loyihalar prototiplarini yaratish laboratoriyasi. Sanoat dizayni va mexanik injiniring asoslari o'rgatiladi.",
            "order": 6,
        },
    ]

    labs = []
    for ld in labs_data:
        lab, _ = Laboratory.objects.get_or_create(
            name=ld["name"],
            defaults=ld,
        )
        labs.append(lab)
    print(f"   ✓ {len(labs)} ta laboratoriya yaratildi")

    # ──────────────────────────────────
    # PROGRAMS
    # ──────────────────────────────────
    print("\n[4/8] Ta'lim dasturlari...")
    now = timezone.now().date()
    programs_data = [
        {
            "name": "Robototexnika asoslari",
            "laboratory": labs[0],
            "description": "Arduino platformasi asosida robotlar yaratish, sensorlar bilan ishlash va C++ dasturlash tilini o'rganish. Kurs davomida talabalar o'z robotlarini loyihalash, yig'ish va dasturlashni o'rganadilar.",
            "level": "beginner",
            "age_min": 10, "age_max": 16,
            "format": "offline",
            "duration": "3 oy (48 soat)",
            "start_date": now + timedelta(days=14),
            "end_date": now + timedelta(days=104),
        },
        {
            "name": "Python dasturlash",
            "laboratory": labs[2],
            "description": "Python dasturlash tilining asoslaridan boshlab ilg'or mavzulargacha — ma'lumotlar tuzilmasi, OOP, API yaratish, web scraping va avtomatlashtirish. Har darsda amaliy mashqlar va mini-loyihalar.",
            "level": "beginner",
            "age_min": 12, "age_max": 25,
            "format": "hybrid",
            "duration": "4 oy (64 soat)",
            "start_date": now + timedelta(days=7),
            "end_date": now + timedelta(days=127),
        },
        {
            "name": "Full-Stack veb dasturlash",
            "laboratory": labs[2],
            "description": "HTML, CSS, JavaScript (React), Python (Django) va PostgreSQL yordamida to'liq veb ilovalar yaratish. REST API, deployment va DevOps asoslarini ham qamrab oladi.",
            "level": "advanced",
            "age_min": 14, "age_max": 25,
            "format": "offline",
            "duration": "6 oy (128 soat)",
            "start_date": now + timedelta(days=21),
            "end_date": now + timedelta(days=201),
        },
        {
            "name": "AI va Machine Learning",
            "laboratory": labs[1],
            "description": "Sun'iy intellekt asoslari, Machine Learning algoritmlari, neural networklar va real loyihalarda ularni qo'llash. Scikit-learn, TensorFlow va PyTorch bilan amaliy mashg'ulotlar.",
            "level": "advanced",
            "age_min": 16, "age_max": 25,
            "format": "hybrid",
            "duration": "5 oy (80 soat)",
            "start_date": now + timedelta(days=30),
            "end_date": now + timedelta(days=180),
        },
        {
            "name": "IoT loyihalar yaratish",
            "laboratory": labs[3],
            "description": "ESP32 va turli sensorlar yordamida aqlli qurilmalar yaratish — aqlli uy, aqlli bog', ob-havo stantsiyasi va boshqa amaliy IoT loyihalar. Cloud platformalar bilan integratsiya.",
            "level": "beginner",
            "age_min": 13, "age_max": 22,
            "format": "offline",
            "duration": "3 oy (48 soat)",
            "start_date": now + timedelta(days=10),
            "end_date": now + timedelta(days=100),
        },
        {
            "name": "Kiberxavfsizlik asoslari",
            "laboratory": labs[4],
            "description": "Tarmoq xavfsizligi, Ethical Hacking, Linux server boshqaruvi va xavfsizlik auditi. Kali Linux va turli xavfsizlik vositalari bilan amaliy mashg'ulotlar. CTF musobaqalariga tayyorgarlik.",
            "level": "advanced",
            "age_min": 15, "age_max": 25,
            "format": "offline",
            "duration": "4 oy (64 soat)",
            "start_date": now + timedelta(days=28),
            "end_date": now + timedelta(days=148),
        },
        {
            "name": "3D modellash va chop etish",
            "laboratory": labs[5],
            "description": "Fusion 360 va Blender dasturlarida 3D modellashtirish, STL fayllarni tayyorlash va 3D printerda chop etish. Sanoat dizayni asoslari va prototiplash jarayoni.",
            "level": "beginner",
            "age_min": 11, "age_max": 20,
            "format": "offline",
            "duration": "2.5 oy (40 soat)",
            "start_date": now + timedelta(days=5),
            "end_date": now + timedelta(days=80),
        },
        {
            "name": "Mobil ilovalar yaratish (Flutter)",
            "laboratory": labs[2],
            "description": "Google Flutter frameworki yordamida Android va iOS uchun cross-platform mobil ilovalar yaratish. Dart tili, Material Design, Firebase va API integratsiya.",
            "level": "advanced",
            "age_min": 15, "age_max": 25,
            "format": "hybrid",
            "duration": "5 oy (80 soat)",
            "start_date": now + timedelta(days=20),
            "end_date": now + timedelta(days=170),
        },
    ]

    programs = []
    for pd in programs_data:
        prog, _ = Program.objects.get_or_create(
            name=pd["name"],
            defaults=pd,
        )
        programs.append(prog)
    print(f"   ✓ {len(programs)} ta dastur yaratildi")

    # ──────────────────────────────────
    # EVENTS
    # ──────────────────────────────────
    print("\n[5/8] Tadbirlar...")
    events_data = [
        {
            "title": "Innovation Hackathon 2026",
            "event_type": "hackathon",
            "description": "24 soatlik intensiv dasturlash marafoni! Jamoalar real muammolarni hal qiluvchi innovatsion loyihalar yaratadi. Eng yaxshi 3 ta loyiha uchun jami 15 million so'm mukofot jamg'armasi. Mentorlar va sanoat mutaxassislari yordamida.",
            "date": timezone.now() + timedelta(days=25),
            "location": "YIM, Asosiy konferens-zal, 1-qavat",
        },
        {
            "title": "Sun'iy intellekt va kelajak kasblar",
            "event_type": "lecture",
            "description": "AI sohasining yetakchi mutaxassisi tomonidan sun'iy intellektning hozirgi holati, kelajakdagi rivojlanish tendensiyalari va yangi kasblar haqida qiziqarli ma'ruza. Savollar va munozara sessiyasi bilan.",
            "date": timezone.now() + timedelta(days=12),
            "location": "Online (Zoom) — havola ro'yxatdan o'tganlarga yuboriladi",
        },
        {
            "title": "Yosh innovatorlar tanlovi — 2026",
            "event_type": "competition",
            "description": "Yillik innovatsion loyihalar tanlovi. O'quvchilar o'z loyihalarini hakamlar hay'ati oldida taqdimot qiladilar. G'oliblar respublika tanloviga yo'llanma oladilar. Qatnashish uchun oldindan loyiha topshirish zarur.",
            "date": timezone.now() + timedelta(days=45),
            "location": "YIM, Taqdimot zali, 3-qavat",
        },
        {
            "title": "Python bilan Data Science — master-klass",
            "event_type": "masterclass",
            "description": "Pandas, NumPy va Matplotlib kutubxonalari bilan real ma'lumotlarni tahlil qilish bo'yicha 4 soatlik amaliy master-klass. O'z laptopingizni olib keling! Python asoslarini bilish tavsiya etiladi.",
            "date": timezone.now() + timedelta(days=8),
            "location": "YIM, Dasturlash laboratoriyasi, 2-qavat",
        },
        {
            "title": "Robototexnika Open Day",
            "event_type": "masterclass",
            "description": "Robototexnika laboratoriyasining ochiq eshiklar kuni! Robotlar ko'rgazmasi, jonli demo va Arduino bilan birinchi robotingizni yaratasiz. Ota-onalar va bolalar uchun bepul!",
            "date": timezone.now() + timedelta(days=18),
            "location": "YIM, Robototexnika laboratoriyasi, 1-qavat",
        },
        {
            "title": "Startup Weekend Toshkent",
            "event_type": "hackathon",
            "description": "48 soat ichida g'oyadan MVPgacha! Biznes g'oya generatsiyasi, jamoa-tuzish, mahsulot yaratish va investor oldida pitch. Investor mentorlar va 10 million so'm grant jamg'armasi.",
            "date": timezone.now() + timedelta(days=60),
            "location": "YIM, Coworking maydon, 2-qavat",
        },
    ]

    events = []
    for ed in events_data:
        event, _ = Event.objects.get_or_create(
            title=ed["title"],
            defaults=ed,
        )
        events.append(event)
    print(f"   ✓ {len(events)} ta tadbir yaratildi")

    # ──────────────────────────────────
    # PROJECTS (all approved by admin)
    # ──────────────────────────────────
    print("\n[6/8] Loyihalar...")
    projects_data = [
        {
            "title": "AgroSense — Aqlli qishloq xo'jaligi",
            "author": students[0],  # Jasur
            "description": "IoT sensorlar va AI yordamida tuproq namligini, haroratni va o'simlik holatini real vaqtda kuzatuvchi tizim. Fermerlar mobil ilova orqali dalalarini masofadan boshqara oladilar. Suv va energiya sarfini 40% gacha kamaytiradi.",
            "stage": "prototype",
            "team_members": "Jasur Karimov (Team Lead), Bobur Toshmatov (IoT), Dildora Nazarova (Backend)",
            "is_approved": True,
        },
        {
            "title": "EduBot — AI o'quv yordamchisi",
            "author": students[1],  # Malika
            "description": "GPT va RAG texnologiyalari asosida ishlaydigan shaxsiy o'quv yordamchisi chatbot. O'quvchilarga matematika, fizika va dasturlash bo'yicha tushuntirish beradi, savollarga javob qaytaradi va individual o'quv rejasini tuzadi.",
            "stage": "mvp",
            "team_members": "Malika Rahimova (AI/ML), Otabek Mirzayev (Frontend), Zilola Usmonova (UX)",
            "is_approved": True,
        },
        {
            "title": "GreenCity Analytics",
            "author": students[2],  # Sardor
            "description": "Shahar ekologiyasini monitoring qilish platformasi. Havo sifati, shovqin darajasi va chiqindi boshqaruvi ma'lumotlarini to'playdi va vizuallashtiradi. Shahar ma'muriyati uchun qaror qabul qilish tizimi.",
            "stage": "idea",
            "team_members": "Sardor Alimov (Data Scientist), Nodira Sultonova (Backend), Jasur Karimov (IoT)",
            "is_approved": True,
        },
        {
            "title": "MedTracker — Sog'liq kuzatuvchisi",
            "author": students[3],  # Dildora
            "description": "Bemor salomatligi holatini kuzatish uchun wearable qurilma va mobil ilova. Yurak urishi, bosim va haroratni o'lchaydi, anomaliyalarni aniqlaydi va shifokorga xabar yuboradi. Telemedicina moduli ham mavjud.",
            "stage": "prototype",
            "team_members": "Dildora Nazarova (Mobile Dev), Bobur Toshmatov (Hardware), Malika Rahimova (AI)",
            "is_approved": True,
        },
        {
            "title": "LearnUz — O'zbek tilidagi MOOC platforma",
            "author": students[6],  # Otabek
            "description": "O'zbek tilida bepul online ta'lim platformasi. Video darslar, interaktiv testlar, sertifikatlar va o'qituvchilar uchun kurs yaratish vositalari. Gamifikatsiya elementi bilan o'quvchilarni rag'batlantiradi.",
            "stage": "mvp",
            "team_members": "Otabek Mirzayev (Full-Stack), Zilola Usmonova (UX/UI), Sardor Alimov (DevOps)",
            "is_approved": True,
        },
        {
            "title": "SmartBin — Aqlli chiqindi saralash",
            "author": students[4],  # Bobur
            "description": "Computer Vision yordamida chiqindilarni avtomatik saralash tizimi. Kamera orqali plastik, qog'oz, shisha va organik chiqindilarni aniqlaydi va tegishli konteynerga yo'naltiradi. Qayta ishlash statistikasini yuritadi.",
            "stage": "idea",
            "team_members": "Bobur Toshmatov (Hardware), Malika Rahimova (Computer Vision)",
            "is_approved": True,
        },
        {
            "title": "CodeMentor — Dasturlash o'rganish platformasi",
            "author": students[5],  # Nodira
            "description": "Interaktiv dasturlash o'rganish veb ilovasi. Code challenge-lar, real-vaqtda kod tekshirish, progress tracking va mentor bilan bog'lanish imkoniyati. Python, JavaScript va C++ tillari qo'llab-quvvatlanadi.",
            "stage": "prototype",
            "team_members": "Nodira Sultonova (Backend), Otabek Mirzayev (Frontend), Dildora Nazarova (Mobile)",
            "is_approved": True,
        },
        {
            "title": "DroneMap — Dronlar bilan xarita yaratish",
            "author": students[7],  # Zilola
            "description": "Dronlar yordamida yuqori aniqlikdagi 3D xaritalar va ortofotosxemalar yaratish tizimi. Qurilish, qishloq xo'jaligi va shahar rejalashtirish uchun mo'ljallangan. Photogrammetry va LiDAR texnologiyalari.",
            "stage": "idea",
            "team_members": "Zilola Usmonova (GIS), Jasur Karimov (Drone Engineering), Sardor Alimov (Data)",
            "is_approved": True,
        },
    ]

    projects = []
    for ppd in projects_data:
        proj, _ = Project.objects.get_or_create(
            title=ppd["title"],
            defaults=ppd,
        )
        projects.append(proj)
    print(f"   ✓ {len(projects)} ta loyiha yaratildi (barchasi tasdiqlangan)")

    # ──────────────────────────────────
    # PARTNERS
    # ──────────────────────────────────
    print("\n[7/8] Hamkorlar...")
    partners_data = [
        {"name": "INHA University", "website": "https://inha.uz", "order": 1},
        {"name": "IT Park Uzbekistan", "website": "https://it-park.uz", "order": 2},
        {"name": "EPAM Systems", "website": "https://epam.com", "order": 3},
        {"name": "Google for Education", "website": "https://edu.google.com", "order": 4},
        {"name": "UNICEF Uzbekistan", "website": "https://unicef.org/uzbekistan", "order": 5},
        {"name": "Samsung Innovation", "website": "https://samsung.com", "order": 6},
        {"name": "Najot Ta'lim", "website": "https://najottalim.uz", "order": 7},
        {"name": "PDP Academy", "website": "https://pdp.uz", "order": 8},
    ]

    partners = []
    for pad in partners_data:
        partner, _ = Partner.objects.get_or_create(
            name=pad["name"],
            defaults=pad,
        )
        partners.append(partner)
    print(f"   ✓ {len(partners)} ta hamkor yaratildi")

    # ──────────────────────────────────
    # NEWS
    # ──────────────────────────────────
    print("\n[8/8] Yangiliklar...")
    news_data = [
        {
            "title": "Yangi robototexnika laboratoriyasi ochildi",
            "slug": "yangi-robototexnika-lab",
            "content": (
                "Yoshlar innovatsiya markazida eng zamonaviy uskunalar bilan jihozlangan yangi robototexnika "
                "laboratoriyasi o'z faoliyatini boshladi. Laboratoriya 20 dan ortiq Arduino va Raspberry Pi "
                "to'plamlari, 5 ta sanoat roboti, 3 ta dron va zamonaviy 3D printerlar bilan jihozlangan.\n\n"
                "Laboratoriya rahbari Jasur Ergashev: «Bu laboratoriya yoshlarimizga jahon standartlaridagi "
                "ta'lim olish imkonini beradi. Eng muhimi — bu yerda nazariya va amaliyot muvozanatiga e'tibor "
                "qaratiladi. Har bir talaba kurs davomida kamida 3 ta amaliy loyiha yaratadi».\n\n"
                "Laboratoriyaga 10-18 yoshdagi barcha qiziquvchilar qabul qilinadi. Ro'yxatdan o'tish "
                "markazning rasmiy veb-sayti orqali amalga oshiriladi."
            ),
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=3),
        },
        {
            "title": "Xalqaro xakatonda g'alaba — 1-o'rin!",
            "slug": "xalqaro-xakaton-galaba",
            "content": (
                "Markaz talabalari tarkibidagi «InnoTeam» jamoasi Dubayda bo'lib o'tgan Global Innovation "
                "Hackathon 2026 xalqaro xakatonida birinchi o'rinni qo'lga kiritdi! 47 ta mamlakatdan "
                "200 dan ortiq jamoa ishtirok etgan musobaqada bizning yoshlar «SmartWater» loyihasini "
                "taqdim etdilar.\n\n"
                "Loyiha suv resurslarini AI yordamida optimallashtirish tizimini taklif qiladi. Hakamlar "
                "hay'ati loyihaning amaliy ahamiyati va texnik implementatsiyasini yuqori baholadi.\n\n"
                "Jamoa a'zolari: Malika Rahimova (AI/ML), Otabek Mirzayev (Backend), Bobur Toshmatov (IoT) "
                "va Sardor Alimov (Data Science). Mukofot — 10,000 AQSh dollari va akseleratsiya dasturiga "
                "qabul qilinish."
            ),
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=7),
        },
        {
            "title": "2026-yil bahor ta'lim dasturlariga qabul boshlandi",
            "slug": "bahor-talim-dasturlar-2026",
            "content": (
                "Yoshlar innovatsiya markazi 2026-yil bahor semestrida 8 ta yo'nalish bo'yicha ta'lim "
                "dasturlariga qabul e'lon qiladi: Robototexnika, Python dasturlash, Full-Stack veb, "
                "AI/Machine Learning, IoT, Kiberxavfsizlik, 3D modellash va Mobil dasturlash.\n\n"
                "Barcha dasturlar bepul bo'lib, 10 yoshdan 25 yoshgacha bo'lgan yoshlar qabul qilinadi. "
                "Darslar haftada 3 kun, professional mentorlar rahbarligida o'tiladi. Kurs yakunida "
                "imtihondan muvaffaqiyatli o'tgan talabalarga rasmiy sertifikat topshiriladi.\n\n"
                "Ro'yxatdan o'tish 1-mart kunigacha davom etadi. Joylar soni cheklangan — har bir "
                "dasturda atigi 25 ta o'rin mavjud!"
            ),
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=1),
        },
        {
            "title": "Google Developer Expert markazda master-klass o'tkazdi",
            "slug": "google-developer-expert-masterklass",
            "content": (
                "Google Developer Expert unvoniga ega bo'lgan Flutter mutaxassisi markaz talabalariga "
                "ikki kunlik master-klass o'tkazdi. Master-klass davomida Flutter frameworkining "
                "so'nggi yangiliklari, state management yondashuvlari va performance optimizatsiyasi "
                "mavzulari yoritildi.\n\n"
                "Ikkinchi kun talabalar kichik jamoalarda amaliy loyiha ustida ishladilar — fitness "
                "tracker ilovasini yaratdilar. Eng yaxshi loyiha yaratgan jamoa Google tomonidan "
                "maxsus sovg'alar bilan taqdirlandi.\n\n"
                "Markaz bunday tadbirlarni muntazam ravishda o'tkazib turish rejasini tuzmoqda."
            ),
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=10),
        },
        {
            "title": "Markaz IT Park bilan hamkorlik memorandumini imzoladi",
            "slug": "it-park-hamkorlik",
            "content": (
                "Yoshlar innovatsiya markazi va IT Park Uzbekistan o'rtasida strategik hamkorlik "
                "memorandumi imzolandi. Memorandum doirasida quyidagi yo'nalishlarda hamkorlik "
                "qilinadi: birgalikda ta'lim dasturlarini ishlab chiqish, iqtidorli yoshlarni "
                "aniqlash va qo'llab-quvvatlash, startup akseleratsiya dasturlari va xalqaro "
                "anjumanlarda ishtirok etish.\n\n"
                "IT Park rahbari: «Yoshlar innovatsiya markazi bilan hamkorlik O'zbekistondagi "
                "IT ta'lim sifatini yangi bosqichga olib chiqadi. Biz markaz bitiruvchilariga "
                "IT Park rezidentlarida stajirovka o'tash imkonini yaratamiz»."
            ),
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=14),
        },
    ]

    news_list = []
    for nd in news_data:
        news_item, _ = News.objects.get_or_create(
            slug=nd["slug"],
            defaults=nd,
        )
        news_list.append(news_item)
    print(f"   ✓ {len(news_list)} ta yangilik yaratildi")

    # ──────────────────────────────────
    # DONE
    # ──────────────────────────────────
    print("\n" + "=" * 60)
    print("  ✅ Database muvaffaqiyatli to'ldirildi!")
    print("=" * 60)
    print(f"""
    Jami:
    • Sayt sozlamalari   — yangilandi
    • Talabalar          — {len(students)} ta
    • Laboratoriyalar    — {len(labs)} ta
    • Ta'lim dasturlari  — {len(programs)} ta
    • Tadbirlar          — {len(events)} ta
    • Loyihalar          — {len(projects)} ta (barchasi tasdiqlangan)
    • Hamkorlar          — {len(partners)} ta
    • Yangiliklar        — {len(news_list)} ta
    """)


if __name__ == "__main__":
    seed()
