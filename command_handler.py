import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import env

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="start!")

def init():
    application = ApplicationBuilder().token(env.get(env.EnvNames.TELEGRAM_TOKEN)).build()
    
    # TODO: telegram을 통한 명령, 조회 기능 추가
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()