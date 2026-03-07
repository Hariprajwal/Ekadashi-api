import requests
import asyncio
from datetime import datetime
import pytz

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8690388308:AAFk837Z_ajcRwpMTrynlCaYTtGr-3QIEjE"
API_URL = "https://ekadashi-api.onrender.com/"

IST = pytz.timezone("Asia/Kolkata")

subscribers = set()


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    subscribers.add(chat_id)

    msg = """
🙏 *Ekadashi Reminder Bot*

Commands:

/today
/tomorrow
/next
/year 2026
/check 2026-03-15

You will automatically receive reminders.
"""

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- TODAY ----------------

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(f"{API_URL}/today").json()

    if data["is_ekadashi"]:
        msg = "🌼 *Today is Ekadashi!*"
    else:
        msg = "❌ Today is not Ekadashi."

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- TOMORROW ----------------

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(f"{API_URL}/tomorrow").json()

    if data["is_ekadashi"]:
        msg = "🌙 *Tomorrow is Ekadashi!* Prepare spiritually 🙏"
    else:
        msg = "Tomorrow is not Ekadashi."

    await update.message.reply_text(msg, parse_mode="Markdown")


async def next_ek(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(f"{API_URL}/next").json()

    date_obj = datetime.strptime(data["date"], "%Y-%m-%d")

    # D-M-YYYY format
    formatted_date = date_obj.strftime("%-d-%-m-%Y")

    days = data["days_until"]

    msg = f"""
🪔 *NEXT EKADASHI*

`{formatted_date}    {days}`

🌗 Paksha: {data['paksha']}
"""

    await update.message.reply_text(msg, parse_mode="Markdown") 


# ---------------- YEAR ----------------

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

    rows = max(len(krishna), len(shukla))

    msg = f"📜 *Ekadashi Calendar — {year}*\n\n"

    msg += "`Krishna Paksha      | Shukla Paksha\n"
    msg += "---------------------------------------\n"

    for i in range(rows):

        k = krishna[i] if i < len(krishna) else ""
        s = shukla[i] if i < len(shukla) else ""

        msg += f"{k:<20} | {s}\n"

    msg += "`"

    msg += f"\n\n✨ Total Ekadashis: *{data['total']}*"

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- CHECK ----------------

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /check YYYY-MM-DD")
        return

    date = context.args[0]

    data = requests.get(f"{API_URL}/check/{date}").json()

    if data["is_ekadashi"]:
        msg = f"✅ *{date} is Ekadashi.*"
    else:
        msg = f"❌ {date} is not Ekadashi."

    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------------- REMINDER SYSTEM ----------------

async def reminder_loop(app):

    while True:

        now = datetime.now(IST)

        today_data = requests.get(f"{API_URL}/today").json()
        tomorrow_data = requests.get(f"{API_URL}/tomorrow").json()

        # 9 PM reminder
        if now.hour == 21 and tomorrow_data["is_ekadashi"]:

            for chat_id in subscribers:

                await app.bot.send_message(
                    chat_id,
                    "🌙 *Tomorrow is Ekadashi*\n\nPrepare mentally for fasting 🙏",
                    parse_mode="Markdown"
                )

        # 6 AM reminder
        if now.hour == 6 and today_data["is_ekadashi"]:

            for chat_id in subscribers:

                await app.bot.send_message(
                    chat_id,
                    "🌼 *Ekadashi has started*\n\nObserve fasting and devotion 🙏",
                    parse_mode="Markdown"
                )

        await asyncio.sleep(3600)


# ✅ FIX: Schedule reminder_loop AFTER the event loop is running
async def post_init(app):
    asyncio.create_task(reminder_loop(app))


# ---------------- MAIN ----------------

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

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















    #BOT_TOKEN = "8690388308:AAFk837Z_ajcRwpMTrynlCaYTtGr-3QIEjE"
