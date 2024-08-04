import pygame
import time
import random
import json
import os

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (160, 32, 240)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

save_file = "snake_save.json"

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def show_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

def show_level(level):
    value = score_font.render("Level: " + str(level), True, white)
    dis.blit(value, [0, 35])

def show_lives(lives):
    value = score_font.render("Lives: " + str(lives), True, white)
    dis.blit(value, [0, 70])

def load_progress():
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            return json.load(f)
    return {"score": 0, "level": 1, "lives": 3}

def save_progress(score, level, lives):
    with open(save_file, 'w') as f:
        json.dump({"score": score, "level": level, "lives": lives}, f)

def gameLoop():
    progress = load_progress()
    score = progress["score"]
    level = progress["level"]
    lives = progress["lives"]

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    bonus_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    bonus_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    bonus_timer = random.randint(50, 100)

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        save_progress(score, level, lives)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(score, level, lives)
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            lives -= 1
            if lives == 0:
                game_close = True
            else:
                x1 = dis_width / 2
                y1 = dis_height / 2
                x1_change = 0
                y1_change = 0
                snake_List = []
                Length_of_snake = 1

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, purple, [bonus_foodx, bonus_foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                lives -= 1
                if lives == 0:
                    game_close = True
                else:
                    x1 = dis_width / 2
                    y1 = dis_height / 2
                    x1_change = 0
                    y1_change = 0
                    snake_List = []
                    Length_of_snake = 1

        our_snake(snake_block, snake_List)
        show_score(score)
        show_level(level)
        show_lives(lives)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            if score % 10 == 0:
                level += 1
                snake_speed += 5

        if x1 == bonus_foodx and y1 == bonus_foody:
            bonus_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            bonus_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 3
            score += 5
            bonus_timer = random.randint(50, 100)

        if bonus_timer == 0:
            bonus_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            bonus_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            bonus_timer = random.randint(50, 100)
        else:
            bonus_timer -= 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
