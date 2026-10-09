import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8334324978:AAHBjAnKYBn_QS9GowEaMsbr3QNquRWMWis")

# የዌብሳይትህ ሊንክ (HTTPS መሆን አለበት)
WEBAPP_URL = "https://your-website-url.com" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ልክ እንደ አፕሊኬሽን ዌብሳይቱን የሚከፍት ቁልፍ
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 ዳሽቦርድ ክፈት (Open Web App)", 
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"እንኳን ደህና መጡ {update.effective_user.first_name}!\n\n"
        "ወደ ዋናው ዳሽቦርድ ለመግባት ከታች ያለውን ቁልፍ ይጫኑ፦",
        reply_markup=reply_markup
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
