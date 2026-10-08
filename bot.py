import openai, base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8941934368:AAG30A-UwVp2EwAbCa2yxpaaAjrToae1ooQ"
AGENTROUTER_KEY = "sk-ysrWVAximFX9qKCV8rB0mLB7oRxl6FgV5W3qffAjeF0HK9Wh"
BASE_URL = "https://agentrouter.org/v1"

client = openai.OpenAI(api_key=AGENTROUTER_KEY, base_url=BASE_URL)

async def start(update, context):
    await update.message.reply_text("مرحبا! ابعث تصويرة 📸")

async def handle_photo(update, context):
    await update.message.reply_text("⏳...")
    p = update.message.photo[-1]
    f = await context.bot.get_file(p.file_id)
    b = await f.download_as_bytearray()
    b64 = base64.b64encode(b).decode('utf-8')
    r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":[{"type":"text","text":"Give TITLE, DESCRIPTION, 45 KEYWORDS for Shutterstock"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}])
    await update.message.reply_text(r.choices[0].message.content)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
