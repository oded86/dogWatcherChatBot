import os
import logging
import exif
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

my_token = "1953999006:AAE8WR6973394HivMDgw7sY1dkZI0hyrZCE"
updater = Updater(token=my_token, use_context=True)
file_name = ""

dispatcher = updater.dispatcher
current_pos = {"lat": 0, "lon": 0}
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    message_text = "עיריית ראשון לציון שלום, אנא העלה את התמונה של המפגע"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    logging.info("Chat_id=" + str(update.effective_chat.id) + ", message=" + message_text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    logging.info("Chat_id=" + str(update.effective_chat.id) + ", message= Echo " + update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def unknown(update, context):
    message_text = "הפקודה שנשלחה לא קיימת במערכת. אנא נסה שנית"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    logging.info("Chat_id=" + str(update.effective_chat.id) + ", message=" + message_text)


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


def photo(update, context):
    global file_name
    file_id = update.message.photo[-1]
    file_name = str(file_id.file_unique_id) + '.jpg'
    new_file = context.bot.getFile(file_id)
    new_file.download(file_name)
    message_text = "קיבלנו את תמונת המפגע אנא שלח את מיקומך"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    logging.info("Chat_id=" + str(update.effective_chat.id) + ", message=" + message_text)


photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)


def location(update, context):
    global file_name
    message_text = "קיבלנו את תמונת המפגע והעברנו אותה לטיפול, להתראות"
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    current_pos["lat"] = message.location.latitude
    current_pos["lon"] = message.location.longitude
    exif.set_gps_location(file_name, current_pos["lat"], current_pos["lon"], 1)
    os.rename(file_name, "images/"+file_name)
    context.bot.sendMessage(chat_id=update.message.chat_id, text=message_text)
    logging.info("Chat_id=" + str(update.effective_chat.id) + "message=" + message_text)
    start(update, context)


location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

updater.start_polling()
