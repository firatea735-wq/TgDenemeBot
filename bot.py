from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# ================== BOT BİLGİLERİ ==================
TELEGRAM_TOKEN = "8674149760:AAEVp4BRF0q12IMrFnOVRWDWAp5W5r4zN1k"
GROQ_API_KEY = "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"
# ===================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ TgDenemeBot aktif!\nMetin veya fotoğraf at, sor bakalım 🔥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fotoğraf geldiyse
    if update.message.photo:
        await update.message.reply_text("📸 Fotoğrafı aldım! Ne hakkında konuşmak istiyorsun?")
        return
    
    # Normal metin mesajı
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
    except Exception:
        await update.message.reply_text("Hata oldu, tekrar dene.")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), handle_message))
    
    print("✅ TgDenemeBot Render'da çalışıyor... (Fotoğraf desteği aktif)")
    app.run_polling()
