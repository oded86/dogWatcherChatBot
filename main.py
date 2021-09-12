import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

my_token = "1953999006:AAE8WR6973394HivMDgw7sY1dkZI0hyrZCE"
updater = Updater(token=my_token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="עיריית ראשון לציון שלום, אנא העלה את התמונה של המפגע")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="הפקודה שנשלחה לא קיימת במערכת. אנא נסה שנית")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


def photo(update, context):
    file_id = update.message.photo[-1]
    new_file = context.bot.getFile(file_id)
    new_file.download('images/'+str(file_id.file_unique_id)+'.jpg')
    context.bot.sendMessage(chat_id=update.message.chat_id, text="קיבלנו את תמונת המפגע והעברנו אותה לטיפול, להתראות")
    start(update, context)


photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)

updater.start_polling()
