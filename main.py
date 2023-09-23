# -*- coding: utf-8 -*-
import telebot
from telebot import types
import requests
from io import BytesIO

# Замените 'YOUR_BOT_TOKEN' на ваш токен
TOKEN = '6698019340:AAF7388yf84RY-Dk_xNHz5K1GUODA-buboo'

# Создаем экземпляр telebot
bot = telebot.TeleBot(TOKEN)

# Словарь для отслеживания состояний пользователей
user_states = {}

# Словарь с информацией о тарифах
tariffs = {
    '\U0001F308Mинu пак\U0001F496': {
        'цена': '199₽ ',
        'срок действия': '30 дней',
        'описание': 'Данный пак подойдёт тем, кто посетил нас впервые, содержит лишь малую часть всех паков\U0001F970',
    },
    '\U0001F349ɯᴋ0ᴧьHицы\U0001F4A6': {
        'цена': '399₽ ',
        'срок действия': '30 дней',
        'описание': ' \U0001F919зᴀᴨᴩᴇщᴇнныᴇ ᴨоᴩно ʙидᴇо ᴄ дᴀᴩᴋнᴇᴛᴀ ᴄо ɯᴋодницᴀʍи \U0001F919ᴋᴀчᴇᴄᴛʙᴇнный ᴋонᴛᴇнᴛ из ᴄᴀʍоᴦо дᴀᴩᴋнᴇᴛᴀ! \U0001F919доᴄᴛуᴨ ᴋ 9700 ʙидᴇо, обноʙᴧᴇниᴇ ᴩᴀз ʙ ᴛᴩи дня, ᴨᴩи ᴨоᴋуᴨᴋᴇ дᴀнноᴦо ᴛᴀᴩиɸᴀ ʙы ᴨоᴧучᴀᴇᴛᴇ: \U00002705 зᴀᴋᴩыᴛый ᴋᴀнᴀᴧ дᴧя ᴋᴧиᴇнᴛоʙ \U00002705 ᴩᴇзᴇᴩʙныᴇ ᴦᴩуᴨᴨы нᴀ ᴄᴧучᴀй бᴧоᴋиᴩоʙᴋи \U00002705 нᴇобходиʍыᴇ инᴄᴛᴩуᴋции, ᴨᴩоʍоᴀᴋции и ᴛ.д\U0001F308',
    },
    '\U0001F48Bmалышku\U0001F525': {
        'цена': '499₽ ',
        'срок действия': '90 дней',
        'описание': 'Данный пак содержит в себе множество увлекательного контента <16\U0001F9C1\U0001F36D Такой контент точно не оставит никого равнодушным\U0001F33A Получаете доступ в приватную группу\U00002705 Обновление контента раз в три дня\U00002705 Поддержка с 08 до 22 по МСК\U00002705',
    },
    '\U0001F351ᴧuɯᴇниᴇ ʍ@ᴧоᴧᴇᴛоᴋ\U0001F308': {
        'цена': '499',
        'срок действия': '120 дней',
        'описание': ' \U0001F34Cдоᴄᴛʏᴨ ʙ ᴋ`ᴀнᴀᴧ ᴄ 1 918 ʙиᴅᴇо и 73ᴏ ɸᴏᴛ0 3ᴀᴨᴘᴇщᴇʜн0ᴦᴏ ᴋ0нᴛᴇнᴛᴀ ᴄᴀʍых ʍᴀʟᴇʜьᴋиx ᴅᴇᴛᴇй ʙо3ᴘᴀᴄᴛ0ʍ ᴅо 6ᴊʟᴇᴛ...жжжᴇᴄᴛь, ᴋ0нᴛᴇнᴛ ᴄобᴩᴀн зᴀ ʙᴄᴇ ʙᴩᴇʍя, и ноʙый и ᴄᴛᴀᴩый и ᴄо ʙᴄᴇх ᴛᴇᴧᴇᴦᴩᴀᴍʍ ᴋᴀнᴀᴧ0ʙ ᴨᴩодᴀющих иʍᴇнно ϶ᴛ0ᴛ ᴩᴀ3дᴇᴧ ᴄ ᴄᴀʍыʍи ʍᴀᴧᴇʜьᴋиʍᴜ \U0001F36D ',

    },
    '\U00002728VIP тариф ʙᴄᴇ ʙᴋᴧючᴇно\U00002728': {
        'цена': '799₽ ',
        'срок действия': '120 дней',
        'описание': 'изнᴀᴄиᴧоʙᴀниᴇ, ᴧиɯᴇниᴇ ʍᴀᴧоᴧᴇᴛоᴋ, ɯᴋоᴧьницы, ᴨоᴧнᴀя ᴋонɸидᴇнциᴀᴧьноᴄᴛь, ᴦᴀᴩᴀнᴛия нᴀ ʙозʙᴩᴀᴛ ᴄᴩᴇдᴄᴛʙ 15 ʍинуᴛ ᴄ ʍоʍᴇнᴛᴀ ᴨоᴋуᴨᴋи, круглосуточная поддержка VIP клиентов, фулл паки, полные отборного контента, отобранного и проверенного нами лично\U0001F496 ',
    },
}


# Клавиатура для главного меню
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
tech_support_button = types.KeyboardButton('Техподдержка')
my_subscription_button = types.KeyboardButton('Моя подписка')
tariffs_button = types.KeyboardButton('\U0001F36DТарифы\U0001F525')
proofs_button = types.KeyboardButton('Доказательства')
support_button = types.KeyboardButton('Поддержать проект\U0001F4B8')
keyboard.row(tech_support_button, my_subscription_button)
keyboard.row(tariffs_button, proofs_button, support_button)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.from_user

        bot.send_message(
            message.chat.id,
            f"Привет, {user.first_name}!\n\n\n"
            "ЕЙ ВСЕГО 15, А УЖЕ ДЕЛАЕТ ТАКОЕ 🥵Вечная гарантия! Круглосуточная поддержка! Сочнейший контент💦Такого ты не увидишь больше нигде 🔥💕Жми на «Тарифы» 💦👇🏻\n"
            "Потеря связи- Кликай \U0001F449 /start",

            reply_markup=keyboard
        )


        # Инициализируем стек состояний пользователя
        user_states[message.chat.id] = []
    except Exception as e:
        print("Ошибка в обработчике '/start':", str(e))


        # Инициализируем стек состояний пользователя
        user_states[message.chat.id] = []
    except Exception as e:
        print("Ошибка в обработчике '/start':", str(e))


# Обработчик "Поддержать проект"
@bot.message_handler(func=lambda message: message.text == "Поддержать проект\U0001F4B8", content_types=['text'])
def support_project(message):
    try:
        # Добавляем кнопку "Назад" только для поддержки проекта
        keyboard_support = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        back_button = types.KeyboardButton('Назад')
        keyboard_support.row(back_button)

        bot.send_message(
            message.chat.id,
            "Мы рады стараться для Вас\U00002764!Поддержите наш проект! Ваша поддержка- это покупка у нас тарифов! Нас ждут свежие обновления раз в 3 дня, мы рады стараться для вас! ",
            reply_markup=keyboard_support
        )

        # Добавляем состояние "Поддержка проекта"
        user_states[message.chat.id].append(support_project)
    except Exception as e:
        print("Ошибка в обработчике 'support_project':", str(e))


# Обработчик "Доказательства"
@bot.message_handler(func=lambda message: message.text == "Доказательства", content_types=['text'])
def proofs(message):
    try:
        user_states[message.chat.id].append(proofs)

        # Отправляем текст "Их нет"
        bot.send_message(
            message.chat.id,
            "Это лишь малая часть того, что мы можем Вам представить, скорее заходи во вкладку Тарифы и оформляй тот, который понравился\U0001F648 Лучший и отобранный контент! Никакого шлака, только годный материал \U0001F337"
        )

        # Отправляем фотографию по URL
        photo_url = "https://i.imgur.com/JP51iim.jpeg"  # Замените на реальный URL вашей фотографии
        try:
            response = requests.get(photo_url)
            if response.status_code == 200:
                photo_data = BytesIO(response.content)
                bot.send_photo(message.chat.id, photo_data)
            else:
                bot.send_message(message.chat.id, "Не удалось загрузить изображение")
        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))

        # Создаем клавиатуру для кнопки "Назад"
        keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        back_button = types.KeyboardButton('Назад')
        keyboard_back.add(back_button)

        bot.send_message(
            message.chat.id,
            "Вы можете вернуться в главное меню, нажав кнопку 'Назад'",
            reply_markup=keyboard_back
        )
        # Создаем клавиатуру для кнопки "Назад"
        keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        back_button = types.KeyboardButton('Назад')
        keyboard_back.add(back_button)
    except Exception as e:
        print("Ошибка в обработчике 'proofs':", str(e))
# Обработчик "Техподдержка"
@bot.message_handler(func=lambda message: message.text == "Техподдержка", content_types=['text'])
def tech_support(message):
    try:
        user_states[message.chat.id].append(tech_support)
        keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        back_button = types.KeyboardButton('Назад')
        keyboard_back.add(back_button)

        bot.send_message(
            message.chat.id,
            "Писать только по делу @xxc239 \n"
            "\U000026D4 \U000026D4 За СПАМ моментальный бан\U000026D4\U000026D4 ",
            reply_markup=keyboard_back
        )
    except Exception as e:
        print("Ошибка в обработчике 'tech_support':", str(e))
# Обработчик "Моя подписка"
@bot.message_handler(func=lambda message: message.text == "Моя подписка", content_types=['text'])
def my_subscription(message):
    user_states[message.chat.id].append(my_subscription)
    keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    back_button = types.KeyboardButton('Назад')
    keyboard_back.add(back_button)

    bot.send_message(
        message.chat.id,
        "У вас нет действующей подписки. Ознакомьтесь с тарифами нажав на соответствующую кнопку.",
        reply_markup=keyboard_back
    )

# Обработчик "Тарифы"
@bot.message_handler(func=lambda message: message.text == "\U0001F36DТарифы\U0001F525", content_types=['text'])
def view_tariffs(message):
    user_states[message.chat.id].append(view_tariffs)
    keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    back_button = types.KeyboardButton('Назад')
    keyboard_back.add(back_button)

    # Создаем клавиатуру с кнопками тарифов
    tariff_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for tariff_name in tariffs:
        tariff_buttons.add(types.KeyboardButton(tariff_name))

    bot.send_message(
        message.chat.id,
        "Выберите тариф из списка:",
        reply_markup=tariff_buttons
    )

# Обработчик выбора тарифа
@bot.message_handler(func=lambda message: message.text in tariffs.keys(), content_types=['text'])
def select_item(message):
    user_choice = message.text

    if user_choice == 'Назад':
        if user_states[message.chat.id]:
            user_states[message.chat.id].pop()
            if user_states[message.chat.id]:
                previous_state = user_states[message.chat.id][-1]
                if previous_state == tech_support:
                    tech_support(message)
                elif previous_state == my_subscription:
                    my_subscription(message)
                elif previous_state == view_tariffs:
                    view_tariffs(message)
            else:
                bot.send_message(
                    message.chat.id,
                    "Возврат в главное меню",
                    reply_markup=keyboard
                )
        return

    if user_choice in tariffs:
        # Сохраняем выбранный тариф в user_states
        user_states[message.chat.id].append(user_choice)
        tariff_info = tariffs[user_choice]
        message_text = f"Тариф: {user_choice}\nЦена: {tariff_info['цена']}\nСрок действия: {tariff_info['срок действия']}\nОписание: {tariff_info['описание']}"
        bot.send_message(message.chat.id, message_text)

        keyboard_payment = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        payment_button = types.KeyboardButton('Оплатить')
        back_button = types.KeyboardButton('Назад')
        keyboard_payment.row(payment_button, back_button)

        bot.send_message(
            message.chat.id,
            "Для оплаты нажмите кнопку 'Оплатить'",
            reply_markup=keyboard_payment
        )

        user_states[message.chat.id].append(select_item)
    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите тариф из списка или нажмите 'Назад'."
        )


# Обработчик "Оплатить"
@bot.message_handler(func=lambda message: message.text == "Оплатить", content_types=['text'])
def payment(message):
    try:
        user_choice = message.text
        if user_choice == 'Оплатить':
            # Получаем выбранный пользователем тариф
            selected_tariff = user_states[message.chat.id][-2]  # Предпоследний элемент стека - выбранный тариф
            requisites = "2204 3101 5149 1555"  # Ваши реквизиты

            bot.send_message(
                message.chat.id,
                f"Способ оплаты: Перевод на карту по \U00002757\U00002757\U00002757СБП\U00002757\U00002757\U00002757"
                f"\n\n"
                f"Для оплаты тарифа '{selected_tariff}' Пожалуйста выполните перевод на указанные реквизиты: {requisites}, отправьте скриншот перевода (не документ) и нажмите кнопку 'Я оплатил'"
            )



            # Добавляем кнопку "Я оплатил"
            keyboard_confirm_payment = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            confirm_payment_button = types.KeyboardButton('Я оплатил')
            back_button = types.KeyboardButton('Назад')
            keyboard_confirm_payment.row(confirm_payment_button, back_button)

            bot.send_message(
                message.chat.id,
                "После оплаты, нажмите кнопку 'Я оплатил'",
                reply_markup=keyboard_confirm_payment
            )


            user_states[message.chat.id].append(payment)
    except Exception as e:
        print("Ошибка в обработчике 'payment':", str(e))


# Обработчик "Я оплатил"
@bot.message_handler(func=lambda message: message.text == "Я оплатил", content_types=['text'])
def confirm_payment(message):
    try:


        # Добавляем кнопку "Главное меню"
        keyboard_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        main_menu_button = types.KeyboardButton('Главное меню')
        keyboard_main_menu.row(main_menu_button)

        bot.send_message(
            message.chat.id,
            "Выберите дальнейшее действие:",
            reply_markup=keyboard_main_menu
        )

        # Возвращение к главному меню
        if user_states[message.chat.id]:
            user_states[message.chat.id].pop()  # Удаляем состояние "confirm_payment"
    except Exception as e:
        print("Ошибка в обработчике 'confirm_payment':", str(e))



# Обработчик ожидания отправки квитанции
@bot.message_handler(content_types=['photo'])
def waiting_receipt(message):
    try:
        # Замените 'ADMIN_CHAT_ID' на реальный chat_id администратора
        admin_chat_id = '6406455642'

        # Отправляем фотографию администратору
        bot.send_photo(chat_id=admin_chat_id, photo=message.photo[-1].file_id)

        # Отправляем сообщение пользователю
        bot.send_message(
            message.chat.id,
            "Квитанция отправлена на проверку. Пожалуйста, ожидайте."
        )

        # Возвращение к предыдущему состоянию (кнопка "Я оплатил")
        if user_states[message.chat.id]:
            user_states[message.chat.id].pop()
    except Exception as e:
        print("Ошибка в обработчике 'waiting_receipt':", str(e))

# Обработчик кнопки "Главное меню"
@bot.message_handler(func=lambda message: message.text == 'Главное меню', content_types=['text'])
def main_menu(message):
    try:
        # Отправляем сообщение и клавиатуру главного меню
        bot.send_message(
            message.chat.id,
            "Выберите дальнейшее действие:",
            reply_markup=keyboard  # Используем клавиатуру главного меню
        )

        # Очищаем стек состояний пользователя
        user_states[message.chat.id] = []
    except Exception as e:
        print("Ошибка в обработчике 'main_menu':", str(e))

# Обработчик "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад", content_types=['text'])
def go_back(message):
    try:
        if user_states[message.chat.id]:
            user_states[message.chat.id].pop()
        bot.send_message(
            message.chat.id,
            "Возврат в главное меню",
            reply_markup=keyboard  # Обновляем клавиатуру на главное меню
        )
    except Exception as e:
        print("Ошибка в обработчике 'go_back':", str(e))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("Ошибка в основном цикле:", str(e))

