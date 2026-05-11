# ============================================
# ZOYA AI TELEGRAM BOT
# ============================================

import os
import logging
import google.generativeai as genai

from dotenv import load_dotenv

from telegram import Update
from telegram.constants import ChatAction

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ============================================
# LOAD ENV
# ============================================

load_dotenv()

BOT_TOKEN = os.getenv("8013074037:AAGsBsDHB-mIJHfXnMX-qPSiAZjsH4Sg3IY")
GEMINI_API_KEY = os.getenv("AIzaSyBY_9ZG9-faahs2ZWqL_KMO-9IBZYbdXuI")

# ============================================
# CHECK ENV
# ============================================

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

# ============================================
# GEMINI SETUP
# ============================================

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# ============================================
# START COMMAND
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.first_name

    text = f"""
👋 Hello {user}

💖 Welcome to Zoya AI

আমি তোমার AI assistant 🤖
যেকোনো প্রশ্ন করতে পারো ✨
"""

    await update.message.reply_text(text)

# ============================================
# HELP COMMAND
# ============================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
📌 Commands

/start - Start Bot
/help - Help Menu

💬 শুধু message পাঠাও
"""

    await update.message.reply_text(help_text)

# ============================================
# AI CHAT
# ============================================

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    try:

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        prompt = f"""
You are Zoya AI Assistant.

Reply smartly, shortly and friendly.

User Message:
{user_message}
"""

        response = model.generate_content(prompt)

        ai_reply = response.text

        if not ai_reply:
            ai_reply = "⚠️ No response."

        await update.message.reply_text(ai_reply)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{str(e)}"
        )

# ============================================
# ERROR HANDLER
# ============================================

async def error_handler(update, context):

    print(f"ERROR: {context.error}")

# ============================================
# MAIN
# ============================================

def main():

    print("🚀 Zoya AI Bot Started")

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat
        )
    )

    # Error Handler
    app.add_error_handler(error_handler)

    # Run Bot
    app.run_polling()

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    main()