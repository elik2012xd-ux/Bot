import telebot
import os
import time

# ──────────────────────────────────────────────────────────────
# ВАШИ ДАННЫЕ (обязательно замените, если нужно)
BOT_TOKEN = "8365918250:AAF4uKzE_T6886xS_A8YrqXtA9S6UEigvw4"
ADMIN_ID = 7469181511
# ──────────────────────────────────────────────────────────────

bot = telebot.TeleBot(BOT_TOKEN)

def create_game_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        one_time_keyboard=False
    )
    games = [
        "CS2", "Valorant", "Fortnite", "Apex Legends",
        "Roblox", "Minecraft", "GTA V", "Rust",
        "Escape from Tarkov", "The Finals", "War Thunder", "Другая"
    ]
    for i in range(0, len(games), 2):
        if i + 1 < len(games):
            markup.add(games[i], games[i+1])
        else:
            markup.add(games[i])
    return markup

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        "Выберите игру, для которой нужен скрипт:",
        reply_markup=create_game_keyboard()
    )

@bot.message_handler(content_types=['text'])
def handle_selection(message):
    game = message.text.strip()
    
    report = (
        f"НОВАЯ ЗАЯВКА\n"
        f"Пользователь: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
        f"@{message.from_user.username or 'нет'}\n"
        f"ID: {message.from_user.id}\n"
        f"Игра: {game}\n"
        f"Время: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
    )
    
    try:
        bot.send_message(ADMIN_ID, report)
        bot.reply_to(message, "Заявка отправлена. Ожидайте ответа.")
    except Exception as e:
        bot.reply_to(message, "Ошибка отправки. Попробуйте позже.")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    print("Бот стартовал на Render.com")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=30)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(10)
