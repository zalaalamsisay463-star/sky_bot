import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

# Render ላይ ከ Environment Variables የሚወሰድ ወይም በቀጥታ ማስገባት ትችላለህ
TOKEN = os.getenv("BOT_TOKEN", "8334324978:AAHBjAnKYBn_QS9GowEaMsbr3QNquRWMWis")

CHOOSING_AUTH, GET_PASSWORD, LOGGED_IN = range(3)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

auth_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Sign Up"), KeyboardButton("Log In")]],
    resize_keyboard=True
)

dashboard_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 Dashboard"), KeyboardButton("🛒 Order")],
        [KeyboardButton("🔗 Share Me"), KeyboardButton("🚪 Logout")]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        await update.message.reply_text(
            f"እንኳን ደህና መጡ {update.effective_user.first_name}!",
            reply_markup=auth_keyboard
        )
    else:
        await update.message.reply_text(
            "እንኳን ደህና መጡ! ለመጀመር እባክዎ መለያ ይመዝግቡ (Sign Up ያድርጉ)።",
            reply_markup=auth_keyboard
        )
    return CHOOSING_AUTH

async def auth_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data["action"] = text

    if text == "Sign Up":
        await update.message.reply_text("እባክዎ አዲስ የይለፍ ቃል ያስገቡ፦")
        return GET_PASSWORD
    elif text == "Log In":
        await update.message.reply_text("እባክዎ የይለፍ ቃልዎን ያስገቡ፦")
        return GET_PASSWORD
    return CHOOSING_AUTH

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"
    action = context.user_data.get("action")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    if action == "Sign Up":
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            await update.message.reply_text("ቀደም ሲል ተመዝግበዋል! እባክዎ Log In ያድርጉ።", reply_markup=auth_keyboard)
            conn.close()
            return CHOOSING_AUTH
        
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, username, password))
        conn.commit()
        conn.close()
        await update.message.reply_text("ምዝገባዎ ተሳክቷል! ወደ ዳሽቦርድ ገብተዋል።", reply_markup=dashboard_keyboard)
        return LOGGED_IN

    elif action == "Log In":
        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row and row[0] == password:
            await update.message.reply_text("በተሳካ ሁኔታ ገብተዋል!", reply_markup=dashboard_keyboard)
            return LOGGED_IN
        else:
            await update.message.reply_text("የተሳሳተ የይለፍ ቃል! እንደገና ይሞክሩ።", reply_markup=auth_keyboard)
            return CHOOSING_AUTH

async def dashboard_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    bot_username = context.bot.username

    if text == "📊 Dashboard":
        await update.message.reply_text("📊 Dashboard ገጽ ላይ ነዎት። ሁሉም ነገር በትክክል እየሰራ ነው።")
    elif text == "🛒 Order":
        await update.message.reply_text("🛒 Order ገጽ፦ ትዕዛዝዎን እዚህ ማስገባት ይችላሉ።")
    elif text == "🔗 Share Me":
        share_link = f"https://t.me/{bot_username}?start={update.effective_user.id}"
        await update.message.reply_text(f"🔗 ቦቱን ለሌሎች ለማጋራት ሊንኩን ይጠቀሙ፦\n{share_link}")
    elif text == "🚪 Logout":
        await update.message.reply_text("ከመለያዎ ወጥተዋል።", reply_markup=auth_keyboard)
        return CHOOSING_AUTH
    
    return LOGGED_IN

def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_AUTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_choice)],
            GET_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
            LOGGED_IN: [MessageHandler(filters.TEXT & ~filters.COMMAND, dashboard_actions)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
