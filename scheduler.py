import asyncio
from db.database import get_all_users, get_messages_to_delete, clear_user_messages
from services.payment import is_payment_due, days_left
from aiogram import types

async def run_scheduler(bot):
    while True:
        for user_id, payment_dt in get_all_users():
            if is_payment_due(payment_dt):
                for chat_id, msg_id in get_messages_to_delete(user_id):
                    try:
                        await bot.delete_message(chat_id, msg_id)
                    except:
                        pass
                clear_user_messages(user_id)
            elif days_left(payment_dt) in [1, 2]:
                await bot.send_message(user_id, "To'lov vaqti yaqinlashmoqda, kechiktirmasligingizni so'raymiz.", reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[[types.InlineKeyboardButton(text="To'lov qilish", callback_data="pay")]]))
        await asyncio.sleep(86400)
