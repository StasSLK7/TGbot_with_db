from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN, MAX_TOKENS
from gpt import GPT
from database import DB
import logging

bot = TeleBot(TOKEN)
gpt = GPT()



# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
    filename="logs.txt"
)


# Функция для создания клавиатуры с нужными кнопочками
def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


# Приветственное сообщение /start
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Привет, {user_name}! Я бот-помощник для решения разных задач!\n"
                          f"Ты можешь прислать условие задачи, а я постараюсь её решить.\n"
                          "Иногда ответы получаются слишком длинными - в этом случае ты можешь попросить продолжить.",
                     reply_markup=create_keyboard(["/solve_task", '/help']))
    logging.info("Отправка приветственного сообщения")


# Команда /help
@bot.message_handler(commands=['help'])
def support(message):
    bot.send_message(message.from_user.id,
                     text="Чтобы приступить к решению задачи: нажми /solve_task, а затем напиши условие задачи",
                     reply_markup=create_keyboard(["/solve_task"]))
    logging.info("Отправка вспомогательного сообщения")


@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    bot.send_message(message.chat.id, "Напиши условие новой задачи:")
    bot.register_next_step_handler(message, get_promt)


def continue_filter(message):
    button_text = 'Продолжить решение'
    return message.text == button_text


@bot.message_handler(func=continue_filter)
def get_promt(message):
    user_id = message.from_user.id


    # Проверяем тип сообщения
    if message.content_type != "text":
        bot.send_message(user_id, "Необходимо отправить именно текстовое сообщение")
        bot.register_next_step_handler(message, get_promt)
        logging.info(f"Пользователь {user_id} отправил неверный тип сообщения")
        return

    # Вытаскиваем текст
    user_request = message.text

    # Проверяем количество токенов
    if gpt.count_tokens(user_request) > MAX_TOKENS:
        bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
        bot.register_next_step_handler(message, get_promt)
        return

    # проверяем наличие usera в БД
    if not DB.check_user(user_id):
        DB.create_user(user_id)  # создаем запись в БД, если user not found
        DB.update_user(user_id,
                       task=user_request,
                       level="Решим задачу по шагам: ",
                       current_subject="Ты - дружелюбный помощник для решения задач по математике. Давай подробный ответ с решением на русском языке",
                       )   # заполняем инфмормацию о пользователе


    # Формируем промт и отправляем его
    promt = gpt.make_promt(users_history[user_id])  # json
    resp = gpt.send_request(promt)

    # Обрабатываем ответ
    answer = gpt.process_resp(resp)


    # Дописываем
    if answer[0]:
        users_history[user_id]['assistant_content'] += answer[1]

    bot.send_message(user_id, text=users_history[user_id]['assistant_content'],
                     reply_markup=create_keyboard(["Продолжить решение", "Завершить решение"]))

    logging.info(f"Пользователь {user_id} успешно получил ответ от GPT")


# Завершаем решение
def end_filter(message):
    button_text = 'Завершить решение'
    return message.text == button_text


@bot.message_handler(content_types=['text'], func=end_filter)
def end_task(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Текущие решение завершено")
    users_history[user_id] = {}
    solve_task(message)


@bot.message_handler(commands=['debug'])
def send_debug(message):
    user_id = message.from_user.id
    with open("logs.txt", "rb") as f:
        bot.send_document(user_id, f)


bot.polling()
