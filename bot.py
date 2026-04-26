from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# ================== BOT BİLGİLERİ ==================
TELEGRAM_TOKEN = "8674149760:AAGP-gAoaM0UKGwMibeyKZyElpxUuQtZZKQ"
GROQ_API_KEY = "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"
# ===================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ TgDenemeBot 24/7 aktif!\nSor bakalım 🔥")

async def grok_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.8,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("Biraz bekle, tekrar dene.")
    except:
        await update.message.reply_text("Hata oldu, tekrar dene.")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, grok_reply))
    
    print("✅ Bot Render'da çalışıyor...")
    app.run_polling()
