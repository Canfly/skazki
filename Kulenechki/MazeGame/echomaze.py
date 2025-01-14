import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размер экрана
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 160
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Название окна
pygame.display.set_caption("Echo Maze")

# Частота кадров
clock = pygame.time.Clock()
FPS = 30

# Загрузка смайлика
font = pygame.font.SysFont('Arial', 20)
player_img = font.render('😊', True, (255, 255, 255))
player_rect = player_img.get_rect()

# Размер клетки
CELL_SIZE = 10

# Размер лабиринта
maze_width = 50
maze_height = 50

def generate_maze():
    maze = []
    for y in range(maze_height):
        row = []
        for x in range(maze_width):
            if random.random() < 0.2:
                row.append(1)  # Стена
            else:
                row.append(0)  # Пустое пространство
        maze.append(row)

    # Границы лабиринта
    for x in range(maze_width):
        maze[0][x] = 1
        maze[maze_height - 1][x] = 1
    for y in range(maze_height):
        maze[y][0] = 1
        maze[y][maze_width - 1] = 1

    return maze

# Генерация первого лабиринта
maze = generate_maze()

# Видимость (False - темнота, True - видимо)
visibility = [[False for _ in range(maze_width)] for _ in range(maze_height)]

# Позиция игрока (в клетках)
player_cell_x = 1
player_cell_y = 1

# Установка игрока в стартовую позицию
player_rect.x = player_cell_x * CELL_SIZE
player_rect.y = player_cell_y * CELL_SIZE

# Размещение монетки (цели)
def place_coin():
    while True:
        coin_x = random.randint(1, maze_width - 2)
        coin_y = random.randint(1, maze_height - 2)
        if maze[coin_y][coin_x] == 0 and (coin_x != player_cell_x or coin_y != player_cell_y):
            return coin_x, coin_y

coin_cell_x, coin_cell_y = place_coin()
coin_img = font.render('💰', True, (255, 215, 0))
coin_rect = coin_img.get_rect()
coin_rect.x = coin_cell_x * CELL_SIZE
coin_rect.y = coin_cell_y * CELL_SIZE

# Звук
try:
    echo_sound = pygame.mixer.Sound('echo.wav')
except pygame.error:
    echo_sound = None

# Функция отображения лабиринта
def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            if visibility[y][x]:
                rect = pygame.Rect(x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE)
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                else:
                    pygame.draw.rect(screen, (50, 50, 50), rect)

# Камера
camera_x = 0
camera_y = 0

# Главный цикл игры
running = True
while running:
    screen.fill((0, 0, 0))  # Очистка экрана

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Сохранение текущей позиции
    old_cell_x = player_cell_x
    old_cell_y = player_cell_y

    # Движение игрока
    if keys[pygame.K_LEFT]:
        if maze[player_cell_y][player_cell_x - 1] == 0:
            player_cell_x -= 1
    if keys[pygame.K_RIGHT]:
        if maze[player_cell_y][player_cell_x + 1] == 0:
            player_cell_x += 1
    if keys[pygame.K_UP]:
        if maze[player_cell_y - 1][player_cell_x] == 0:
            player_cell_y -= 1
    if keys[pygame.K_DOWN]:
        if maze[player_cell_y + 1][player_cell_x] == 0:
            player_cell_y += 1

    # Обновление позиции игрока
    player_rect.x = player_cell_x * CELL_SIZE - camera_x
    player_rect.y = player_cell_y * CELL_SIZE - camera_y

    # Эхолокация при нажатии пробела
    if keys[pygame.K_SPACE]:
        # Воспроизведение звука
        if echo_sound:
            echo_sound.play()

        # Определение видимости клеток вокруг игрока
        for y in range(-5, 6):
            for x in range(-5, 6):
                cell_x = player_cell_x + x
                cell_y = player_cell_y + y
                if 0 <= cell_x < maze_width and 0 <= cell_y < maze_height:
                    visibility[cell_y][cell_x] = True

    # Обновление камеры
    camera_x = player_cell_x * CELL_SIZE - SCREEN_WIDTH // 2 + CELL_SIZE // 2
    camera_y = player_cell_y * CELL_SIZE - SCREEN_HEIGHT // 2 + CELL_SIZE // 2

    # Проверка на сбор монетки
    if player_cell_x == coin_cell_x and player_cell_y == coin_cell_y:
        # Переход на следующий уровень
        maze = generate_maze()
        visibility = [[False for _ in range(maze_width)] for _ in range(maze_height)]
        player_cell_x, player_cell_y = 1, 1
        coin_cell_x, coin_cell_y = place_coin()
        coin_rect.x = coin_cell_x * CELL_SIZE
        coin_rect.y = coin_cell_y * CELL_SIZE

    # Отображение лабиринта
    draw_maze()

    # Отображение монетки, если она в видимой области
    if visibility[coin_cell_y][coin_cell_x]:
        coin_rect.x = coin_cell_x * CELL_SIZE - camera_x
        coin_rect.y = coin_cell_y * CELL_SIZE - camera_y
        screen.blit(coin_img, (coin_rect.x, coin_rect.y))

    # Отображение игрока
    player_rect.x = player_cell_x * CELL_SIZE - camera_x
    player_rect.y = player_cell_y * CELL_SIZE - camera_y
    screen.blit(player_img, (player_rect.x, player_rect.y))

    pygame.display.flip()
    clock.tick(FPS)

