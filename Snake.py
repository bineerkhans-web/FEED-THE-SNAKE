import pygame
import time
import random

snake_speed = 15
base_speed = 15

window_x = 720
window_y = 480


black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


pygame.init()
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0


pygame.display.set_caption('Feed the Snake')
game_window = pygame.display.set_mode((window_x, window_y))


fps = pygame.time.Clock()

snake_position = [100, 50]

snake_body = [  [100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
            ]

fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

def show_score(choice, color, font, size):
  
    
    score_font = pygame.font.SysFont(font, size)
    
    
   
    score_surface = score_font.render(
    'Score : ' + str(score) + '  High Score : ' + str(high_score),
    True, color
    )
    
    
    score_rect = score_surface.get_rect()
    
    game_window.blit(score_surface, score_rect)

def game_over():
    global high_score

    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))


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
                      random.randrange(1, (window_y//10)) * 10]

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
        high_surface = info_font.render('High Score : ' + str(high_score), True, white)

        title_rect = title_surface.get_rect(center=(window_x/2, window_y/3))
        info_rect = info_surface.get_rect(center=(window_x/2, window_y/2))
        high_rect = high_surface.get_rect(center=(window_x/2, window_y/2 + 50))

        game_window.blit(title_surface, title_rect)
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

start_screen()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
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

    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white,
                     pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    show_score(1, white, 'times new roman', 20)

    pygame.display.update()
    fps.tick(snake_speed)
