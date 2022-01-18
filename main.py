import pygame
import random
import sys
import os

pygame.init()

wight_disp = 1280
height_disp = 820

display = pygame.display.set_mode((wight_disp, height_disp))
pygame.display.set_caption("Играй что бы выжить =)")

image = pygame.image.load("картинки/almaz.png")
pygame.display.set_icon(image)

pygame.mixer.music.load("fon_myz.mp3")
pygame.mixer.music.set_volume(0.02)

myr1 = pygame.mixer.Sound("мур1.mp3")
myr2 = pygame.mixer.Sound("мур2.mp3")
myr3 = pygame.mixer.Sound("мур3.mp3")
spis_myr = [myr1, myr2, myr3]

pw = 60
ph = 100
x = wight_disp // 3
y = height_disp - ph - 100
hy = 100
wx = 119

clock = pygame.time.Clock()
jump = False

jump_count = 25

fps = 80

preg_w = 20
preg_h = 70
preg_x = wight_disp - 50
preg_y = height_disp - preg_h - 100

speed = 5
ocki = 0

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


preg1 = load_image("камень.jpg")
preg1 = pygame.transform.scale(preg1, (100, 110))
preg2 = load_image("камень.jpg")
preg2 = pygame.transform.scale(preg2, (100, 110))
preg3 = load_image("ящик.jpg")
preg3 = pygame.transform.scale(preg3, (100, 110))
pregrad_spis = [preg1, preg3, preg2]

kot1 = load_image("кот1.PNG", -1)
kot1 = pygame.transform.flip(kot1, True, False)
kot2 = load_image("кот2.PNG", -1)
kot2 = pygame.transform.flip(kot2, True, False)
kot3 = load_image("кот3.PNG", -1)
kot3 = pygame.transform.flip(kot3, True, False)
kot4 = load_image("кот4.PNG", -1)
kot4 = pygame.transform.flip(kot4, True, False)

spis_kot = [kot1, kot2, kot3, kot4]

kot12 = load_image("ток1.PNG", -1)
kot12 = pygame.transform.flip(kot12, True, False)
kot22 = load_image("ток2.PNG", -1)
kot22 = pygame.transform.flip(kot22, True, False)
kot32 = load_image("ток3.PNG", -1)
kot32 = pygame.transform.flip(kot32, True, False)
kot42 = load_image("ток4.PNG", -1)
kot42 = pygame.transform.flip(kot42, True, False)

fish = load_image("рыба.png")
fish = pygame.transform.flip(fish, True, False)
fish = pygame.transform.scale(fish, (50, 50))

spis_kot2 = [kot12, kot22, kot32, kot42]
pause = False
kill_xp = False

xp = 9
xp_image = load_image("хп.png")
xp_image = pygame.transform.scale(xp_image, (50, 50))

shet = 1
game_over = load_image("game_over.jpg")
game_over = pygame.transform.scale(game_over, (1280, 920))

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
            self.x = wight_disp + 50
            return False

    def ret(self, radius):
        self.x = radius

    def proverka(self):
        global x, y, wx, hy
        if (x + wx > self.x and x + wx < self.x + 50) and y + hy > self.y or (x > self.x and x < self.x + 50 and y + hy > self.y ):
            return True


def run_jump():
    global x, y, jump, jump_count
    if jump_count >= -25:
        y -= jump_count
        jump_count -= 1
    else:
        jump_count = 25
        jump = False


def app():
    global spis_p, add_preg
    spis_p = []


def run_game():
    pygame.mixer.music.play(-1)
    count = 0
    global jump, x, y, pause, kill_xp, ocki, speed, xp, shet, spis_myr
    game = True
    fon = load_image("фон2.png")
    fon1 = pygame.transform.scale(fon, (1280, 820))
    app()
    add_preg(spis_p)
    vrema = 0
    vrema_xp = 0
    flagR = False
    flagL = False
    run = 0
    x_f, y_f = 1280, 670
    flag = False
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
                    if flagR == True:
                        run = 1
                    else:
                        run = 0
                if event.key == pygame.K_RIGHT:
                    flagR = False
                    if flagL == True:
                        run = 2
                    else:
                        run = 0
        if run == 1 and x + 5 < wight_disp - 150:
            x += speed - 1
        if run == 2 and x - 5 > 0:
            x -= speed - 2
        if count == 4:
            count = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pass
        if jump:
            run_jump()
        display.blit(fon1, (0, 0))
        if (x + wx > x_f and x + wx < x_f + 50) and y + hy > y_f or (x > x_f and x < x_f + 50 and y + hy > y_f):
            x_f, y_f = 12800, 67000
            flag = False
            pygame.mixer.Sound.play(spis_myr[random.randint(0, 2)])
            ocki += 1
            if xp < 9:
                xp += 1
        if flag is True:
            display.blit(fish, (x_f, y_f))
            x_f -= speed
            if x_f < 0:
                flag = False
        for index in range(xp):
            display.blit(xp_image, (index * 55, 0))
        print_text(f"{ocki}", 1160, 10, (255, 100, 100), fonte = "bebas_neue_book.ttf", font_size = 70)
        draw_array(spis_p)
        display.blit(spis_kot[count], (x, y))
        pygame.display.update()
        vrema += clock.tick()
        if kill_xp:
            if vrema > 40 / shet:
                xp -= 1
                if xp < 1:
                    xp = 0
                    display.blit(game_over, (0, 0))
                    pygame.display.flip()
                    pause = True
                kill_xp = False
        if vrema > 20 / shet:
            if random.randint(1, 60) == 1:
                if flag is False:
                    flag = True
                    x_f, y_f = 1280, 670
                    display.blit(fish, (x_f, y_f))
        if vrema > 40 / shet:
            count += 1
            vrema = 0
        clock.tick(fps)


def add_preg(array):
    global speed
    array.append(Pregrada(wight_disp + 600, height_disp - 180, 50, 80, pregrad_spis[random.randint(0, 2)], speed, False))
    array.append(Pregrada(wight_disp, height_disp - 170, 40, 50, pregrad_spis[random.randint(0, 2)], speed, False))
    array.append(Pregrada(wight_disp + 300, height_disp - 150, 30, 50, pregrad_spis[random.randint(0, 2)], speed, False))


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


def draw_array(array):
    for i in array:
        flag = i.move()
        if not flag:
            radius = postav(array)
            i.ret(radius)


def print_text(texte, x, y, color = (0, 0, 0), fonte = "bebas_neue_book.ttf", font_size = 50):
    font_type = pygame.font.Font(fonte, font_size)
    text = font_type.render(texte, True, color)
    display.blit(text, (x, y))


run_game()