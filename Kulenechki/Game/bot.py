import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

REQUIRED_MARKERS = 5
MAX_TENEHOD_POSITION = 5

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.user_data['character'] = None
    context.user_data['location'] = 'Пушнор'
    context.user_data['markers'] = 0
    context.user_data['tenehod_position'] = 0
    keyboard = [
        [InlineKeyboardButton('Лумик', callback_data='Лумик')],
        [InlineKeyboardButton('Флаффи', callback_data='Флаффи')],
        [InlineKeyboardButton('Тинори', callback_data='Тинори')],
        [InlineKeyboardButton('Ириска', callback_data='Ириска')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Привет, {user.first_name}! Выберите своего Куленёчка:", reply_markup=reply_markup)

def choose_character(update: Update, context: CallbackContext):
    query = update.callback_query
    character = query.data
    context.user_data['character'] = character
    query.edit_message_text(text=f"Вы выбрали {character}! Приключение начинается!")
    show_main_menu(query, context)

def show_main_menu(update_or_query, context):
    keyboard = [
        [InlineKeyboardButton('/move - переместиться на другую локацию', callback_data='move')],
        [InlineKeyboardButton("/search - искать маркеры 'Света Дружбы'", callback_data='search')],
        [InlineKeyboardButton('/status - показать текущий статус', callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if isinstance(update_or_query, Update):
        update_or_query.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    else:
        update_or_query.message.reply_text("Выберите действие:", reply_markup=reply_markup)

def main_menu_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    action = query.data
    if action == 'move':
        choose_location(query, context)
    elif action == 'search':
        search(query, context)
    elif action == 'status':
        status(query, context)

def choose_location(query, context):
    current_location = context.user_data.get('location', 'Пушнор')
    locations = {
        'Пушнор': ['Светящаяся поляна', 'Туманная роща'],
        'Светящаяся поляна': ['Пушнор', 'Ручей Забытых Снов'],
        'Туманная роща': ['Пушнор'],
        'Ручей Забытых Снов': ['Светящаяся поляна']
    }
    available_locations = locations.get(current_location, [])
    if available_locations:
        keyboard = [[InlineKeyboardButton(loc, callback_data=f'location_{loc}')] for loc in available_locations]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Куда вы хотите переместиться?", reply_markup=reply_markup)
    else:
        query.edit_message_text("Нет доступных локаций для перемещения.")
        show_main_menu(query, context)

def location_chosen(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data.startswith('location_'):
        new_location = data.replace('location_', '')
        context.user_data['location'] = new_location
        query.edit_message_text(f"Вы переместились в {new_location}.")
        show_main_menu(query, context)

def search(query, context):
    import random
    events = ['positive', 'negative', 'special']
    event = random.choice(events)
    if event == 'positive':
        context.user_data['markers'] = context.user_data.get('markers', 0) + 1
        query.edit_message_text("Вы нашли маркер 'Света Дружбы'!")
        check_victory_condition(query, context)
    elif event == 'negative':
        advance_tenehod(query, context)
    else:
        query.edit_message_text("Вы встретили лесное существо, которое предлагает вам помощь.")
        show_main_menu(query, context)

def advance_tenehod(query, context):
    tenehod_position = context.user_data.get('tenehod_position', 0) + 1
    context.user_data['tenehod_position'] = tenehod_position
    if tenehod_position >= MAX_TENEHOD_POSITION:
        query.edit_message_text("Тенеход достиг дерева Луми. Игра окончена. Вы проиграли.")
    else:
        query.edit_message_text(f"Тенеход продвинулся! Текущее положение: {tenehod_position}")
        show_main_menu(query, context)

def check_victory_condition(query, context):
    markers = context.user_data.get('markers', 0)
    if markers >= REQUIRED_MARKERS:
        query.edit_message_text("Поздравляем! Вы собрали достаточное количество маркеров и спасли лес!")
    else:
        show_main_menu(query, context)

def status(query, context):
    character = context.user_data.get('character', 'Не выбран')
    location = context.user_data.get('location', 'Неизвестно')
    markers = context.user_data.get('markers', 0)
    tenehod_position = context.user_data.get('tenehod_position', 0)
    status_message = (
        f"Персонаж: {character}\n"
        f"Локация: {location}\n"
        f"Маркеры 'Света Дружбы': {markers}\n"
        f"Позиция Тенехода: {tenehod_position}"
    )
    query.edit_message_text(status_message)
    show_main_menu(query, context)

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать игру\n"
        "/help - помощь"
    )

def main():
    token = '7314783664:AAEkBebeoJUKZFwcTsFP_rVt6resccsdYWs'
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CallbackQueryHandler(choose_character, pattern='^(Лумик|Флаффи|Тинори|Ириска)$'))
    dp.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^(move|search|status)$'))
    dp.add_handler(CallbackQueryHandler(location_chosen, pattern='^location_'))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
