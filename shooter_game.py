from pygame import *
from random import *
from time import time as rel_time

# from pygame import sprite

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -20, 50, 50)
        bullets.add(bullet)


class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(80, 620)
class Asteroid(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



window = display.set_mode((700, 500))
display.set_caption("Caption")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
player = Player("rocket.png", 5, 420, 4, 80, 80)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, 620), 80, 1.3, 40, 40)
    asteroids.add(asteroid)
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), 80, 1.3, 80, 80)
    monsters.add(monster)

font.init()
font = font.Font(None, 36)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render("YOU LOSE", True, (255, 215, 0))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
timer = 0
game = True
clock = time.Clock()
FPS = 60
finish = False
score = 0
lost = 0
max_lost = 5
goal = 10

while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()


    if finish != True:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), 80, 1.3, 80,80)
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200,200))        
        score1 = font.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(score1,(10,20))
        lose_condition = font.render('Потрачено:' + str(lost), 1, (255, 255, 255))
        window.blit(lose_condition, (10, 50))
        player.update()
        player.reset()
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        asteroids.update()
        asteroids.draw(window)

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for z in asteroids:
            z.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(80, 620), 80, 1.3, 80,80)
            monsters.add(monster)
        for i in range(3):
            asteroid = Asteroid('asteroid.png', randint(80, 620), 80, 1.3, 30, 30)
            asteroids.add(asteroid)
        
    clock.tick(FPS)
