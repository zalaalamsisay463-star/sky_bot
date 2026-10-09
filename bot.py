import os
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN" 8334324978:AAHBjAnKYBn_QS9GowEaMsbr3QNquRWMWis")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ReplyKeyboardRemove() ከስር ያሉትን የ Sign Up እና Log In ቁልፎች ያጠፋል
    await update.message.reply_text(
        f"እንኳን ደህና መጡ {update.effective_user.first_name}!\n\n"
        "ለመቀጠል ከታች በስተግራ ያለውን የሜኑ (App) ቁልፍ ይጫኑ።",
        reply_markup=ReplyKeyboardRemove()
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
