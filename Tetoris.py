import pygame
import random
import copy
import time

pygame.init()

# Настройки игры
columns = 10
strings = 20
screen_x = 300
screen_y = 600
cell_x = screen_x / columns
cell_y = screen_y / strings

# Цвета
BACKGROUND_COLOR = pygame.Color(231, 192, 188, 100)
GRID_COLOR = pygame.Color(236, 159, 171, 100)
BLOCK_COLOR = pygame.Color(217, 126, 138, 100)
OUTLINE_COLOR = pygame.Color(139, 60, 70, 50)
TEXT_COLOR = pygame.Color(55, 8, 8)

# Инициализация экрана
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Tetoris Pink!')

clock = pygame.time.Clock()
fps = 60

# Инициализация сетки
grid = [[[1, pygame.Rect(i * cell_x, j * cell_y, cell_x, cell_y), GRID_COLOR] for j in range(strings)] for i in range(columns)]

# Фигуры
details = [
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    [[1, 1], [-1, 0], [0, 0], [1, 0]], 
    [[-1, 1], [0, 1], [0, 0], [-1, 0]], 
    [[1, 0], [1, 1], [0, 0], [-1, 0]], 
    [[0, 1], [-1, 0], [0, 0], [1, 0]], 
    [[-1, 1], [0, 1], [0, 0], [1, 0]],
]

det = [[pygame.Rect(details[i][j][0] * cell_x + cell_x * (columns // 2), details[i][j][1] * cell_y, cell_x, cell_y) for j in range(4)] for i in range(len(details))]

# Переменные игры
detail = pygame.Rect(0, 0, cell_x, cell_y)
det_choice = copy.deepcopy(random.choice(det))
count = 0
game = True
rotate = False
score = 0
max_score = 0
paused = False
in_menu = True
game_over = False

# Шрифты
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 36)

def draw_text(text, x, y, color=TEXT_COLOR, font_type=font, center=False):
    """Функция для отрисовки текста"""
    text_surface = font_type.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
    else:
        screen.blit(text_surface, (x, y))

def draw_menu():
    """Отрисовка главного меню"""
    screen.fill(BACKGROUND_COLOR)
    draw_text("Tetoris Pink!", screen_x // 2, screen_y // 2 - 60, font_type=large_font, center=True)
    draw_text(f"Max Score: {max_score}", screen_x // 2, screen_y // 2 - 20, center=True)
    draw_text("Press SPACE", screen_x // 2, screen_y // 2 + 20, center=True)
    draw_text("to start", screen_x // 2, screen_y // 2 + 50, center=True)
    pygame.display.flip()

def draw_pause():
    """Отрисовка экрана паузы"""
    screen.fill(BACKGROUND_COLOR)
    draw_text("Paused", screen_x // 2, screen_y // 2 - 50, font_type=large_font, center=True)
    draw_text("Press P to resume", screen_x // 2, screen_y // 2, center=True)
    pygame.display.flip()

def draw_game_over():
    """Отрисовка экрана проигрыша"""
    screen.fill(BACKGROUND_COLOR)
    draw_text("Game Over!", screen_x // 2, screen_y // 2 - 60, font_type=large_font, center=True)
    draw_text(f"Score: {score}", screen_x // 2, screen_y // 2 - 20, center=True)
    pygame.display.flip()

def clear_row(row):
    """Удаление строки"""
    for i in range(columns):
        if grid[i][row][0] == 0:
            outline_rect = pygame.Rect(grid[i][row][1].x, grid[i][row][1].y, cell_x, cell_y)
            pygame.draw.rect(screen, OUTLINE_COLOR, outline_rect, 3)
        grid[i][row][0] = 1  # Очищаем строку

def shift_rows_down(from_row):
    """Сдвиг строк вниз после удаления"""
    for row in range(from_row, 0, -1):
        for col in range(columns):
            grid[col][row][0] = grid[col][row - 1][0]
            grid[col][row][2] = grid[col][row - 1][2]

while game:
    if in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_menu = False
                    score = 0
                    grid = [[[1, pygame.Rect(i * cell_x, j * cell_y, cell_x, cell_y), GRID_COLOR] for j in range(strings)] for i in range(columns)]  # Очистка сетки
                    det_choice = copy.deepcopy(random.choice(det))  # Новая фигура
    else:
        if game_over:
            draw_game_over()
            time.sleep(3)
            in_menu = True
            game_over = False
        elif paused:
            draw_pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
        else:
            delta_x = 0
            delta_y = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        delta_x = -1
                    elif event.key == pygame.K_RIGHT:
                        delta_x = 1
                    elif event.key == pygame.K_UP:
                        rotate = True
                    elif event.key == pygame.K_p:
                        paused = True

            key = pygame.key.get_pressed()

            if key[pygame.K_DOWN]:
                count = 31 * fps

            screen.fill(BACKGROUND_COLOR)

            for i in range(columns):
                for j in range(strings):
                    if grid[i][j][0] == 0:
                        pygame.draw.rect(screen, grid[i][j][2], grid[i][j][1])
                    else:
                        pygame.draw.rect(screen, GRID_COLOR, grid[i][j][1], 1)
            
            for i in range(4):
                if ((det_choice[i].x + delta_x * cell_x < 0) or (det_choice[i].x + delta_x * cell_x >= screen_x)):
                    delta_x = 0

                if ((det_choice[i].y + cell_y >= screen_y) or (
                    grid[int(det_choice[i].x // cell_x)][int(det_choice[i].y // cell_y) + 1][0] == 0)):
                    delta_y = 0

                    for i in range(4):
                        x = int(det_choice[i].x // cell_x)
                        y = int(det_choice[i].y // cell_y)

                        grid[x][y][0] = 0
                        grid[x][y][2] = pygame.Color(139, 60, 70, 100)

                        # Проверка на проигрыш
                        if y <= 0:
                            game_over = True
                            if score > max_score:
                                max_score = score

                    # Начисление 10 очков за каждую поставленную фигуру
                    score += 10

                    detail.x = 0
                    detail.y = 0
                    det_choice = copy.deepcopy(random.choice(det))

            for i in range(4):
                det_choice[i].x += delta_x * cell_x

            count += fps

            if count > 30 * fps:
                for i in range(4):
                    det_choice[i].y += delta_y * cell_y
                count = 0

            for i in range(4):
                detail.x = det_choice[i].x
                detail.y = det_choice[i].y
                pygame.draw.rect(screen, BLOCK_COLOR, detail)
            
            C = det_choice[2]
            if rotate:
                for i in range(4):
                    x = det_choice[i].y - C.y
                    y = det_choice[i].x - C.x

                    det_choice[i].x = C.x - x
                    det_choice[i].y = C.y + y
                rotate = False

            for j in range(strings - 1, -1, -1):
                count_cells = 0

                for i in range(columns):
                    if grid[i][j][0] == 0:
                        count_cells += 1

                if count_cells == columns:
                    clear_row(j)
                    shift_rows_down(j)  # Сдвиг строк вниз
                    score += 50  # Начисление 50 очков за удалённую строку

            draw_text(f"Score: {score}", 10, 10)  

            pygame.display.flip()
            clock.tick(fps)

pygame.quit()