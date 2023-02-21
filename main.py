import pygame
import os
import sys
import random


pygame.init()
size = width, height = 1440, 900
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["",
                  "Управление с помощью стрелок",
                  '       на клавиатуре',
                  "Стрелять при помощи пробела"]

    fon = load_image('title_fon.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("Zaychik-Regular.ttf", 40)
    font2 = pygame.font.Font("Zaychik-Regular.ttf", 90)
    text_coord = 700
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('#000000'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    title = font2.render("Saving the Planet", True, (0, 0, 0))
    screen.blit(title, (450, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    player_image = pygame.transform.scale(load_image('player.jpg', -1), (70, 60))

    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = Player.player_image
        self.rect = self.image.get_rect()
        self.rect.x = width / 2 - self.rect.width // 2
        self.rect.y = 510
        self.step = 0

    def update(self):
        self.step = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.step = -5
        if keys[pygame.K_RIGHT]:
            self.step = 5
        self.rect.x += self.step
        if self.rect.x + self.rect.width > width:
            self.rect.right = width
        if self.rect.x < 0:
            self.rect.x = 0

    def gun(self):
        bullet = Bullet(self.rect.center, self.rect.top)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullets_group, all_sprites)
        self.image = pygame.Surface((5, 10))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.center = x
        self.speed_bullet = -10

    def update(self):
        self.rect.y += self.speed_bullet
        # если он заходит за верхнюю часть экрана, исчезает
        if self.rect.bottom < 0:
            self.kill()


class Kosmos(pygame.sprite.Sprite):
    image = load_image("fon.jpg")

    def __init__(self):
        super().__init__(kosmos_group, all_sprites)
        self.image = Kosmos.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Asteroid(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("asteroid.png"), (60, 60))

    def __init__(self, x, y):
        super().__init__(asteroid_group, all_sprites)
        self.image = Asteroid.image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        # если он заходит за верхнюю часть экрана, исчезает
        if self.rect.bottom < 0:
            self.kill()


def game_over():
    for i in range(100000):
        screen.fill(pygame.Color('black'),
                    (random.random() * width,
                     random.random() * height, 3, 3))
    img = load_image('game_over.png', -1)
    screen.blit(img, (380, 270))
    r = read_record()
    font = pygame.font.Font("Zaychik-Regular.ttf", 60)
    text_counter = font.render(f'Счёт: {COUNT_GAME}           Рекорд: {r}', True, (255, 255, 255))
    screen.blit(text_counter, (460, 200))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


# функция возвращает число - рекордный счет, записанный в файле
def read_record():
    with open('data/record.txt') as f:
        return f.readline()


# перезаписываем рекорд, если счет больше
def write_record(r):
    with open('data/record.txt', 'w') as f:
        f.write(str(r))


start_screen()
pygame.display.set_caption('Saving the Planet')
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
kosmos_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
mountain = Kosmos()
player = Player()

timer = 50
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 5000)

timer_game = 0
timer_game_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_game_event, 1000)

COUNT_GAME = 0
font = pygame.font.Font(None, 70)
running = True
while running:
    record = read_record()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == timer_event:
            timer -= 1
            #print(timer)
            x = random.randint(0, 750)
            y = random.randint(-10, 0)
            lg = Asteroid(x, y)
        if event.type == timer_game_event:
            timer_game += 1
            print(timer_game)
            if timer_game == 60:
                if COUNT_GAME > int(record):
                    write_record(COUNT_GAME)
                game_over()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.gun()

    screen.fill(pygame.Color("black"))
    kosmos_group.draw(screen)
    asteroid_group.draw(screen)

    player_group.draw(screen)
    bullets_group.draw(screen)
    asteroid_group.update()
    player_group.update()
    bullets_group.update()
    conflict1 = pygame.sprite.groupcollide(asteroid_group, bullets_group, True, True)
    font = pygame.font.Font("Zaychik-Regular.ttf", 60)
    if conflict1:
        COUNT_GAME += 1
    text = font.render(f'Таймер: {str(timer_game)}     Счет: {str(COUNT_GAME)}', True, (0, 0, 0))
    screen.blit(text, (50, 800))
    conflict2 = pygame.sprite.spritecollide(player, asteroid_group, True)
    if conflict2:
        if COUNT_GAME > int(record):
            write_record(COUNT_GAME)
        game_over()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
