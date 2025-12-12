import pygame, sys, random
from data import colors_codes

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.width = 50
        self.height = 100
        self.image = pygame.image.load("assets/player_car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.player_car_x = (SCREEN_WIDTH - self.width) // 2
        self.player_car_y = SCREEN_HEIGHT - 100
        self.rect = self.image.get_rect(center=(self.player_car_x, self.player_car_y))

        self.vel_x=0
        self.vel_y=0
        self.acceleration=0.5
        self.max_speed=10
        self.friction=0.1

    def keep_car_on_street(self, street):
        if street.rect:
            if self.rect.left <= street.rect.left:
                self.rect.left = street.rect.left
            if self.rect.right >= street.rect.right:
                self.rect.right = street.rect.right
            if self.rect.top <= street.rect.top:
                self.rect.top = street.rect.top
            if self.rect.bottom >= street.rect.bottom - 10:
                self.rect.bottom = street.rect.bottom - 10


    def car_movement(self):
        kays=pygame.key.get_pressed()
        if kays[pygame.K_LEFT] or kays[pygame.K_a]:
            self.vel_x -= self.acceleration
        elif kays[pygame.K_RIGHT] or kays[pygame.K_d]:
            self.vel_x += self.acceleration
        elif kays[pygame.K_UP] or kays[pygame.K_w]:
            self.vel_y -= self.acceleration
        elif kays[pygame.K_DOWN] or kays[pygame.K_s]:
            self.vel_y += self.acceleration
        else:
            if self.vel_x>0:
                self.vel_x = max(0, self.vel_x - self.friction)
            elif self.vel_x<0:
                self.vel_x = min(0, self.vel_x + self.friction)
            elif self.vel_y>0:
                self.vel_y = max(0, self.vel_y - self.friction)
            elif self.vel_y<0:
                self.vel_y = min(0, self.vel_y + self.friction)
    
        #limit speed
        if self.vel_x > self.max_speed:
            self.vel_x = self.max_speed
        elif self.vel_x < -self.max_speed:
            self.vel_x = -self.max_speed
        if self.vel_y > self.max_speed:
            self.vel_y = self.max_speed 
        elif self.vel_y < -self.max_speed:
            self.vel_y = -self.max_speed
        
        #update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y   

    def update(self, street):
        self.car_movement()
        self.keep_car_on_street(street)