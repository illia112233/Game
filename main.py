import math
import random
import time
import pygame
import sys

pygame.init()
pygame.mixer.init()

height = 600
width = 800

font = pygame.font.Font("Snowstorm.otf", 74)
text = font.render('Game Over', True, (100, 0, 200))
text_rect = text.get_rect(center=(800/2, 600/2))

quack_sound = pygame.mixer.Sound('sounds/quack.wav')
trampoline_sound = pygame.mixer.Sound('sounds/trampoline.wav')
game_over_sound = pygame.mixer.Sound("sounds/mixkit-arcade-retro-game-over-213.wav")

game_over_phon = pygame.image.load("game_over_phon.png")
game_over_phon = pygame.transform.scale(game_over_phon, (800, 600))
game_over_phon_rect = game_over_phon.get_rect(center=(400, 300))
phon_img = pygame.image.load("phon.png")
phon_img = pygame.transform.scale(phon_img, (800, 600))
phon_img_rect = phon_img.get_rect(center=(400, 300))
platform_img = pygame.image.load("platform.png")
platform_img = pygame.transform.scale(platform_img, (1000, 250))
platform_img_rect = platform_img.get_rect(center=(400, 565))
img = pygame.image.load("arrow.png")
img_rect = img.get_rect(center=(400, 300))
srd_img = pygame.image.load("srd.png")
srd_img = pygame.transform.scale(srd_img, (70, 50))
x_s = 25
srd_img_rect = srd_img.get_rect(center=(25, 25))

pers_img = pygame.image.load("Player.png")
pers_img = pygame.transform.scale(pers_img, (70, 70))
x = 50
y = 50
pers_img_rect = pers_img.get_rect(center=(50, 50))

window = pygame.display.set_mode((width, height))
run = True
#pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

y_vel = 0
u_gravitation = 0.06
arrow_speed = 1.8
kilk_srd = 3

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        pers_img_rect.x -= 5
    if keys[pygame.K_d]:
        pers_img_rect.x += 5
    if keys[pygame.K_w]:
        y_vel = -5
    if keys[pygame.K_s]:
        pers_img_rect.y += 5
    clock.tick(150)

    y_vel += u_gravitation
    pers_img_rect.y += y_vel

    if pers_img_rect.y > 500:
        pers_img_rect.y = 500
        y_vel = 0
    if pers_img_rect.x > 700:
        pers_img_rect.x = 0
        x_vel = 0
    if pers_img_rect.x < 0:
        pers_img_rect.x = 700
        x_vel = 0

    if pers_img_rect.y < -10:
        pers_img_rect.y = 500
        y_vel = 0

    direction_x, direction_y = pers_img_rect.centerx - img_rect.centerx, pers_img_rect.centery - img_rect.centery
    distance = math.hypot(direction_x, direction_y)
    if distance != 0:
        direction_x, direction_y = direction_x / distance, direction_y / distance

        # Переміщення стріли до персонажа
        img_rect.x += direction_x * arrow_speed
        img_rect.y += direction_y * arrow_speed

    # Обчислення кута повороту стріли
    angle = -math.degrees(math.atan2(direction_y, direction_x))

    rotated_img = pygame.transform.rotate(img, angle)
    rotated_img_rect = rotated_img.get_rect(center=img_rect.center)

    window.blit(phon_img, phon_img_rect)
    x_s = -40
    if pers_img_rect.colliderect(img_rect):
        kilk_srd -= 1
        quack_sound.play()
        x, y = random.randint(0, 800), random.randint(0, 600)
        img_rect.x = x
        img_rect.y = y
        window.blit(rotated_img, rotated_img_rect)
        pygame.display.update()
    for i in range(kilk_srd):
        window.blit(srd_img, srd_img_rect)
        x_s += 70
        srd_img_rect.center=(x_s, 25)
    if kilk_srd == 0:
        window.blit(game_over_phon, game_over_phon_rect)
        window.blit(text, text_rect)
        pygame.display.update()
        game_over_sound.play()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    window.blit(rotated_img, rotated_img_rect)
    window.blit(pers_img, pers_img_rect)
    window.blit(platform_img, platform_img_rect)
    pygame.display.update()
pygame.quit()




