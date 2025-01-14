
const TelegramBot = require('node-telegram-bot-api');

// Замените 'YOUR_TELEGRAM_BOT_TOKEN' на токен вашего бота
const token = 'YOUR_TELEGRAM_BOT_TOKEN';

// Создаем бота
const bot = new TelegramBot(token, { polling: true });

// Константы для игры
const REQUIRED_MARKERS = 7;
const MAX_TENEHOD_POSITION = 5;

// Хранение данных пользователей в памяти
const users = {};

// Функция для отправки главного меню
function showMainMenu(chatId) {
  const options = {
    reply_markup: {
      inline_keyboard: [
        [{ text: '🚶‍♂️ Переместиться', callback_data: 'move' }],
        [{ text: '🔍 Искать маркеры', callback_data: 'search' }],
        [{ text: '🛠 Способность', callback_data: 'ability' }],
        [{ text: '📊 Статус', callback_data: 'status' }]
      ]
    }
  };
  bot.sendMessage(chatId, 'Выберите действие:', options);
}

// Обработчик команды /start
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;

  // Инициализируем данные пользователя
  users[userId] = {
    character: null,
    location: '🏡 Пушнор',
    markers: 0,
    tenehodPosition: 0,
    energy: 3,
    abilityUsed: false,
    specialItems: []
  };

  // Предлагаем выбрать персонажа
  const options = {
    reply_markup: {
      inline_keyboard: [
        [{ text: '🌟 Лумик', callback_data: 'character_Лумик' }],
        [{ text: '🎉 Флаффи', callback_data: 'character_Флаффи' }],
        [{ text: '🧠 Тинори', callback_data: 'character_Тинори' }],
        [{ text: '🌈 Ириска', callback_data: 'character_Ириска' }]
      ]
    }
  };

  bot.sendMessage(chatId, `Привет, ${msg.from.first_name}! Выберите своего Куленёчка:`, options);
});

// Обработчик нажатий на кнопки
bot.on('callback_query', (callbackQuery) => {
  const msg = callbackQuery.message;
  const data = callbackQuery.data;
  const userId = callbackQuery.from.id;
  const user = users[userId];

  if (!user) {
    bot.sendMessage(msg.chat.id, 'Пожалуйста, начните игру с команды /start.');
    return;
  }

  // Обработка выбора персонажа
  if (data.startsWith('character_')) {
    const character = data.replace('character_', '');
    user.character = character;
    bot.sendMessage(msg.chat.id, `Вы выбрали ${character}! Приключение начинается!`);
    showMainMenu(msg.chat.id);
  }

  // Обработка главного меню
  else if (data === 'move') {
    chooseLocation(msg.chat.id, user);
  } else if (data === 'search') {
    search(msg.chat.id, user);
  } else if (data === 'status') {
    showStatus(msg.chat.id, user);
  } else if (data === 'ability') {
    useAbility(msg.chat.id, user);
  }

  // Обработка выбора локации
  else if (data.startsWith('location_')) {
    const newLocation = data.replace('location_', '');
    user.location = newLocation;
    bot.sendMessage(msg.chat.id, `Вы переместились в ${newLocation}.`);
    showMainMenu(msg.chat.id);
  }
});

// Функция выбора локации
function chooseLocation(chatId, user) {
  const currentLocation = user.location;
  const locations = {
    '🏡 Пушнор': ['🌲 Светящаяся поляна', '🌫 Туманная роща'],
    '🌲 Светящаяся поляна': ['🏡 Пушнор', '🌊 Ручей Забытых Снов', '💧 Магический водопад'],
    '🌫 Туманная роща': ['🏡 Пушнор', '🕯 Таинственная пещера'],
    '💧 Магический водопад': ['🌲 Светящаяся поляна'],
    '🕯 Таинственная пещера': ['🌫 Туманная роща'],
    '🌊 Ручей Забытых Снов': ['🌲 Светящаяся поляна', '🦋 Поле светлячков'],
    '🦋 Поле светлячков': ['🌊 Ручей Забытых Снов']
  };
  const availableLocations = locations[currentLocation] || [];

  if (availableLocations.length > 0) {
    const keyboard = availableLocations.map(loc => [{ text: loc, callback_data: `location_${loc}` }]);
    const options = {
      reply_markup: {
        inline_keyboard: keyboard
      }
    };
    bot.sendMessage(chatId, 'Куда вы хотите переместиться?', options);
  } else {
    bot.sendMessage(chatId, 'Нет доступных локаций для перемещения.');
    showMainMenu(chatId);
  }
}

// Функция поиска маркеров
function search(chatId, user) {
  const events = ['positive', 'negative', 'special'];
  const event = events[Math.floor(Math.random() * events.length)];

  if (event === 'positive') {
    user.markers += 1;
    user.energy = Math.min(user.energy + 1, 3); // Восстанавливаем энергию
    bot.sendMessage(chatId, "🎉 Вы нашли маркер 'Света Дружбы' и восстановили 1 энергию!");
    checkVictoryCondition(chatId, user);
  } else if (event === 'negative') {
    advanceTenehod(chatId, user);
  } else {
    specialEvent(chatId, user);
  }
}

// Функция специальных событий
function specialEvent(chatId, user) {
  const specialEvents = ['hedgehog', 'trap', 'artifact'];
  const event = specialEvents[Math.floor(Math.random() * specialEvents.length)];

  if (event === 'hedgehog') {
    user.energy = Math.min(user.energy + 1, 3);
    bot.sendMessage(chatId, '🦔 Вы встретили Ежион! Он восстановил вашу энергию на 1 единицу.');
  } else if (event === 'trap') {
    user.tenehodPosition += 1;
    bot.sendMessage(chatId, '🕸 Вы попали в теневую ловушку! Тенеход продвинулся вперёд.');
  } else if (event === 'artifact') {
    user.specialItems.push('✨ Волшебный артефакт');
    bot.sendMessage(chatId, '✨ Вы нашли Волшебный артефакт! Теперь вы собираете на 1 маркер больше.');
  }
  showMainMenu(chatId);
}

// Функция использования способности
function useAbility(chatId, user) {
  if (user.energy <= 0) {
    bot.sendMessage(chatId, '⚠️ У вас недостаточно энергии для использования способности.');
    showMainMenu(chatId);
    return;
  }

  if (user.abilityUsed && user.character === '🌈 Ириска') {
    bot.sendMessage(chatId, '⚠️ Вы уже использовали свою способность.');
    showMainMenu(chatId);
    return;
  }

  user.energy -= 1;
  switch (user.character) {
    case 'Лумик':
      // Перемещение на две локации
      bot.sendMessage(chatId, '🌟 Вы можете переместиться на две локации за один ход!');
      // Логика перемещения на две локации
      chooseLocation(chatId, user);
      break;
    case 'Флаффи':
      // Повтор последнего действия
      bot.sendMessage(chatId, '🎉 Вы повторяете последнее действие!');
      // Логика повторения последнего действия
      search(chatId, user);
      break;
    case 'Тинори':
      // Просмотр следующего события
      const events = ['positive', 'negative', 'special'];
      const nextEvent = events[Math.floor(Math.random() * events.length)];
      bot.sendMessage(chatId, `🧠 Следующее событие при поиске будет: ${nextEvent}`);
      showMainMenu(chatId);
      break;
    case 'Ириска':
      if (!user.abilityUsed) {
        user.abilityUsed = true;
        user.markers += 1;
        bot.sendMessage(chatId, '🌈 Вы превратили негативное событие в позитивное и получили маркер!');
        checkVictoryCondition(chatId, user);
      } else {
        bot.sendMessage(chatId, '⚠️ Вы уже использовали свою способность.');
        showMainMenu(chatId);
      }
      break;
    default:
      bot.sendMessage(chatId, '⚠️ У вашего персонажа нет специальной способности.');
      showMainMenu(chatId);
      break;
  }
}

// Функция продвижения Тенехода
function advanceTenehod(chatId, user) {
  user.tenehodPosition += 1;
  if (user.tenehodPosition >= MAX_TENEHOD_POSITION) {
    bot.sendMessage(chatId, '🌑 Тенеход достиг дерева Луми. Игра окончена. Вы проиграли.');
  } else {
    bot.sendMessage(chatId, `🌑 Тенеход продвинулся! Текущее положение: ${user.tenehodPosition}`);
    showMainMenu(chatId);
  }
}

// Функция проверки условия победы
function checkVictoryCondition(chatId, user) {
  let totalMarkers = user.markers;
  if (user.specialItems.includes('✨ Волшебный артефакт')) {
    totalMarkers += 1; // Увеличиваем количество маркеров за счёт артефакта
  }
  if (totalMarkers >= REQUIRED_MARKERS) {
    bot.sendMessage(chatId, '🎉 Поздравляем! Вы собрали достаточное количество маркеров и спасли лес!');
  } else {
    showMainMenu(chatId);
  }
}

// Функция отображения статуса игрока
function showStatus(chatId, user) {
  const statusMessage = `
Персонаж: ${user.character}
Локация: ${user.location}
Маркеры 'Света Дружбы': ${user.markers}
Позиция Тенехода: ${user.tenehodPosition}
Энергия: ${user.energy}
Специальные предметы: ${user.specialItems.join(', ') || 'Нет'}
  `;
  bot.sendMessage(chatId, statusMessage);
  showMainMenu(chatId);
}

// Обработчик команды /help
bot.onText(/\/help/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Доступные команды:\n/start - начать игру\n/help - помощь');
});

// Установка команд бота
bot.setMyCommands([
  { command: '/start', description: 'Начать игру' },
  { command: '/help', description: 'Помощь по командам' }
]);


