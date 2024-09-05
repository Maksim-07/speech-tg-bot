import telebot

from config import TOKEN
from test_func import text_to_voice

bot = telebot.TeleBot(TOKEN)

user_states = {"lang": "ru"}


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я умею озвучивать текст.")


@bot.message_handler(commands=["setlanguage"])
def set_language(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_1 = telebot.types.InlineKeyboardButton("Русский", callback_data="ru")
    button_2 = telebot.types.InlineKeyboardButton("Английский", callback_data="en")
    markup.add(button_1, button_2)
    bot.send_message(
        message.chat.id, text="Выберите язык для озвучки.", reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            match call.data:
                case "ru":
                    user_states["lang"] = "ru"
                case "en":
                    user_states["lang"] = "en"

            bot.send_message(call.message.chat.id, "Язык установлен!")
    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=["text"])
def echo(message):
    audio = text_to_voice(message.text, language=user_states["lang"])
    bot.send_audio(message.chat.id, audio=open(audio, "rb"))


bot.infinity_polling()
