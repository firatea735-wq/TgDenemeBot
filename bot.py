from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = "8674149760:AAEVp4BRF0q12IMrFnOVRWDWAp5W5r4zN1k"
GROQ_API_KEY = "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"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif! Sor bakalım.")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": text}], "max_tokens": 500},
            timeout=15
        )
        answer = r.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    except:
        await update.message.reply_text("Bir hata oldu, tekrar dene.")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("✅ Basit bot çalışıyor...")
    app.run_polling()
