import pygame
import sys
import sqlite3
import time
import random
import os

# -------------------- БАЗА ДАННЫХ --------------------
def init_db():
    conn = sqlite3.connect("snake.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        user_id INTEGER,
        level INTEGER,
        score INTEGER,
        state TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = sqlite3.connect("snake.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def create_user(username):
    conn = sqlite3.connect("snake.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    user_id = cur.lastrowid
    cur.execute("INSERT INTO scores (user_id, level, score, state) VALUES (?,?,?,?)", (user_id, 1, 0, ''))
    conn.commit()
    conn.close()

def load_user_state(username):
    user_id = get_user_id(username)
    if user_id is None:
        create_user(username)
        user_id = get_user_id(username)
    conn = sqlite3.connect("snake.db")
    cur = conn.cursor()
    cur.execute("SELECT level, score, state FROM scores WHERE user_id = ? ORDER BY rowid DESC LIMIT 1", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0], row[1], row[2]
    else:
        create_user(username)
        return 1, 0, ''

def save_user_state(username, level, score, state=''):
    user_id = get_user_id(username)
    conn = sqlite3.connect("snake.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (user_id, level, score, state) VALUES (?,?,?,?)", (user_id, level, score, state))
    conn.commit()
    conn.close()

# -------------------- ИГРА ЗМЕЙКА --------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

def generate_walls(level):
    walls = []
    # Меньше препятствий: 
    
    wall_count = max(0, level - 1)  # На 1 уровне 0 стен, на 2 уровне 1 стена, и т.д.
    for i in range(wall_count):
        x = random.randint(1, GRID_WIDTH - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        walls.append((x,y))
    return walls

def random_food_position(snake, walls):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x,y) not in snake and (x,y) not in walls:
            return (x,y)

def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def serialize_state(snake, direction, food_pos, food_time, food_value, walls, level, score):
    state_str = f"{level}|{score}|{direction[0]}|{direction[1]}|"
    state_str += ";".join([f"{p[0]},{p[1]}" for p in snake]) + "|"
    state_str += f"{food_pos[0]},{food_pos[1]}|{food_time}|{food_value}|"
    state_str += ";".join([f"{w[0]},{w[1]}" for w in walls])
    return state_str

def deserialize_state(state_str):
    if not state_str:
        return None
    parts = state_str.split("|")
    level = int(parts[0])
    score = int(parts[1])
    dx = int(parts[2])
    dy = int(parts[3])
    direction = (dx, dy)

    snake_str = parts[4]
    snake = []
    if snake_str:
        for s in snake_str.split(";"):
            if s:
                sx, sy = s.split(",")
                snake.append((int(sx), int(sy)))

    food_pos_str = parts[5]
    fx, fy = food_pos_str.split(",")
    food_pos = (int(fx), int(fy))
    food_time = float(parts[6])
    food_value = int(parts[7])

    walls_str = parts[8] if len(parts) > 8 else ""
    walls = []
    if walls_str:
        for w in walls_str.split(";"):
            if w:
                wx, wy = w.split(",")
                walls.append((int(wx), int(wy)))
    return level, score, direction, snake, food_pos, food_time, food_value, walls

def main():
    init_db()
    username = input("Введите имя пользователя: ").strip()
    level, score, saved_state = load_user_state(username)
    
    load_saved = False
    if saved_state:
        print("Найдено сохраненное состояние. Загрузить? (y/n)")
        ans = input().strip().lower()
        if ans == 'y':
            loaded = deserialize_state(saved_state)
            if loaded:
                level, score, direction, snake, food_pos, food_spawn_time, food_value, walls = loaded
                load_saved = True

    if not load_saved:
        snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        direction = (1,0)
        walls = generate_walls(level)
        food_pos = random_food_position(snake, walls)
        food_value = random.randint(1,3)
        food_spawn_time = time.time()

    SPEED = 5 + level
    running = True
    paused = False

    while running:
        clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state_str = serialize_state(snake, direction, food_pos, food_spawn_time, food_value, walls, level, score)
                save_user_state(username, level, score, state_str)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0,1):
                    direction = (0,-1)
                elif event.key == pygame.K_DOWN and direction != (0,-1):
                    direction = (0,1)
                elif event.key == pygame.K_LEFT and direction != (1,0):
                    direction = (-1,0)
                elif event.key == pygame.K_RIGHT and direction != (-1,0):
                    direction = (1,0)
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        state_str = serialize_state(snake, direction, food_pos, food_spawn_time, food_value, walls, level, score)
                        save_user_state(username, level, score, state_str)

        if paused:
            screen.fill((0,0,0))
            msg = font.render("PAUSED (P to unpause)", True, (255,255,255))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
            pygame.display.flip()
            continue

        head = snake[-1]
        new_head = (head[0]+direction[0], head[1]+direction[1])

        # Проверка выхода за границы
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            running = False

        # Проверка столкновения со стеной
        if new_head in walls:
            running = False

        # Проверка столкновения с собой
        if new_head in snake:
            running = False

        if not running:
            save_user_state(username, level, score, '')
            break

        snake.append(new_head)

        # Проверка на исчезновение еды (10 секунд)
        if time.time() - food_spawn_time > 10:
            food_pos = random_food_position(snake, walls)
            food_value = random.randint(1,3)
            food_spawn_time = time.time()

        # Проверка на съедение еды
        if new_head == food_pos:
            score += food_value
            food_pos = random_food_position(snake, walls)
            food_value = random.randint(1,3)
            food_spawn_time = time.time()
        else:
            snake.pop(0)

        
        if score > 0 and score % 3 == 0:
            # Переход на следующий уровень
            new_level = (score // 3) + 1
            if new_level != level:  # Добавим проверку, чтобы не генерировать на каждом кадре
                level = new_level
                SPEED = 5 + level
                walls = generate_walls(level)

        screen.fill((0,0,0))
        # Рисуем стены
        for w in walls:
            draw_cell(w, (100,100,100))

        # Рисуем змею
        for i, s in enumerate(snake):
            color = (0,255,0) if i < len(snake)-1 else (0,200,0)
            draw_cell(s, color)

        # Рисуем еду
        draw_cell(food_pos, (255,0,0))

        score_text = font.render(f"Score: {score} Level: {level}", True, (255,255,255))
        screen.blit(score_text, (5,5))

        pygame.display.flip()

    screen.fill((0,0,0))
    over_text = font.render(f"Game Over! Score: {score}", True, (255,255,255))
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()

if __name__ == "__main__":
    main()
