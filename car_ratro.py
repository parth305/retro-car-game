import pygame
import random

pygame.init()
WIDTH = 1100
HEIGHT = 400
FPS = 1
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

song = pygame.mixer.Sound("secondgamefolder/mixkit-i-wont-surrender-846.mp3")

car_width = 110
car_height = 60
car_velo = 1
obs_velo = 1
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsans", 40)
font_end = pygame.font.SysFont("comicsans", 100)

object_genreate = pygame.USEREVENT + 1
genrate = pygame.event.Event(object_genreate)

colliede = pygame.USEREVENT + 2
accident = pygame.event.Event(colliede)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

image = pygame.transform.rotate(pygame.image.load('secondgamefolder/road..jfif'), 0)
road_image = pygame.transform.scale(image, (WIDTH, HEIGHT))

car_image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('secondgamefolder/car.jfif'), 0),
                                   (car_width, car_height))

obstical1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("secondgamefolder/ob1.jfif"), 270),
                                   (100, 50))
obstical3 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("secondgamefolder/ob3.jfif"), 270),
                                   (250, 75))
obstical4 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("secondgamefolder/ob4.jpg"), 270),
                                   (125, 50))
obstical5 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("secondgamefolder/ob5.jfif"), 270),
                                   (125, 50))

obsticals = [obstical1, obstical3, obstical4, obstical5]

rand_time = [800, 900, 1000, 1100, 1200]

last_tick = 0


def count_clock(ticks):
    global last_tick
    if ticks - last_tick >= random.choice(rand_time):
        last_tick = ticks
        pygame.event.post(genrate)


def draw(car_rect, obstical_rects, score):
    WIN.blit(road_image, (0, 0))
    WIN.blit(car_image, (car_rect.x, car_rect.y))
    for obstical in obstical_rects:
        WIN.blit(obstical[0], (obstical[1].x, obstical[1].y))
    text = font.render("score: " + str(score), True, WHITE)
    WIN.blit(text, (WIDTH - text.get_width(), 10))
    pygame.display.update()


def car_move(key_pressed, car):
    if key_pressed[pygame.K_UP] and car.y - car_velo >= 0:  # UP
        car.y -= car_velo
    if key_pressed[pygame.K_DOWN] and car.y + car_velo + car.height <= HEIGHT:  # DOWN
        car.y += car_velo
    if key_pressed[pygame.K_RIGHT] and car.x + car.width <= WIDTH:  # RIGHT
        car.x += car_velo
    if key_pressed[pygame.K_LEFT] and car.x >= 0:  # LEFT
        car.x -= car_velo


def obstical_move(obstical_rect, car):
    for obstical in obstical_rect:
        obstical[1].x -= obs_velo
        if car.colliderect(obstical[1]):
            pygame.event.post(accident)
        if obstical[1].x <= -obstical[0].get_width():
            obstical_rect.remove(obstical)


def game_over():
    song.stop()
    text = font_end.render("Game Over", True, RED)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def score_increment(score, car, obs_rect):
    global obs_velo
    for obstical in obs_rect:
        if car.x - 2 == obstical[1].x + obstical[1].width:
            score += 1
            # if score % 15 == 0:
            #     print("hey")
            #     obs_velo += 1
    return score


def main():
    run = True
    clock.tick(FPS)
    car_rect = pygame.Rect(100, 200, car_width, car_height)
    obstical_rects = []
    score = 0
    song.play(-1)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == object_genreate:
                # TODO:write code
                obs = random.choice(obsticals)
                obstical_rects.append((obs, pygame.Rect(WIDTH, random.randint(0, HEIGHT - obs.get_height() // 2 - 10),
                                                        obs.get_width(), obs.get_height())))
                # change==HEIGHT-obs.get_height()
            if event.type == colliede:
                # TODO:write code
                game_over()
                run = False
        KEY_PRESSED = pygame.key.get_pressed()
        count_clock(pygame.time.get_ticks())
        car_move(KEY_PRESSED, car_rect)
        obstical_move(obstical_rects, car_rect)
        score = score_increment(score, car_rect, obstical_rects)
        draw(car_rect, obstical_rects, score)


if __name__ == '__main__':
    main()
