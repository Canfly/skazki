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
player_img = pygame.font.SysFont('Arial', 20).render('😊', True, (255, 255, 255))
player_rect = player_img.get_rect()

# Позиция игрока
player_rect.x = SCREEN_WIDTH // 2
player_rect.y = SCREEN_HEIGHT - 30

# Создание лабиринта
maze = []
maze_width = 50
maze_height = 50
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

# Размер клетки
CELL_SIZE = 10

# Видимость (False - темнота, True - видимо)
visibility = [[False for _ in range(maze_width)] for _ in range(maze_height)]

# Звук
echo_sound = pygame.mixer.Sound('echo.wav')

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
while True:
    screen.fill((0, 0, 0))  # Очистка экрана

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Движение игрока
    if keys[pygame.K_LEFT]:
        player_rect.x -= 2
    if keys[pygame.K_RIGHT]:
        player_rect.x += 2
    if keys[pygame.K_UP]:
        player_rect.y -= 2
    if keys[pygame.K_DOWN]:
        player_rect.y += 2

    # Ограничение движения по границам экрана
    player_rect.x = max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, SCREEN_HEIGHT - player_rect.height))

    # Эхолокация при нажатии пробела
    if keys[pygame.K_SPACE]:
        # Воспроизведение звука
        echo_sound.play()

        # Определение видимости клеток вокруг игрока
        player_cell_x = (player_rect.x + camera_x) // CELL_SIZE
        player_cell_y = (player_rect.y + camera_y) // CELL_SIZE
        for y in range(-5, 6):
            for x in range(-5, 6):
                cell_x = player_cell_x + x
                cell_y = player_cell_y + y
                if 0 <= cell_x < maze_width and 0 <= cell_y < maze_height:
                    visibility[cell_y][cell_x] = True

    # Обновление камеры
    camera_x = player_rect.x - SCREEN_WIDTH // 2 + player_rect.width // 2
    camera_y = player_rect.y - SCREEN_HEIGHT // 2 + player_rect.height // 2

    # Отображение лабиринта
    draw_maze()

    # Отображение игрока
    screen.blit(player_img, (player_rect.x, player_rect.y))

    pygame.display.flip()
    clock.tick(FPS)

