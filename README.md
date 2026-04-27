# 🕉️ Ekadashi Reminder & Calendar

A **complete Ekadashi calculation system** consisting of:

* 🌐 **Public Ekadashi API**
* 📅 **Interactive Web Calendar**
* 🤖 **Telegram Reminder Bot**
* 🔭 **Astronomically accurate calculations**

This project calculates **Ekadashi dates using astronomical moon–sun positions**, rather than relying on static tables.

---

# 🌍 Live Demo

### 🌐 Website

https://hariprajwal.github.io/Ekadashi-reminder/

Interactive interface to:

* Check if today is Ekadashi
* Find next Ekadashi
* View Ekadashi calendar for any year
* Check specific dates

---

### 🔌 Public API

Base API endpoint:

https://ekadashi-api.onrender.com/

This API can be integrated into:

* Mobile apps
* Telegram bots
* Calendar apps
* Websites
* Spiritual reminder systems

---

# 📌 Features

### Accurate Ekadashi Calculation

The system calculates Ekadashi using:

* **Sun–Moon angular distance**
* **Tithi calculations**
* **Arunodaya rule (96 minutes before sunrise)**
* **Vaishnava / ISKCON fasting rules**

Each Ekadashi is classified as:

* 🌕 **Shukla Paksha** (Waxing Moon)
* 🌑 **Krishna Paksha** (Waning Moon)

---

### Telegram Reminder Bot

The bot automatically sends reminders:

* 🌙 **1 day before Ekadashi**
* 🌅 **6 AM on Ekadashi day**

Users can also query:

```
/today
/tomorrow
/next
/year 2026
/check 2026-03-15
```

---

### Interactive Website

The website allows users to:

✔ Check today's Ekadashi
✔ Check tomorrow's Ekadashi
✔ Find next Ekadashi
✔ View full yearly calendar
✔ Verify any specific date

---

# 🧠 How Ekadashi is Calculated

Ekadashi is determined by **tithi (lunar day)**.

A tithi is calculated using:

```
Tithi = (Moon Longitude − Sun Longitude) / 12°
```

Each tithi spans **12 degrees** of separation between the Moon and Sun.

Ekadashi corresponds to:

```
11th Tithi
```

---

### Astronomical Calculation Steps

1️⃣ Calculate **Julian day**

2️⃣ Get **Sun longitude**

3️⃣ Get **Moon longitude**

4️⃣ Compute angular difference

```
elongation = (moon_longitude - sun_longitude) % 360
```

5️⃣ Determine tithi

```
tithi = int(elongation / 12) + 1
```

---

### Arunodaya Rule

Vaishnava Ekadashi fasting follows an additional rule:

Ekadashi must be present at:

```
Arunodaya = Sunrise - 96 minutes
```

If **Dashami overlaps Arunodaya**, the fasting day shifts.

This rule ensures the **correct observance day**.

---

# 📡 API Endpoints

## Base URL

```
https://ekadashi-api.onrender.com
```

---

## Check Today

```
/today
```

Example response:

```json
{
 "date": "2026-03-15",
 "is_ekadashi": true
}
```

---

## Check Tomorrow

```
/tomorrow
```

---

## Next Ekadashi

```
/next
```

Example response:

```json
{
 "date": "2026-03-29",
 "paksha": "Shukla",
 "days_until": 14
}
```

---

## Ekadashis in a Year

```
/year/{year}
```

Example:

```
/year/2028
```

Response:

```json
{
 "year": 2028,
 "total": 25,
 "dates": [
   {"date":"2028-01-08","paksha":"Shukla"},
   {"date":"2028-01-22","paksha":"Krishna"}
 ]
}
```

---

## Check Specific Date

```
/check/YYYY-MM-DD
```

Example:

```
/check/2026-03-15
```

---

# 🏗️ Project Architecture

```
                ┌─────────────────────────┐
                │     GitHub Pages        │
                │   Ekadashi Website      │
                └──────────┬──────────────┘
                           │
                           ▼
                ┌─────────────────────────┐
                │        Render API       │
                │     FastAPI Server      │
                └──────────┬──────────────┘
                           │
                           ▼
                ┌─────────────────────────┐
                │   Ekadashi Calculator   │
                │  Swiss Ephemeris Logic  │
                └─────────────────────────┘
```

---

# 🧰 Technologies Used

### Backend

* **Python**
* **FastAPI**
* **Swiss Ephemeris**
* **pytz**

---

### Frontend

* HTML
* CSS
* JavaScript
* GitHub Pages

---

### Infrastructure

* Render (API hosting)
* GitHub Pages (website hosting)
* Telegram Bot API

---

# 🚀 Deployment

### API Deployment

Hosted on:

```
Render
```

Start command:

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

### Website Deployment

Hosted using:

```
GitHub Pages
```

---

# 📷 Screenshots

(Add images here)

Example:

```
/images/website.png
/images/calendar.png
/images/api.png
```

---

# 🔗 Integration Example

Example JavaScript request:

```javascript
fetch("https://ekadashi-api.onrender.com/next")
.then(res => res.json())
.then(data => console.log(data))
```

---

# 📅 Example Output

Next Ekadashi:

```
Date: 29 March 2026
Paksha: Shukla
Days remaining: 14
```

---

# 📖 Why This Project Exists

Many Ekadashi calendars online:

* rely on **static tables**
* do not expose **developer APIs**
* cannot be integrated with applications

This project provides:

✔ Dynamic calculations
✔ Open API
✔ Developer integration
✔ Reminder automation

---

# 🤝 Contributions

Pull requests and improvements are welcome.

Possible future improvements:

* Panchang API
* Moon phase display
* Festival calendar
* Mobile app

---

# 📜 License

MIT License

---

# 🙏 Acknowledgements

Inspired by traditional **Vaishnava Panchang calculations** and astronomical ephemeris data.

---

# 🕉️

May this project help devotees observe Ekadashi with devotion and awareness.
