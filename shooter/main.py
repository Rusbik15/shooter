from random import randint
from pygame import*
from typing import Any 
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
window = display.set_mode((700, 500 ))
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)
font.init()
my_font = font.SysFont('Times' , 36)
font1 = font.SysFont('Times' , 80)
win = font1.render('You win', True, (255, 255, 255))
lose = font1.render('You lose', True, (180, 0, 0))

hp = 3
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
game = True
finish = False
lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        sprite.Sprite.__init__(self)
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        buttons = key.get_pressed()
        if buttons[K_a] and self.rect.x >5:
            self.rect.x -= self.speed
        if buttons[K_d] and self.rect.x <620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
       self.rect.y += self.speed
       if self.rect.y >= 500:
            self.rect.x = randint(0 , 620)
            self.rect.y = -40
            global lost
            lost += 1
 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

Enemys = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(0 , 620), -30 , 80, 50, randint(1, 4))
    Enemys.add(enemy)
bullets = sprite.Group()




rocket = Player('rocket.png', 20, 400, 80, 100, 10)

while game == True:
    for i in event.get():
        if i.type == QUIT:
            game = False

        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.fire()
                fire_sound.play()

    if finish != True:
        window.blit(bg, (0, 0))
        rocket.draw()
        rocket.update()
        Enemys.draw(window)
        Enemys.update()
        bullets.update()
        bullets.draw(window)
        if sprite.spritecollide(rocket, Enemys, True):
            hp -= 1
            enemy = Enemy("ufo.png", randint(0, 640), -40, 70, 50, randint(1, 4))
            Enemys.add(enemy)
        if sprite.groupcollide(Enemys, bullets, True, True):
            score += 1
            enemy = Enemy("ufo.png", randint(0, 640), -40, 70, 50, randint(1, 4))
            Enemys.add(enemy)
        if score > 15:
            finish = True
            window.blit(win, (250, 200))
        if hp <= 0 or lost >= 5:
            finish = True
            window.blit(lose, (250, 200))
        text_score = my_font.render("Рахунок: " + str(score), True, (255,255,255))
        window.blit(text_score, (10,20))
        text_lose = my_font.render("Пропущено: " + str(lost), True, (255,255,255))
        window.blit(text_lose, (10,50))
        text_lose = my_font.render("життя: " + str(hp), True, (255,255,255))
        window.blit(text_lose, (10,80))

    else:
        time.delay(5000)
        finish = False
        lost = 0 
        score = 0
        hp = 3
        for nemy in Enemys:
            enemy.kill()
        for bullet in bullets:
            bullet.kill()
        for i in range(4):
            enemy = Enemy("ufo.png", randint(0,620), -40, 80, 50, randint(1, 5))
            Enemys.add(enemy)

    display.update()
    clock.tick(50)
