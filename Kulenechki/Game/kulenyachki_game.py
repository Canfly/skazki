import pygame
import random
import sys

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Куленёчки (Skazki Canfly)")

clock = pygame.time.Clock()

# Загрузка изображений
logo_img = pygame.image.load("images/logo.png").convert_alpha()
background_img = pygame.image.load("images/background.png").convert()
character_sprites = {
    "Лумик": pygame.image.load("images/lumik.png").convert_alpha(),
    "Флаффи": pygame.image.load("images/flaffi.png").convert_alpha(),
    "Тинори": pygame.image.load("images/tinori.png").convert_alpha(),
    "Ириска": pygame.image.load("images/iriska.png").convert_alpha()
}
tenehod_img = pygame.image.load("images/tenehod.png").convert_alpha()
dice_imgs = [pygame.image.load(f"images/dice_{i}.png").convert_alpha() for i in range(1, 7)]

# Персонажи
characters = ["Лумик", "Флаффи", "Тинори", "Ириска"]
character_index = 0

# Игрок
player = {
    "location": "Пушнор",
    "markers": 0,
    "energy": 3,
    "special_items": [],
    "character": characters[character_index],
    "sprite": character_sprites[characters[character_index]]
}

# Тенеход
tenehod_position = 0

# Кубик
dice_symbols = [
    "Движение",
    "Поиск",
    "Взаимодействие",
    "Особое действие",
    "Движение",
    "Поиск"
]

# Локации
locations = [
    "Пушнор",
    "Светящаяся поляна",
    "Туманная роща",
    "Магический водопад",
    "Таинственная пещера",
    "Поле светлячков",
    "Ручей Забытых Снов",
    "Волшебный холм",
    "Долина ветров",
    "Забытая роща",
    "Озеро отражений",
    "Солнечная тропа",
    "Лунный камень",
    "Древо Луми"
]

# Позиции локаций на карте
location_positions = {
    "Пушнор": (500, 300),
    "Светящаяся поляна": (300, 200),
    "Туманная роща": (700, 200),
    "Магический водопад": (200, 100),
    "Таинственная пещера": (800, 100),
    "Поле светлячков": (500, 100),
    "Ручей Забытых Снов": (300, 400),
    "Волшебный холм": (700, 400),
    "Долина ветров": (200, 500),
    "Забытая роща": (800, 500),
    "Озеро отражений": (500, 500),
    "Солнечная тропа": (400, 300),
    "Лунный камень": (600, 300),
    "Древо Луми": (500, 50)
}

# Карты событий
positive_events = [
    "Вы нашли маркер 'Света Дружбы'!",
    "Вы получили дополнительную энергию!",
    "Вы нашли волшебный артефакт!"
]

negative_events = [
    "Тенеход продвинулся ближе к дереву Луми!",
    "Вы потеряли маркер!",
    "Вы пропускаете ход!"
]

special_events = [
    "Вы встретили Ежиона, он предлагает вам помощь.",
    "Вы нашли загадочный свиток.",
    "Вы попали в ловушку Тенехода!"
]

# Флаги
dice_rolled = False
current_action = ""
move_log = []

# Кнопки
dice_button_rect = pygame.Rect(650, 520, 130, 50)

# Состояния игры
STATE_INTRO = 0
STATE_GAME = 1
game_state = STATE_INTRO

def draw_intro():
    screen.fill(BLACK)
    screen.blit(logo_img, (0, 0))
    font = pygame.font.Font("fonts/alagard.ttf", 30)
    # Отображение персонажей для выбора
    for i, char in enumerate(characters):
        if i == character_index:
            color = (255, 0, 0)
        else:
            color = WHITE
        char_text = font.render(char, True, color)
        screen.blit(char_text, (WIDTH//2 - char_text.get_width()//2, 300 + i * 40))
    # Инструкции
    instruction_text = font.render("Выберите персонажа и нажмите Enter", True, WHITE)
    screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, 500))

def draw_map():
    screen.blit(background_img, (200, 0))
    for loc, pos in location_positions.items():
        # Отображение локаций
        pygame.draw.circle(screen, (255, 255, 255), pos, 20)
        font = pygame.font.Font("fonts/alagard.ttf", 18)
        text = font.render(loc, True, BLACK)
        screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - 40))

def draw_player():
    pos = location_positions[player["location"]]
    sprite = player["sprite"]
    screen.blit(sprite, (pos[0] - sprite.get_width() // 2, pos[1] - sprite.get_height() // 2))

def draw_tenehod():
    if tenehod_position < len(locations):
        loc = locations[tenehod_position]
        pos = location_positions[loc]
        screen.blit(tenehod_img, (pos[0] - tenehod_img.get_width() // 2, pos[1] - tenehod_img.get_height() // 2))

def draw_ui():
    # Левая панель для отображения ходов
    panel = pygame.Surface((200, HEIGHT), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 150))
    screen.blit(panel, (0, 0))
    font = pygame.font.Font("fonts/alagard.ttf", 16)
    # Отображение списка ходов
    y_offset = 10
    for log in move_log[-20:]:
        log_text = font.render(log, True, WHITE)
        screen.blit(log_text, (10, y_offset))
        y_offset += 20
    # Кнопка "Бросить кубик"
    pygame.draw.rect(screen, (200, 200, 200), dice_button_rect)
    text = font.render("Бросить кубик", True, BLACK)
    screen.blit(text, (dice_button_rect.x + 10, dice_button_rect.y + 15))
    # Статус игрока
    status_text = f"Локация: {player['location']}  Маркеры: {player['markers']}  Энергия: {player['energy']}"
    status = font.render(status_text, True, WHITE)
    screen.blit(status, (210, 10))
    # Последнее действие
    if dice_rolled:
        action_text = f"Выпало действие: {current_action}"
        action = font.render(action_text, True, WHITE)
        screen.blit(action, (210, 40))

def handle_dice_roll():
    global dice_rolled, current_action
    dice_roll = random.randint(1, 6)
    current_action = dice_symbols[dice_roll % len(dice_symbols)]
    dice_rolled = True
    move_log.append(f"Брошен кубик: {current_action}")
    if current_action == "Движение":
        move_player()
    elif current_action == "Поиск":
        search_event()
    elif current_action == "Взаимодействие":
        interact()
    elif current_action == "Особое действие":
        use_ability()

def move_player():
    neighbors = get_neighbors(player["location"])
    if neighbors:
        new_location = random.choice(neighbors)
        player["location"] = new_location
        move_log.append(f"Перемещение в {new_location}")

def get_neighbors(location):
    connections = {
        "Пушнор": ["Светящаяся поляна", "Туманная роща", "Солнечная тропа", "Лунный камень"],
        "Светящаяся поляна": ["Пушнор", "Магический водопад", "Ручей Забытых Снов"],
        "Туманная роща": ["Пушнор", "Таинственная пещера", "Волшебный холм"],
        "Магический водопад": ["Светящаяся поляна"],
        "Таинственная пещера": ["Туманная роща"],
        "Поле светлячков": ["Ручей Забытых Снов"],
        "Ручей Забытых Снов": ["Светящаяся поляна", "Поле светлячков", "Долина ветров"],
        "Волшебный холм": ["Туманная роща", "Забытая роща"],
        "Долина ветров": ["Ручей Забытых Снов"],
        "Забытая роща": ["Волшебный холм"],
        "Озеро отражений": ["Солнечная тропа"],
        "Солнечная тропа": ["Пушнор", "Озеро отражений"],
        "Лунный камень": ["Пушнор"],
        "Древо Луми": []
    }
    return connections.get(location, [])

def search_event():
    event = random.choice(["positive", "negative", "special"])
    if event == "positive":
        message = random.choice(positive_events)
        move_log.append(f"Событие: {message}")
        if message == "Вы нашли маркер 'Света Дружбы'!":
            player["markers"] += 1
        elif message == "Вы получили дополнительную энергию!":
            player["energy"] += 1
        elif message == "Вы нашли волшебный артефакт!":
            player["special_items"].append("Артефакт")
    elif event == "negative":
        message = random.choice(negative_events)
        move_log.append(f"Событие: {message}")
        if message == "Тенеход продвинулся ближе к дереву Луми!":
            advance_tenehod()
        elif message == "Вы потеряли маркер!":
            if player["markers"] > 0:
                player["markers"] -= 1
        elif message == "Вы пропускаете ход!":
            pass
    elif event == "special":
        message = random.choice(special_events)
        move_log.append(f"Событие: {message}")

def advance_tenehod():
    global tenehod_position
    if tenehod_position < len(locations) - 1:
        tenehod_position += 1
        move_log.append(f"Тенеход продвинулся в {locations[tenehod_position]}")
    else:
        move_log.append("Тенеход достиг Древа Луми! Игра окончена.")
        game_over()

def interact():
    move_log.append("Вы взаимодействуете с окружающим миром.")

def use_ability():
    if player["energy"] <= 0:
        move_log.append("Недостаточно энергии для использования способности.")
        return
    player["energy"] -= 1
    if player["character"] == "Лумик":
        move_player()
        move_player()
        move_log.append("Лумик перемещается на две локации!")
    elif player["character"] == "Флаффи":
        handle_dice_roll()
        move_log.append("Флаффи повторяет бросок кубика!")
    elif player["character"] == "Тинори":
        next_action = random.choice(dice_symbols)
        move_log.append(f"Тинори предсказывает следующее действие: {next_action}")
    elif player["character"] == "Ириска":
        move_log.append("Ириска превращает негативное событие в позитивное!")

def game_over():
    move_log.append("Игра окончена.")
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

running = True
while running:
    clock.tick(FPS)
    if game_state == STATE_INTRO:
        draw_intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    character_index = (character_index - 1) % len(characters)
                    player["character"] = characters[character_index]
                    player["sprite"] = character_sprites[characters[character_index]]
                elif event.key == pygame.K_DOWN:
                    character_index = (character_index + 1) % len(characters)
                    player["character"] = characters[character_index]
                    player["sprite"] = character_sprites[characters[character_index]]
                elif event.key == pygame.K_RETURN:
                    game_state = STATE_GAME
    elif game_state == STATE_GAME:
        screen.fill(WHITE)
        draw_map()
        draw_player()
        draw_tenehod()
        draw_ui()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dice_button_rect.collidepoint(event.pos):
                    handle_dice_roll()
        pygame.display.flip()
    pygame.display.flip()

pygame.quit()
