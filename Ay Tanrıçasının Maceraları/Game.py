import pygame
import os
import sys
import random
pygame.init()
width=1024
height=576
size = (width, height)


screen = pygame.display.set_mode(size)
level = 1

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
sounds_folder = os.path.join(game_folder,"sounds")
animation_folder = os.path.join(game_folder,"animation")
animations = []
for i in range(0,5):
    animations.append("{}.png".format(i))

background = pygame.image.load(os.path.join(img_folder,"background3.png")).convert()
#1366x768
pygame.mixer.music.load(os.path.join(sounds_folder,"sailor moon.mp3"))
pygame.mixer.music.play(100000000)



fireEffect = pygame.mixer.Sound(os.path.join(sounds_folder,"fire.ogg"))
deathEffect = pygame.mixer.Sound(os.path.join(sounds_folder,"death.ogg"))
devilDieEffect = pygame.mixer.Sound(os.path.join(sounds_folder,"enemydeath.ogg"))
speedGain  = pygame.mixer.Sound(os.path.join(sounds_folder,"ice.ogg"))
liveGain = pygame.mixer.Sound(os.path.join(sounds_folder,"wow.ogg"))
action = pygame.mixer.Sound(os.path.join(sounds_folder,"action.ogg"))
powerUps = ["sun.png","lucky.png", "lucky.png", "lucky.png", "lucky.png", "lucky.png"]

clock = pygame.time.Clock()

font = pygame.font.SysFont("Helvetica", 50 )
devils =  [ "enemy1.png","enemy2.png","enemy3.png","enemy4.png",
            "enemy1.png","enemy2.png","enemy3.png","enemy4.png",
            "enemy1.png","enemy2.png","enemy3.png","enemy4.png",
            "enemy1.png","enemy2.png","enemy3.png","enemy4.png","moon.png","moon.png","moon.png" ]


pygame.mouse.set_visible(0)
class Ms(pygame.sprite.Sprite):
    def __init__(self, x=width // 2, y=height // 2):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder,"usagi.png"))#.convert()
        self.can = 3
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.rect.x = 0
        self.rect.y = y
        self.shild = 100
        self.fireDelay = 250
        self.fireLast = pygame.time.get_ticks()
        self.hider_timer = 2100
        self.isHide = False
        self.lastHide = pygame.time.get_ticks()
        self.boostStart = 0
    def changeBulletSpeed(self,speed):
        self.fireDelay = speed
        self.boostStart = pygame.time.get_ticks()
        # 83x110
    def hide(self):
        self.isHide = True
        self.lastHide = pygame.time.get_ticks()
        self.rect.center = (-200, height // 2)





    def update(self, *args) :
        up,down,right,left,shoot = args
        if self.isHide and pygame.time.get_ticks() - self.lastHide > self.hider_timer:
            self.isHide = False
            self.rect.x = 0
            self.rect.y = height//2

        if pygame.time.get_ticks() - self.boostStart > 5000:
            self.changeBulletSpeed(250)

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.size[1] > height:
            self.rect.y = height - self.rect.size[1]
        if up:
            self.rect.y -= 10
        if down:
            self.rect.y += 10
        if shoot:
            self.shoot()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.fireLast > self.fireDelay:
            self.fireLast = now
            fireEffect.play()
            rocket = Rocket(self.rect.y)
            all_sprites.add(rocket)
            rockets.add(rocket)
class PowerUp(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.choice = random.choice(powerUps)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,self.choice)),(40,40))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = 5
    def update(self, *args):
        self.rect.x -= self.speedx
class Aliens(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.secim = random.choice(devils)
        devil = pygame.image.load(os.path.join(img_folder, self.secim))
        self.image = devil
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.rect.y = random.randrange(height - self.rect.height)
        self.rect.x = random.randrange(width + 40, width + 100)
        self.speedx = random.randrange(5, 13)
        self.speedy = random.randrange(-3,3)
        #enemy90x121
        #enem290x90

    def update(self, *args):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0:
            self.rect.y = random.randrange(height - self.rect.height)
            self.rect.x = random.randrange(width + 40, width + 100)
            self.speedx = random.randrange(5, 13)
            self.speedy = random.randrange(-3, 3)
            global score
            score += 1

class Animation(pygame.sprite.Sprite):
    def __init__(self,devil,game_folder,list):
        super().__init__()
        self.devil = devil
        self.game_folder = game_folder
        self.list = list
        self.counter = 1
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.game_folder, self.list[self.counter])), self.devil.image.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.devil.rect.center
        self.delay = 75
        self.lastChange = pygame.time.get_ticks()
    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.lastChange > self.delay:
            self.lastChange = now
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.game_folder, self.list[self.counter])), self.devil.image.get_size())
            self.rect = self.image.get_rect()
            self.rect.center = self.devil.rect.center
            self.counter += 1

        if self.counter == len(self.list):
            self.kill()


class Rocket(pygame.sprite.Sprite):
    def __init__(self,msy):
        super().__init__()

        self.image = pygame.image.load(os.path.join(img_folder,"fire.png"))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.80) // 2
        self.rect.x = 59
        self.rect.y = msy + 6
        #30x21
    def update(self, *args):
        self.rect.x += 8
        if self.rect.left > width:
            self.kill()

counterRestart = True



## MS2 SHILD IMAGE ##
def shildDraw(screen,x,y,value):
    if value < 0:
        value = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (value / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 3)
    if value >= 60:
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)
    elif value >= 30 and value < 60:
        pygame.draw.rect(screen, (204, 204, 0), fill_rect)
    elif value < 30:
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
def hpDraw(screen,x,y,can):
    img = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,"hp1.png")),(25,20))
    img_rect = img.get_rect()
    for i in range(can):
        img_rect.x = x + (40*i)
        img_rect.y = y
        screen.blit(img, img_rect)


game_over = True
def show_gameover_screen():
    kontrol = True
    endstart = pygame.image.load(os.path.join(img_folder,"start1.png")).convert()
    screen.blit(endstart,endstart.get_rect())
    pygame.display.update()

    while kontrol:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h:
                    kontrol = False



while True:
    if game_over:
        show_gameover_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        aliens = pygame.sprite.Group()
        rockets = pygame.sprite.Group()
        powerGains = pygame.sprite.Group()
        for i in range(10):
            alien1 = Aliens()
            all_sprites.add(alien1)
            aliens.add(alien1)

        ms2 = Ms()
        all_sprites.add(ms2)

        score = 0
    screen.fill((255, 255, 255))
    screen.blit(background,background.get_rect())
    aliensNumber = len(aliens)
    clock.tick(60)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ms2.shoot()
    up,down,right,left,shoot = keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_d],keys[pygame.K_a],keys[pygame.K_SPACE]
    all_sprites.update(up,down,right,left,shoot)
    fontScore = font.render("EVILS  : {}".format(aliensNumber), 1, (255,255,0))

    all_sprites.draw(screen)

    screen.blit(fontScore, (width - fontScore.get_size()[0], height - fontScore.get_size()[1]))
    act = pygame.sprite.spritecollide(ms2,aliens,True,collided=pygame.sprite.collide_circle)

    isHit = pygame.sprite.groupcollide(rockets,aliens,True,True)
    if isHit:
        devilDieEffect.play()
        for devilss in isHit.values():
            for devil in devilss:
                kaboom = Animation(devil, animation_folder, animations)
                all_sprites.add(kaboom)
                if random.random() > 0.90:
                    powerGain = PowerUp(devil.rect.center)
                    powerGain.add(powerGains)
                    all_sprites.add(powerGain)

                if devil.secim == "moon.png":
                    if ms2.shild + 10 < 100:
                        ms2.shild += 10

                    else:
                        ms2.shild = 100
    isPowerGain = pygame.sprite.spritecollide(ms2,powerGains,True)
    if isPowerGain:
        for powerType in isPowerGain:
            if powerType.choice == "lucky.png":
                speedGain.play()
                ms2.changeBulletSpeed(130)
            else:
                liveGain.play()
                ms2.can += 1
    if act:
        pygame.mixer.Sound(deathEffect).play()
        for alien1 in act:
            boom = Animation(alien1,animation_folder,animations)
            all_sprites.add(boom)
            ms2.shild -= alien1.radius *2

    shildDraw(screen, 5, 5, ms2.shild)
    hpDraw(screen, 5, 25, ms2.can)

    if act or aliensNumber == 0:
        if ms2.shild <= 0:
            deathEffect.play()
            ms2.can -= 1
            ms2.hide()
            if ms2.can == 0:
                level = 1
                game_over = True
            ms2.shild = 100

        if aliensNumber == 0:
            if counterRestart:
                action.play()
                finishValue = pygame.time.get_ticks()
                counterRestart = False
                levelArticleFont = pygame.font.SysFont("Helvetica", 50)
                article = levelArticleFont.render("LEVEL {}".format(level + 1), 1, (255, 255, 0))

            screen.blit(article, (10, 40))
            if pygame.time.get_ticks() - finishValue > 4000:
                counterRestart = True
                level += 1
                for i in range(level * 10):
                    alien1 = Aliens()
                    all_sprites.add(alien1)
                    aliens.add(alien1)

    pygame.display.update()

