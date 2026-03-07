import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "your api key "
API_URL = "http://127.0.0.1:8000"


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = """
🙏 *Ekadashi Reminder Bot*

Available Commands:

📅 */today*  
Check if today is Ekadashi

🌙 */tomorrow*  
Check if tomorrow is Ekadashi

🪔 */next*  
Next upcoming Ekadashi

📜 */year 2026*  
Show all Ekadashis of a year

🔎 */check 2026-03-15*  
Check specific date
"""

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- TODAY ----------------

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(f"{API_URL}/today").json()

    if data["is_ekadashi"]:

        msg = """
🌼 *Today is Ekadashi*

A sacred day for fasting and devotion 🙏
"""

    else:

        msg = "❌ Today is not Ekadashi."

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- TOMORROW ----------------

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(f"{API_URL}/tomorrow").json()

    if data["is_ekadashi"]:

        msg = """
🌙 *Tomorrow is Ekadashi*

Prepare yourself mentally and spiritually 🙏
"""

    else:

        msg = "Tomorrow is not Ekadashi."

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- NEXT EKADASHI ----------------

async def next_ek(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(f"{API_URL}/next").json()

    msg = f"""
🪔 *Next Ekadashi*

📅 Date: *{data['date']}*  
🌗 Paksha: *{data['paksha']}*  
⏳ Days remaining: *{data['days_until']}*

Stay prepared 🙏
"""

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- YEAR CALENDAR ----------------

async def year(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /year 2026")
        return

    year = context.args[0]

    data = requests.get(f"{API_URL}/year/{year}").json()

    krishna = []
    shukla = []

    for e in data["dates"]:

        date = datetime.strptime(e["date"], "%Y-%m-%d")

        formatted = date.strftime("%d %b")

        if e["paksha"] == "Krishna":
            krishna.append(formatted)
        else:
            shukla.append(formatted)

    msg = f"📜 *Ekadashi Calendar — {year}*\n\n"

    msg += "🌑 *Krishna Paksha*\n"

    for d in krishna:
        msg += f"• {d}\n"

    msg += "\n🌕 *Shukla Paksha*\n"

    for d in shukla:
        msg += f"• {d}\n"

    msg += f"\n✨ Total Ekadashis: *{data['total']}*"

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- CHECK DATE ----------------

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /check YYYY-MM-DD")
        return

    date = context.args[0]

    data = requests.get(f"{API_URL}/check/{date}").json()

    if "error" in data:
        await update.message.reply_text(data["error"])
        return

    if data["is_ekadashi"]:

        msg = f"""
✅ *{date} is Ekadashi*

Observe fasting and devotion 🙏
"""

    else:

        msg = f"❌ {date} is not Ekadashi."

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- MAIN ----------------

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("next", next_ek))
    app.add_handler(CommandHandler("year", year))
    app.add_handler(CommandHandler("check", check))

    print("Ekadashi Telegram Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()



##CHAT_ID = "7690163799"












