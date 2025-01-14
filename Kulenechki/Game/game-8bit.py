import pygame
import random

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Приключения Куленёчков")

clock = pygame.time.Clock()

# Загрузка изображений
player_img = pygame.Surface((40, 40))
player_img.fill((0, 255, 0))

dice_button_img = pygame.Surface((100, 50))
dice_button_img.fill((200, 200, 200))

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
    "Пушнор": (400, 300),
    "Светящаяся поляна": (200, 200),
    "Туманная роща": (600, 200),
    "Магический водопад": (100, 100),
    "Таинственная пещера": (700, 100),
    "Поле светлячков": (400, 100),
    "Ручей Забытых Снов": (200, 400),
    "Волшебный холм": (600, 400),
    "Долина ветров": (100, 500),
    "Забытая роща": (700, 500),
    "Озеро отражений": (400, 500),
    "Солнечная тропа": (300, 300),
    "Лунный камень": (500, 300),
    "Древо Луми": (400, 50)
}

# Игрок
player = {
    "location": "Пушнор",
    "markers": 0,
    "energy": 3,
    "special_items": [],
    "character": "Лумик"
}

# Кубик
dice_symbols = [
    "Движение",
    "Поиск",
    "Взаимодействие",
    "Особое действие",
    "Движение",
    "Поиск",
    "Взаимодействие",
    "Особое действие",
    "Движение",
    "Поиск",
    "Взаимодействие",
    "Особое действие",
    "Движение",
    "Поиск"
]

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

# Кнопки
dice_button_rect = pygame.Rect(350, 520, 100, 50)

# Функции
def draw_map():
    for loc, pos in location_positions.items():
        pygame.draw.circle(screen, (100, 100, 255), pos, 20)
        font = pygame.font.SysFont(None, 24)
        text = font.render(loc, True, BLACK)
        screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - 40))

def draw_player():
    pos = location_positions[player["location"]]
    screen.blit(player_img, (pos[0] - 20, pos[1] - 20))

def draw_ui():
    pygame.draw.rect(screen, (200, 200, 200), dice_button_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render("Бросить кубик", True, BLACK)
    screen.blit(text, (dice_button_rect.x + 10, dice_button_rect.y + 15))
    status_text = f"Локация: {player['location']}  Маркеры: {player['markers']}  Энергия: {player['energy']}"
    status = font.render(status_text, True, BLACK)
    screen.blit(status, (10, 10))
    if dice_rolled:
        action_text = f"Выпало действие: {current_action}"
        action = font.render(action_text, True, BLACK)
        screen.blit(action, (10, 40))

def handle_dice_roll():
    global dice_rolled, current_action
    current_action = random.choice(dice_symbols)
    dice_rolled = True
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
        player["location"] = random.choice(neighbors)

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
        if message == "Вы нашли маркер 'Света Дружбы'!":
            player["markers"] += 1
        elif message == "Вы получили дополнительную энергию!":
            player["energy"] += 1
        elif message == "Вы нашли волшебный артефакт!":
            player["special_items"].append("Артефакт")
    elif event == "negative":
        message = random.choice(negative_events)
        if message == "Тенеход продвинулся ближе к дереву Луми!":
            pass
        elif message == "Вы потеряли маркер!":
            if player["markers"] > 0:
                player["markers"] -= 1
        elif message == "Вы пропускаете ход!":
            pass
    elif event == "special":
        message = random.choice(special_events)
    font = pygame.font.SysFont(None, 24)
    event_text = font.render(message, True, BLACK)
    screen.blit(event_text, (10, 70))

def interact():
    pass

def use_ability():
    pass

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    draw_map()
    draw_player()
    draw_ui()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dice_button_rect.collidepoint(event.pos):
                handle_dice_roll()
    pygame.display.flip()

pygame.quit()
