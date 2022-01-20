import pygame
import random
import sys
import os

"""Инициализируем pygame"""
pygame.init()


"""Обозначаем все необходимые пременные"""

# Размеры
wight_disp = 1280
height_disp = 820
height_player = 100
weight_player = 119
x = wight_disp // 3
y = height_disp - 100 - 100
pregrada_weight = 20
pregrada_height = 70
pregrada_x = wight_disp - 50
pregrada_y = height_disp - pregrada_height - 100

display = pygame.display.set_mode((wight_disp, height_disp))

# Перемещение
jump = False
jump_count = 25
speed = 5
shet = 1

# Прочие константы
ocki = 0
name_kot = "Сёмка"
pause = False
kill_xp = False
xp = 9


# Время
fps = 80
clock = pygame.time.Clock()

"""Подключаем звук и настраиваем"""
myr1 = pygame.mixer.Sound("мур1.mp3")
myr2 = pygame.mixer.Sound("мур2.mp3")
myr3 = pygame.mixer.Sound("мур3.mp3")
spis_myr = [myr1, myr2, myr3]
pygame.mixer.music.load("fon_myz.mp3")
pygame.mixer.music.set_volume(0.02)
proval = pygame.mixer.Sound("ахах.mp3")

"""Функция для загрузки картинок"""


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


"""Загружаем картинки"""

pygame.display.set_caption("Беги за рыбой")
image = pygame.image.load("картинки/almaz.png")
pygame.display.set_icon(image)

# Загржаем_преграды
preg1 = load_image("камень.jpg")
preg1 = pygame.transform.scale(preg1, (100, 110))
preg2 = load_image("камень.jpg")
preg2 = pygame.transform.scale(preg2, (100, 110))
preg3 = load_image("ящик.jpg")
preg3 = pygame.transform.scale(preg3, (100, 110))
pregrad_spis = [preg1, preg3, preg2, preg3]

# Загружаем котов
kot1 = load_image("кот1.PNG", -1)
kot1 = pygame.transform.flip(kot1, True, False)
kot2 = load_image("кот2.PNG", -1)
kot2 = pygame.transform.flip(kot2, True, False)
kot3 = load_image("кот3.PNG", -1)
kot3 = pygame.transform.flip(kot3, True, False)
kot4 = load_image("кот4.PNG", -1)
kot4 = pygame.transform.flip(kot4, True, False)

kot12 = load_image("ток1.PNG", -1)
kot12 = pygame.transform.flip(kot12, True, False)
kot22 = load_image("ток2.PNG", -1)
kot22 = pygame.transform.flip(kot22, True, False)
kot32 = load_image("ток3.PNG", -1)
kot32 = pygame.transform.flip(kot32, True, False)
kot42 = load_image("ток4.PNG", -1)
kot42 = pygame.transform.flip(kot42, True, False)

spis_kot1 = [kot1, kot2, kot3, kot4]
spis_kot2 = [kot12, kot22, kot32, kot42]
# Список котов
spis_kot = spis_kot1

# Загружаем рыбу
fish = load_image("рыба.png")
fish = pygame.transform.flip(fish, True, False)
fish = pygame.transform.scale(fish, (50, 50))

# Загружаем сковородку
skovorodka = load_image("сковородка.png", -1)
skovorodka = pygame.transform.scale(skovorodka, (100, 100))
skovorodka1 = pygame.transform.rotate(skovorodka, 57)

# Загружаем конец игры
game_over = load_image("game_over.jpg")
game_over = pygame.transform.scale(game_over, (1280, 920))

# Загружаем менюшку
menu = load_image("менюшка.jpg")
menu = pygame.transform.scale(menu, (1280, 920))

# Загружаем хп_бар
xp_image = load_image("хп.png")
xp_image = pygame.transform.scale(xp_image, (50, 50))


"""Класс препятствий"""


class Pregrada:
    def __init__(self, x, y, wight, height, image, speed, flag):
        self.x = x
        self.y = y
        self.wight = wight
        self.height = height
        self.image = image
        self.speed = speed
        self.flag = flag

    def move(self):
        flag = False
        global pause, kill_xp, ocki, speed, shet
        if self.x >= -self.wight:
            self.image = pygame.transform.scale(self.image, (50, 100))
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            if self.proverka():
                kill_xp = True
            if ocki >= 3:
                self.speed = 6
                shet = 1.2
                speed = 6
            if ocki >= 10:
                self.speed = 7
                shet = 1.4
                speed = 7
            if ocki >= 15:
                self.speed = 8
                shet = 1.4
                speed = 8
            if ocki >= 20:
                self.speed = 9
                shet = 1.8
                speed = 9
            if ocki >= 30:
                self.speed = 10
                shet = 2.2
                speed = 10
            if ocki >= 50:
                self.speed = 11
                shet = 2.8
                speed = 11
            return True
        else:
            self.image = pregrad_spis[random.randint(0, 2)]
            self.x = wight_disp + 50
            return False

    def ret(self, radius):
        self.x = radius

    def proverka(self):
        global x, y, weight_player, height_player
        if (self.x < x + weight_player < self.x + 50) and y + height_player > self.y or \
                (self.x < x < self.x + 50 and y + height_player > self.y):
            return True


"""Прыжок"""


def run_jump():
    global x, y, jump, jump_count
    if jump_count >= -25:
        y -= jump_count
        jump_count -= 1
    else:
        jump_count = 25
        jump = False


""""Стартовое меню"""


def menu_start():
    global xp, spis_kot, name_kot, skovorodka
    spis = []
    rez = open("rez.txt", "r")
    rezult = rez.readlines()
    for i in rezult:
        i = i.strip("\n")
        spis.append(i.split(" "))
    while True:
        display.blit(menu, (0, 0))
        print_text("Сёмка", 1135, 60, (0, 0, 0), fonte="bebas_neue_book.ttf",
                   font_size=40)
        print_text("Дымка", 935, 60, (0, 0, 0), fonte="bebas_neue_book.ttf",
                   font_size=40)
        if spis_kot == spis_kot2:
            name_kot = "Дымка"
            pygame.draw.rect(display, (0, 255, 0), (915, 100, 130, 120), 5)
        else:
            name_kot = "Сёмка"
            pygame.draw.rect(display, (0, 255, 0), (1115, 100, 130, 120), 5)
        print_text(f"Твои лучшие результаты", 10, 500, (100, 100, 255),
                   fonte="bebas_neue_book.ttf",
                   font_size=40)
        xp = 9
        clock.tick(10000)
        display.blit(skovorodka, (10, 10))
        display.blit(kot3, (1115, 100))
        display.blit(kot32, (915, 100))
        display.blit(fish, (42, 52))
        print_text(f"Нажмите Enter чтобы начать игру", 255, 290, (255, 100, 100),
                   fonte="bebas_neue_book.ttf",
                   font_size=70)
        spis = sorted(spis, key=lambda x: int(x[0]))
        for index, lyhii_rez in enumerate(spis[::-1]):
            if index < 5:
                print_text(f"{lyhii_rez[0]} - ({lyhii_rez[1]})", 110, 550 + index * 50, (100, 100, 255),
                           fonte="bebas_neue_book.ttf",
                           font_size=40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 915 < event.pos[0] < 915 + 130 and 100 < event.pos[1] < 100 + 120:
                    spis_kot = spis_kot2
                    pygame.draw.rect(display, (0, 255, 0), (915, 100, 130, 120), 5)
                elif 1115 < event.pos[0] < 1115 + 130 and 100 < event.pos[1] < 100 + 120:
                    spis_kot = spis_kot1
                    pygame.draw.rect(display, (0, 255, 0), (1115, 100, 130, 120), 5)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run_game()
                    break


"""Начало игры"""


def run_game():
    global jump, x, y, pause, kill_xp, ocki, speed, xp, shet, spis_myr
    # Размеры
    x = wight_disp // 3
    y = height_disp - 100 - 100
    x_f, y_f = 1280, 670

    # Данные
    flagR, flagL, flag_fish = False, False, False
    sprait = 0
    ocki = 0
    vrema = 0
    run = 0
    game = True
    flag_scovorodka, x_covorod, y_covorod = False, 0, y

    # Результаты и музыка
    rezult = open("rez.txt", "a")
    pygame.mixer.music.play(-1)

    # Фоны
    fon = load_image("фон2.png")
    fon1 = pygame.transform.scale(fon, (1280, 820))

    # Прочее
    spis_p = []
    add_preg(spis_p)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump = True
                if event.key == pygame.K_LEFT:
                    flagL = True
                    run = 2
                if event.key == pygame.K_RIGHT:
                    flagR = True
                    run = 1
                if event.key == pygame.K_ESCAPE:
                    if pause is False:
                        pause = True
                    else:
                        pause = False
                    while pause:
                        pygame.mixer.music.pause()
                        print_text("Пауза. Нажмите Esc для продолжегия", wight_disp // 2 - 300, height_disp // 2 - 200)
                        pygame.display.flip()
                        for event1 in pygame.event.get():
                            if event1.type == pygame.KEYDOWN:
                                if event1.key == pygame.K_ESCAPE:
                                    if pause is False:
                                        pause = True
                                    else:
                                        pause = False
                                        pygame.mixer.music.unpause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    flagL = False
                    if flagR is True:
                        run = 1
                    else:
                        run = 0
                if event.key == pygame.K_RIGHT:
                    flagR = False
                    if flagL is True:
                        run = 2
                    else:
                        run = 0
        if run == 1 and x + 5 < wight_disp - 150:
            x += speed - 1
        if run == 2 and x - 5 > 0:
            x -= speed - 2
        if sprait == 4:
            sprait = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pass
        if jump:
            run_jump()
        display.blit(fon1, (0, 0))
        if (x_f < x + weight_player < x_f + 100) and y + height_player > y_f or\
                (x_f < x < x_f + 100 and y + height_player > y_f):
            x_f, y_f = 12800, 67000
            flag_fish = False
            pygame.mixer.Sound.play(spis_myr[random.randint(0, 2)])
            ocki += 1
            if xp < 9:
                xp += 1
        if (x < x_covorod < x + weight_player and y_covorod >= y - 20 and y_covorod < y + height_player) \
            or (x_covorod + 100 > x and x_covorod + 100 < x + weight_player and
                y_covorod + 100 >= y - 20 and y_covorod + 100 < y + height_player):
            x_covorod, y_covorod = 0, y
            kill_xp = True
            flag_scovorodka = False
        if flag_fish is True:
            display.blit(fish, (x_f, y_f))
            x_f -= speed
            if x_f < 0:
                flag_fish = False
        if flag_scovorodka is True:
            x_covorod += speed + 3
            display.blit(skovorodka1, (x_covorod, y_covorod))
            if x_covorod > wight_disp:
                flag_scovorodka = False
                x_covorod, y_covorod = 0, y
        for index in range(xp):
            display.blit(xp_image, (index * 55, 0))
        print_text(f"{ocki}", 1160, 10, (255, 100, 100), fonte="bebas_neue_book.ttf", font_size=70)
        draw_array(spis_p)
        display.blit(spis_kot[sprait], (x, y))
        pygame.display.update()
        vrema += clock.tick()
        if kill_xp:
            if vrema > 40 / shet:
                xp -= 1
                if xp < 1:
                    rezult.write(f"\n{ocki} {name_kot}")
                    rezult.close()
                    pygame.mixer.Sound.play(proval)
                    display.blit(game_over, (0, -70))
                    print_text(f"Ваш результат {ocki}", 440, 520, (255, 100, 100), fonte="bebas_neue_book.ttf",
                               font_size=70)
                    print_text(f"Нажмите Enter чтобы выйти в меню", 265, 590, (255, 100, 100),
                               fonte="bebas_neue_book.ttf",
                               font_size=70)
                    pygame.mixer.music.stop()
                    pygame.display.flip()
                    while game:
                        for event2 in pygame.event.get():
                            if event2.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event2.type == pygame.KEYDOWN:
                                if event2.key == pygame.K_RETURN:
                                    pygame.mixer.Sound.stop(proval)
                                    menu_start()
                                    break
                kill_xp = False
        if vrema > 20 / shet:
            if random.randint(1, 60) == 1:
                if flag_fish is False:
                    flag_fish = True
                    x_f, y_f = 1280, 670
                    display.blit(fish, (x_f, y_f))
        if vrema > 20 / shet:
            if random.randint(1, 130) == 1:
                if flag_fish is False:
                    flag_scovorodka = True
                    x_f, y_f = 1280, 670
                    display.blit(skovorodka1, (x_covorod, y_covorod))
        if vrema > 40 / shet:
            sprait += 1
            vrema = 0
        clock.tick(fps)


"""Добавляем преграды"""


def add_preg(array):
    global speed
    array.append(
        Pregrada(wight_disp + 600, height_disp - 180, 50, 80, pregrad_spis[random.randint(0, 2)], speed, False))
    array.append(Pregrada(wight_disp, height_disp - 170, 40, 50, pregrad_spis[random.randint(0, 2)], speed, False))
    array.append(
        Pregrada(wight_disp + 300, height_disp - 150, 30, 50, pregrad_spis[random.randint(0, 2)], speed, False))


"""Возвращаем радиус"""


def postav(array):
    ma = max(array[0].x, array[1].x, array[2].x)
    if ma < wight_disp:
        radius = wight_disp
        if radius - ma < 50:
            radius += 150
    else:
        radius = ma
    coise = random.randrange(0, 5)
    if coise == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)
    return radius


"""Перемещаем преграды"""


def draw_array(array):
    for i in array:
        flag = i.move()
        if not flag:
            radius = postav(array)
            i.ret(radius)


"""Выводим текст"""


def print_text(texte, x, y, color=(0, 0, 0), fonte="bebas_neue_book.ttf", font_size=50):
    font_type = pygame.font.Font(fonte, font_size)
    text = font_type.render(texte, True, color)
    display.blit(text, (x, y))


menu_start()