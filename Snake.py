import pygame
import time
import random
import json

score_file = "highscore.txt"
player_name = ""

snake_speed = 15
base_speed = 15

window_x = 720
window_y = 480
status_bar_height = 50

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


pygame.init()
try:
    with open(score_file, "r") as file:
        loaded_scores = json.load(file)
        if isinstance(loaded_scores, dict):
            high_scores = loaded_scores
        else:
            high_scores = {}
except:
    high_scores = {}

pygame.display.set_caption('Feed the Snake')
game_window = pygame.display.set_mode((window_x, window_y))


def name_input_screen():
    global player_name, high_score
    input_text = ""
    prompt_font = pygame.font.SysFont('times new roman', 40)
    info_font = pygame.font.SysFont('times new roman', 24)

    while True:
        game_window.fill(black)

        prompt_surface = prompt_font.render('Enter player name:', True, white)
        name_surface = prompt_font.render(input_text or '_', True, green)
        info_surface = info_font.render('Press Enter when done. Backspace to edit.', True, white)

        prompt_rect = prompt_surface.get_rect(center=(window_x/2, window_y/3))
        name_rect = name_surface.get_rect(center=(window_x/2, window_y/2))
        info_rect = info_surface.get_rect(center=(window_x/2, window_y/2 + 50))

        game_window.blit(prompt_surface, prompt_rect)
        game_window.blit(name_surface, name_rect)
        game_window.blit(info_surface, info_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        player_name = input_text.strip()
                        high_score = high_scores.get(player_name, 0)
                        return
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 15 and event.unicode.isprintable():
                        input_text += event.unicode


fps = pygame.time.Clock()

snake_position = [100, status_bar_height]

snake_body = [  [100, status_bar_height],
                [90, status_bar_height],
                [80, status_bar_height],
                [70, status_bar_height]
            ]

fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, ((window_y - status_bar_height)//10)) * 10 + status_bar_height]
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

def show_score(choice, color, font, size):
  
    
    score_font = pygame.font.SysFont(font, size)
    
    
   
    score_surface = score_font.render(
    f'{player_name}  Score : {score}  High Score : {high_score}',
    True, color
    )
    
    
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    
    game_window.blit(score_surface, score_rect)

def game_over():
    global high_score, high_scores

    if score > high_score:
        high_score = score
        high_scores[player_name] = high_score
        with open(score_file, "w") as file:
            json.dump(high_scores, file)


    my_font = pygame.font.SysFont('times new roman', 50)

    game_over_surface = my_font.render(
        'Game Over! Press any key to Restart',
        True, red
    )

    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():

          
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                waiting = False

    reset_game()


    
def reset_game():
    global snake_position, snake_body, fruit_position
    global fruit_spawn, direction, change_to, score

    snake_position = [100, 50]

    snake_body = [
        [100, 50],
        [90, 50],
        [80, 50],
        [70, 50]
    ]

    fruit_position = [random.randrange(1, (window_x//10)) * 10,
                      random.randrange(1, ((window_y - status_bar_height)//10)) * 10 + status_bar_height]

    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

def start_screen():
    while True:

        game_window.fill(black)

        title_font = pygame.font.SysFont('times new roman', 60)
        info_font = pygame.font.SysFont('times new roman', 30)

        title_surface = title_font.render('FEED THE SNAKE', True, green)
        info_surface = info_font.render('Press Any Key To Start', True, white)
        name_surface = info_font.render(f'Player: {player_name}', True, white)
        high_surface = info_font.render(f'High Score: {high_score}', True, white)

        title_rect = title_surface.get_rect(center=(window_x/2, window_y/3))
        name_rect = name_surface.get_rect(center=(window_x/2, window_y/2))
        info_rect = info_surface.get_rect(center=(window_x/2, window_y/2 + 40))
        high_rect = high_surface.get_rect(center=(window_x/2, window_y/2 + 80))

        game_window.blit(title_surface, title_rect)
        game_window.blit(name_surface, name_rect)
        game_window.blit(info_surface, info_rect)
        game_window.blit(high_surface, high_rect)

        pygame.display.update()

        for event in pygame.event.get():

            # Close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Start game
            if event.type == pygame.KEYDOWN:
                return

name_input_screen()
start_screen()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_k:
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == pygame.K_m:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == pygame.K_j:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))

    if snake_position == fruit_position:
        score += 10
        fruit_spawn = False

        snake_speed = base_speed + (score // 100) * 5
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]
    fruit_spawn = True

    game_window.fill(black)
    pygame.draw.rect(game_window, white, pygame.Rect(0, 0, window_x, status_bar_height))
    pygame.draw.rect(game_window, black, pygame.Rect(0, status_bar_height, window_x, window_y - status_bar_height))

    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white,
                     pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < status_bar_height or snake_position[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    show_score(1, black, 'times new roman', 20)

    pygame.display.update()
    fps.tick(snake_speed)
