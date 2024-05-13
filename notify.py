import telegram
import env

bot = telegram.Bot(env.get(env.EnvNames.TELEGRAM_TOKEN))

async def send_message(msg: str):
    await bot.send_message(chat_id=env.get(env.EnvNames.TELEGRAM_CHAT_ID), text=msg)