# Dessert Crown Quvasoy — Telegram Sotuv Boti

Quvasoy shahridagi **Dessert Crown** (Soy Bo'yi turar-joy majmuasi) qurilish firmasi uchun
to'liq funksional Telegram sotuv boti.

Aiogram 3.x (Python) + SQLAlchemy + SQLite/PostgreSQL.

---

## ✨ Imkoniyatlari

| Imkoniyat | Tavsif |
|-----------|--------|
| 🏢 **Xonadonlar katalogi** | 1 / 2 / 3 xonali xonadonlar, planrovka rasmi, narx, qavat |
| 💰 **To'lov kalkulyatori** | Foizsiz nasiya hisoblovchi — boshlang'ich % va muddat tanlanadi |
| 🎁 **Aksiyalar bloki** | Promo banner + matn (sizning "MAXSUS TAKLIF" formatida) |
| 📞 **Lid yig'ish (anketa)** | Ism + telefon + xonadon turi + to'lov turi → admin/menejerga real-time xabar |
| 📍 **Manzil va kontaktlar** | Menejerga to'g'ridan-to'g'ri qo'ng'iroq/yozish tugmalari |
| 🌐 **Ikki tillilik** | O'zbek (lotin) + Русский |
| 🛠 **Admin panel** | `/admin` — statistika, lidlar, xonadonlar |
| 📊 **Statistika** | Foydalanuvchilar, lidlar, eng mashhur xonadonlar, kalkulyator ishlatilishi |
| 🗄 **SQLite/PostgreSQL** | Boshlash uchun SQLite (sozlama kerak emas), o'sish uchun PostgreSQL |

---

## 📁 Loyiha tuzilmasi

```
dessert-crown-bot/
├── bot/
│   ├── main.py              # Entrypoint
│   ├── config.py            # .env'dan sozlamalar
│   ├── seed.py              # Demo xonadonlarni DB'ga yozadi
│   ├── handlers/            # Routerlar (start, catalog, calculator, lead, admin)
│   ├── keyboards/           # Reply va inline klaviaturalar
│   ├── states/              # FSM holatlari
│   ├── db/                  # SQLAlchemy modellar va repozitor
│   ├── utils/               # Pul/maydon formatlash, kalkulyator
│   └── locales/             # UZ va RU tarjimalar
├── data/                    # Planrovka rasmlari va DB fayli
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Tez ishga tushirish (lokal kompyuterda)

### 1. Repo'ni klonlash

```bash
git clone <repo-url> dessert-crown-bot
cd dessert-crown-bot
```

### 2. `.env` yaratish

```bash
cp .env.example .env
```

Tahrirlang va quyidagi maydonlarni to'ldiring:

```env
BOT_TOKEN=<@BotFather'dan olingan token>
ADMIN_IDS=228114133            # /myid komandasidan oling
MANAGER_ID=228114133
MANAGER_NAME=Aziz
MANAGER_PHONE=+998 93 370 73 41
MANAGER_USERNAME=Azizov71992
COMPANY_NAME=Dessert Crown Quvasoy
COMPANY_ADDRESS=Quvasoy shahri, Soy Bo'yi turar-joy majmuasi
COMPANY_PHONE=+998 93 370 73 41
DATABASE_URL=sqlite+aiosqlite:///data/bot.db
```

### 3. Bog'liqliklarni o'rnatish

```bash
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Demo xonadonlarni yozish (faqat birinchi marta)

```bash
python -m bot.seed
```

### 5. Botni ishga tushirish

```bash
python -m bot.main
```

Telegram'da `/start` yuborib testlang.

---

## 🐳 Docker bilan ishga tushirish

```bash
docker compose up -d --build
```

Loglarni ko'rish:

```bash
docker compose logs -f bot
```

To'xtatish:

```bash
docker compose down
```

---

## ☁️ Production deploy (VPS — masalan Hetzner)

### 1. Server yaratish

- **Hetzner CX22** (~$5/oy) — 2 vCPU, 4 GB RAM, 40 GB SSD — yetarlidan ko'p
- Ubuntu 24.04 LTS

### 2. Docker o'rnatish

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Repo'ni klonlash va sozlash

```bash
git clone <repo-url> ~/dessert-crown-bot
cd ~/dessert-crown-bot
cp .env.example .env
nano .env    # Tokenni va boshqa sozlamalarni kiriting
```

### 4. Ishga tushirish

```bash
docker compose up -d --build
```

### 5. Botning ishlayotganini tekshirish

```bash
docker compose ps
docker compose logs --tail=50 bot
```

Bot avtomatik ravishda **server qayta yuklanganda ham qayta ishga tushadi** (`restart: unless-stopped`).

---

## 🔧 Bot ichida ishlatiladigan komandalar

| Komanda | Tavsif | Kim uchun |
|---------|--------|-----------|
| `/start` | Botni boshlash, asosiy menyu | Hamma |
| `/language` | Tilni almashtirish | Hamma |
| `/myid` | Telegram ID raqamini ko'rish | Hamma |
| `/admin` | Admin paneli | Faqat ADMIN_IDS |

---

## 📥 Yangi xonadon qo'shish

Hozircha xonadonlar `bot/seed.py` faylida belgilangan. Yangi xonadon qo'shish uchun:

1. Planrovka rasmini `data/` papkasiga joylang (masalan, `data/plan_3room_85.jpg`)
2. `bot/seed.py` faylida `DEMO_APARTMENTS` ro'yxatiga yangi `dict` qo'shing
3. `python -m bot.seed` ishga tushiring

**Kelajak yo'l xaritasi:** admin panel orqali bevosita Telegram'dan yangi xonadon qo'shish (planrovka rasmini yuborib).

---

## 🎯 Marketing

### Lidlar qanday keladi?

Mijoz quyidagi yo'llardan biri orqali "tegishadi":
- 🏠 Asosiy menyudagi **"Menejer bilan bog'lanish"**
- 🏡 Har bir xonadon kartochkasidagi **"Ko'rikka yozilish"** tugmasi
- 💰 Kalkulyator natijasidan keyingi **"Ko'rikka yozilish"** tugmasi
- 🎁 "MAXSUS TAKLIF" promo'sidan keyingi **"Anketa to'ldirish"** tugmasi

Anketa to'ldirilgach **darhol** menejerga (228114133 — Aziz) push xabar keladi:

```
🔔 YANGI LID!

👤 Ism: Aziz Karimov
📱 Telefon: +998 90 123 45 67
💬 Telegram: @aziz_user

🏡 Xonadon: 2 xonali 63.4 m²
💰 Narx: 402 750 000 so'm
💳 To'lov turi: Bo'lib-bo'lib (foizsiz)

🔢 Lid #14
```

### Konversiyani oshirish bo'yicha tavsiyalar

1. **Aksiya bloki**ni eng yuqori prioritetga qo'ying ("MAXSUS TAKLIF" 1-banner)
2. **Kalkulyator** keyingi qadam — har bir interaktsiyada ko'rsating
3. **Followup** — 2 kun ichida menejer aloqaga chiqsin (CRM'da kuzating)
4. **Reklamalar** — Tashkent, Farg'ona vodiysi guruhlariga shu botning linki bilan

---

## 🛡 Xavfsizlik

- ✅ Token `.env` faylida saqlanadi, `git`'ga commit qilinmaydi
- ✅ Admin huquqi faqat `ADMIN_IDS` ro'yxatidagi Telegram ID'lar uchun
- ✅ Mijoz telefon raqami validatsiyadan o'tadi
- ✅ Anketa ma'lumotlari **sizning serveringizdagi** SQLite/PostgreSQL'da saqlanadi
- ✅ Botning kodi to'liq sizning nazoratingizda

---

## 📈 Statistika va analitika

Admin panel (`/admin`) orqali ko'rinadi:

- 👥 Jami foydalanuvchilar va bugungi yangi
- 📋 Jami lidlar va so'nggi 7 kun
- 📊 Lidlar statusi bo'yicha (yangi, aloqaga chiqildi, ko'rikka keldi, ...)
- 🔥 Eng mashhur xonadonlar (lid soni bo'yicha)

---

## ❓ Tez-tez beriladigan savollar

**Bot Telegram'da ishlayaptimi?**
Botning username'i — `@Dessertcrown_bot` (demo uchun). O'z botingizni @BotFather orqali yarating va tokenni `.env`'ga qo'ying.

**Mijoz ma'lumotlari qayerda saqlanadi?**
SQLite DB faylida — `data/bot.db`. Production'da PostgreSQL tavsiya etiladi.

**Telegram fayl chegarasi 50 MB. Bu yetarlimi?**
Planrovka rasmlari uchun yetarli. Agar 3D tour video kerak bo'lsa, YouTube linkini yuboring.

**Bot ishlamay qolsa?**
Loglarni ko'ring: `docker compose logs -f bot`. Tokensiz ishlamaydi, restart qilib ko'ring.

---

## 📝 Litsenziya

Dessert Crown Quvasoy uchun maxsus yaratilgan. Boshqa firmalar uchun shablon sifatida ishlatish mumkin.

---

## 👥 Aloqa

- **Menejer:** Aziz — [+998 93 370 73 41](tel:+998933707341)
- **Telegram:** [@Azizov71992](https://t.me/Azizov71992)
- **Manzil:** Quvasoy shahri, Soy Bo'yi turar-joy majmuasi
