from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token va guruh chat ID ni bu yerga kiriting
BOT_TOKEN = "7548365244:AAHqdD_-rpp9Zjkk3tnJ3-JdV1xC2cC0fr4"
GROUP_CHAT_ID = -1002117988914  # Bu siz bergan guruh: https://t.me/+DM_gnKXSTMViZGI6

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Москвадан Тошкентга", "Тошкентдан Москвага"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Салом, ҳурматли мижоз!\nҚаердан қаерга кетмоқчисиз?",
        reply_markup=reply_markup
    )

async def handle_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['direction'] = update.message.text
    contact_btn = KeyboardButton("Телефон рақам юбориш", request_contact=True)
    markup = ReplyKeyboardMarkup([[contact_btn]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Илтимос, телефон рақамингизни юборинг:", reply_markup=markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    direction = context.user_data.get('direction', 'Номаълум йўналиш')
    user = update.message.from_user
    msg_text = (
        f"Янги буюртма!\n"
        f"Фойдаланувчи: @{user.username or user.full_name}\n"
        f"Йўналиш: {direction}\n"
        f"Телефон рақам: {contact.phone_number}"
    )
    await update.message.reply_text("Буюртмангиз қабул қилинди! Ҳайдовчи сиз билан боғланади.")
    await context.bot.forward_message(chat_id=GROUP_CHAT_ID, from_chat_id=update.message.chat.id, message_id=update.message.message_id)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg_text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(Москвадан Тошкентга|Тошкентдан Москвага)$"), handle_direction))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
