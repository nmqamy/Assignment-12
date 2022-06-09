import time
import math
import random
import arcade
from arcade.key import END
from arcade.sprite_list.spatial_hash import check_for_collision

SCREEN__WIDTH=800
SCREEN_HEIGHT=600


class Startship(arcade.Sprite):
    def __init__(self):
       super().__init__(':resources:images/space_shooter/playerShip1_orange.png')
       self.center_x = SCREEN__WIDTH // 2
       self.center_y = 32
       self.width = 30
       self.height = 20
       self.angle = 0
       self.change_angle = 0
       self.speed = 10
       self.bullet_list = []
       self.score = 0
       self.hearth = 3
       self.change_x = 0
       self.change_y = 0

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

    def rotate(self):
        self.angle += self.change_angle * self.speed

    def fire(self):
       self.bullet_list.append(Bullet(self))
       arcade.play_sound(arcade.sound.Sound(':resources:sounds/upgrade4.wav'))
    


class Enemy(arcade.Sprite):
    def __init__(self,s):
       super().__init__(':resources:images/space_shooter/playerShip1_blue.png')
       self.center_x = random.randint(0,SCREEN__WIDTH)
       self.center_y = SCREEN_HEIGHT + 2
       self.width = 50
       self.height = 40
       self.speed = s
       self.angle = 180

    def move(self):
        self.center_y -= self.speed 



class Bullet(arcade.Sprite):
     def __init__(self,host):
       super().__init__(':resources:images/space_shooter/laserRed01.png')
       self.speed = 6
       self.angle = host.angle
       self.center_x = host.center_x
       self.center_y = host.center_y

     def move(self):
        a = math.radians(self.angle) 
        self.center_x -= self.speed * math.sin(a)
        self.center_y += self.speed * math.cos(a)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN__WIDTH , SCREEN_HEIGHT , 'Interstaller Game')
        arcade.set_background_color(arcade.color.NAVY_BLUE)
        self.background_image=arcade.load_texture(':resources:images/backgrounds/stars.png')
        self.me=Startship()
        self.enemy_list = []
        self.start_time = time.time()
        self.num_enemy = 0

    def on_draw(self):
        arcade.start_render()

        if self.me.hearth <= 0:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text('GAME OVER',150,SCREEN_HEIGHT//2,arcade.color.RED,50)
        else:
            arcade.draw_lrwh_rectangle_textured(0,0,SCREEN__WIDTH,SCREEN_HEIGHT,self.background_image)
            self.me.draw()
       
        for bullet in self.me.bullet_list:
            bullet.draw()
       
       
        for enemy in self.enemy_list:
            enemy.draw()

        for hearth in range(self.me.hearth):
            hearth_image = arcade.load_texture('heart.png')
            arcade.draw_lrwh_rectangle_textured(5 + hearth * 21 , 10 , 20 , 20 , hearth_image)

        arcade.draw_text(f'score: {self.me.score}',680 , 20 , arcade.color.PINK , 20)

    def on_update(self, delta_time):
        self.end_time = time.time()
        time_enemy = random.randrange(2,8,2)

        if self.end_time - self.start_time >= time_enemy:
          self.num_enemy += 1
        #   self.enemy_list.append(Enemy(SCREEN__WIDTH , SCREEN_HEIGHT , 3 + self.num_enemy//10))
          self.enemy_list.append(Enemy(3 + self.num_enemy//10))
          self.start_time = time.time()

        self.me.rotate()
        self.me.move()

        for enemy in self.enemy_list:
            enemy.move()

        for bullet in self.me.bullet_list:
            bullet.move()

        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if check_for_collision(enemy , bullet):
                    arcade.play_sound(arcade.sound.Sound(':resources:sounds/explosion1.wav'))
                    self.enemy_list.remove(enemy)
                    self.me.bullet_list.remove(bullet)
                    self.me.score += 1

        for enemy in self.enemy_list:
            if enemy.center_y <= 0:
                self.enemy_list.remove(enemy)
                self.me.hearth -= 1

        for bullet in self.me.bullet_list:
            if bullet.center_y >= SCREEN_HEIGHT or SCREEN__WIDTH <= bullet.center_x <=0 or bullet.center_y <= 0:
                self.me.bullet_list.remove(bullet) 

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.UP:
            self.me.change_y = 1
        elif key == arcade.key.DOWN:
            self.me.change_y = -1
        elif key == arcade.key.LEFT:
            self.me.change_x = -1
        elif key == arcade.key.RIGHT:
            self.me.change_x = +1
        if key == arcade.key.A:
            self.me.change_angle = 1
        if key == arcade.key.S:
            self.me.change_angle = -1
        elif key == arcade.key.SPACE:
            self.me.fire()   

    def on_key_release(self, symbol: int, modifiers: int):
        return super().on_key_release(symbol, modifiers)

    def on_key_release(self, key, modifiers: int):
        self.me.change_angle = 0
        self.me.change_x = 0
        self.me.change_y = 0


game=Game()
arcade.run()
