"""O'zbek tilidagi matnlar."""

UZ = {
    # Asosiy
    "welcome": (
        "🏡 <b>{company_name}</b>ga xush kelibsiz!\n\n"
        "Bu yerda siz:\n"
        "✅ Yangi qurilayotgan zamonaviy xonadonlarni ko'rasiz\n"
        "✅ Planrovkalar va narxlar bilan tanishasiz\n"
        "✅ Foizsiz nasiyaning shartlarini hisoblaysiz\n"
        "✅ Tez ko'rikka yozilishingiz mumkin\n\n"
        "Quyidagi tugmalardan birini tanlang 👇"
    ),
    "menu_catalog": "🏢 Xonadonlarni ko'rish",
    "menu_calculator": "💰 To'lov kalkulyatori",
    "menu_promotions": "🎁 Aksiyalar va chegirmalar",
    "menu_contact": "📞 Menejer bilan bog'lanish",
    "menu_about": "ℹ️ Biz haqimizda",
    "menu_location": "📍 Manzil",
    "menu_language": "🌐 Til / Язык",
    "menu_back": "⬅️ Orqaga",
    "menu_main": "🏠 Asosiy menyu",

    # Til
    "choose_language": "Tilni tanlang / Выберите язык:",
    "language_uz": "🇺🇿 O'zbekcha",
    "language_ru": "🇷🇺 Русский",
    "language_changed": "✅ Til o'zgartirildi.",

    # Katalog
    "catalog_choose_rooms": "Qaysi turdagi xonadon kerak?",
    "catalog_1_room": "🔹 1 xonali",
    "catalog_2_rooms": "🔹 2 xonali",
    "catalog_3_rooms": "🔹 3 xonali",
    "catalog_all": "🔹 Hammasini ko'rish",
    "catalog_empty": (
        "Hozircha bu turdagi xonadonlar mavjud emas.\n"
        "Iltimos, menejerimiz bilan bog'laning yoki keyinroq qayta urinib ko'ring."
    ),
    "apartment_card": (
        "🏡 <b>{title}</b>\n\n"
        "📐 Maydoni: <b>{area} m²</b>\n"
        "🚪 Xonalar: <b>{rooms} ta</b>\n"
        "🏢 Qavat: <b>{floors}</b>\n\n"
        "💰 To'liq narx: <b>{price}</b>\n"
        "📊 1 m² narxi: <b>{price_per_m2}</b>\n\n"
        "<b>20% boshlang'ich + 60 oy foizsiz nasiya:</b>\n"
        "🔹 Boshlang'ich: <b>{down_payment_20}</b>\n"
        "🔹 Har oy: <b>{monthly_60_20}</b>\n\n"
        "{description}"
    ),
    "btn_calculator": "💰 To'lov kalkulyatori",
    "btn_book_viewing": "🗓 Ko'rikka yozilish",
    "btn_contact_manager": "📞 Menejer bilan bog'lanish",
    "btn_view_plan": "📐 Planrovka",

    # Kalkulyator
    "calc_intro": (
        "💰 <b>To'lov kalkulyatori</b>\n\n"
        "Quyidagi parametrlarni tanlang yoki kiritng — biz oylik to'lovingizni hisoblab beramiz."
    ),
    "calc_choose_apartment": "Xonadon tanlang:",
    "calc_enter_price": (
        "Xonadon narxini kiriting (so'mda):\n\n"
        "Misol: <code>402750000</code>"
    ),
    "calc_choose_down_payment": (
        "Boshlang'ich to'lov foizini tanlang:\n\n"
        "💡 Qancha ko'p bo'lsa, oylik to'lov shuncha kam bo'ladi."
    ),
    "calc_down_payment_0": "0% (boshlang'ichsiz)",
    "calc_down_payment_10": "10%",
    "calc_down_payment_20": "20% (eng mashhur)",
    "calc_down_payment_30": "30%",
    "calc_down_payment_50": "50%",
    "calc_down_payment_custom": "✏️ Boshqa foiz",
    "calc_enter_custom_percent": "Boshlang'ich foizni kiriting (0 dan 100 gacha):",
    "calc_choose_term": "Muddatni tanlang:",
    "calc_term_12": "12 oy (1 yil)",
    "calc_term_24": "24 oy (2 yil)",
    "calc_term_36": "36 oy (3 yil)",
    "calc_term_60": "60 oy (5 yil) — eng mashhur",
    "calc_term_84": "84 oy (7 yil)",
    "calc_term_custom": "✏️ Boshqa muddat",
    "calc_enter_custom_term": "Muddatni oyda kiriting (1 dan 240 gacha):",
    "calc_result": (
        "📊 <b>Kalkulyator natijasi</b>\n\n"
        "🏡 Xonadon narxi: <b>{price}</b>\n"
        "📐 Maydon: <b>{area}</b>\n\n"
        "💵 <b>Boshlang'ich to'lov ({down_pct}%):</b>\n"
        "    <b>{down_payment}</b>\n\n"
        "📅 <b>Bo'lib to'lash:</b>\n"
        "    Muddati: {term} oy\n"
        "    Foiz: <b>0% (foizsiz!)</b>\n"
        "    Penya: <b>yo'q</b>\n\n"
        "💰 <b>Har oy to'lov: {monthly}</b>\n"
        "💸 Jami to'lov: <b>{total}</b>\n\n"
        "✨ Bu xonadon sizniki bo'lishi mumkin!"
    ),
    "calc_invalid_number": "❌ Iltimos, faqat raqam kiriting.",
    "calc_invalid_range": "❌ Qiymat noto'g'ri. Iltimos, qayta urinib ko'ring.",

    # Aksiyalar / promo
    "promo_main": (
        "🎁 <b>HOZIRGI AKSIYALAR</b>\n\n"
        "🔥 <b>2 xonali 63.4 m² xonadon orzusidamisiz?</b>\n\n"
        "💭 100% to'lov qilishga imkoniyatingiz yo'qmi?\n"
        "Muammo emas — bizda yechim bor! 🏡\n\n"
        "💥 Faqat <b>20% boshlang'ich to'lov</b> bilan\n"
        "o'z xonadoningizga ega bo'ling!\n\n"
        "📈 Siz bu xonadonni\n"
        "<b>21 500 000 so'm FOYDA</b> bilan xarid qilasiz!\n\n"
        "Qolgan summani esa:\n"
        "✅ 60 oy muddatga\n"
        "✅ FOIZSIZ\n"
        "✅ PENYASIZ\n"
        "✅ Har oy atigi <b>5 370 000 so'm</b>dan\n"
        "to'lab, osonlik bilan uy egasiga aylanasiz 🔑\n\n"
        "✨ 63.4 m² — keng va qulay reja\n"
        "✨ Oila uchun ideal tanlov\n"
        "✨ Zamonaviy qurilish va yaxshi joylashuv\n\n"
        "⏳ <b>Shoshiling!</b> Bunday narx va shartlar uzoqqa cho'zilmaydi!\n"
        "📩 Hozir yozing — batafsil ma'lumot oling!"
    ),

    # Menejer / lid
    "lead_collect_intro": (
        "📝 <b>Anketa</b>\n\n"
        "Menejerimiz siz bilan tez bog'lanishi uchun bir nechta savol beramiz."
    ),
    "lead_ask_name": "Ismingizni kiriting:",
    "lead_ask_phone": (
        "Telefon raqamingizni yuboring 📞\n\n"
        "Pastdagi tugmani bosing yoki qo'lda yozing.\n"
        "Misol: <code>+998 90 123 45 67</code>"
    ),
    "lead_share_contact": "📱 Telefon raqamimni yuborish",
    "lead_ask_rooms": "Qancha xonali xonadon qiziqtiradi?",
    "lead_ask_payment": (
        "To'lov turini tanlang:"
    ),
    "lead_payment_cash": "💵 100% naqd",
    "lead_payment_installment": "📅 Bo'lib-bo'lib (foizsiz)",
    "lead_payment_mortgage": "🏦 Bank ipotekasi",
    "lead_payment_undecided": "🤔 Hali aniq emas",
    "lead_ask_notes": (
        "Qo'shimcha izoh yoki savolingiz bormi? Yozing yoki <b>O'tkazib yuborish</b> tugmasini bosing."
    ),
    "lead_btn_skip": "⏭ O'tkazib yuborish",
    "lead_success": (
        "✅ <b>Rahmat, {name}!</b>\n\n"
        "Ma'lumotlaringiz menejerga yuborildi.\n"
        "📞 Tez orada sizga <b>{phone}</b> raqamiga qo'ng'iroq qilamiz.\n\n"
        "Sabringiz uchun rahmat! 🤝"
    ),
    "lead_invalid_phone": (
        "❌ Telefon raqami noto'g'ri.\n"
        "Iltimos, <code>+998 XX XXX XX XX</code> formatida yuboring."
    ),

    # Kontakt
    "contact_info": (
        "📞 <b>Bizning kontaktlar</b>\n\n"
        "👤 Menejer: <b>{manager_name}</b>\n"
        "📱 Telefon: <b>{manager_phone}</b>\n"
        "💬 Telegram: @{manager_username}\n\n"
        "🏢 Manzil: {company_address}\n"
        "📞 Ofis: {company_phone}\n\n"
        "🕒 Ish vaqti: Du-Sha 9:00 - 19:00\n\n"
        "Pastdagi tugma orqali to'g'ridan-to'g'ri yozishingiz mumkin."
    ),
    "contact_btn_call": "📞 Qo'ng'iroq qilish",
    "contact_btn_message": "💬 Telegram'da yozish",

    # Manzil
    "location_info": (
        "📍 <b>Bizning manzilimiz</b>\n\n"
        "🏢 {company_name}\n"
        "🗺 {company_address}\n\n"
        "Yandex/Google Maps'da ochish uchun pastdagi tugmani bosing."
    ),

    # Biz haqimizda
    "about_info": (
        "🏢 <b>{company_name}</b>\n\n"
        "Biz Quvasoy shahrida zamonaviy, qulay va arzon uylar quramiz.\n\n"
        "✨ <b>Bizning afzalliklarimiz:</b>\n"
        "✅ Sifatli qurilish materiallari\n"
        "✅ Zamonaviy planrovkalar\n"
        "✅ Foizsiz nasiya imkoniyati\n"
        "✅ Tez topshirish muddatlari\n"
        "✅ Qulay joylashuv\n\n"
        "📞 Batafsil ma'lumot uchun menejer bilan bog'laning."
    ),

    # Admin
    "admin_panel": "🛠 <b>Admin paneli</b>",
    "admin_stats": "📊 Statistika",
    "admin_leads": "📋 Lidlar",
    "admin_apartments": "🏢 Xonadonlar",
    "admin_broadcast": "📢 Hamma uchun xabar",
    "admin_not_allowed": "❌ Sizda admin huquqi yo'q.",

    # Universal
    "loading": "⏳ Yuklanmoqda...",
    "error": "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
    "coming_soon": "🚧 Bu funksiya tez orada ishga tushiriladi.",
}
