import pygame, sys, random
from data import colors_codes

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, street):
        super().__init__()
        self.SAFE_DISTANCE=20
        self.SCREEN_HEIGHT=SCREEN_HEIGHT
        self.street = street
        self.width = 50
        self.height = 100
        self.images = [pygame.image.load(f'assets/enemy/enemy{i}.png').convert_alpha() for i in range(1,11)]
        self.images = [pygame.transform.scale(image, (self.width, self.height)) for image in self.images]
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect(center=(0, -400))

        self.timer=0
        self.spawn_delay=random.uniform(0.5, 3.0)
        self.active = False

        self.enemy_speed_list = list(range(self.street.line_speed + 2, self.street.line_speed + 3))

    def activate(self):
        self.active = True
        self.rect.centerx = self.street.get_random_lane_center()
        self.rect.y= -350 - random.randint(0,300)
        self.image = random.choice(self.images)
        self.vel_y = random.choice(self.enemy_speed_list)

    def respawn(self):
        self.timer=0
        self.spawn_delay=random.uniform(0.5, 3.0)
        self.active = False

    def check_cars_on_same_lane(self, enemy_cars_group, move_y):
        for other in enemy_cars_group:
            if other==self or not other.active:
                continue
            if abs(self.rect.centerx-other.rect.centerx)<self.width//2:
                if other.rect.bottom <= self.rect.top:
                    distance= self.rect.top-other.rect.bottom
                    if distance < self.SAFE_DISTANCE:
                        return 0
        return move_y

    def update(self, dt, enemy_cars_group):
        
        if not self.active:
            self.timer+=dt
            if self.timer >= self.spawn_delay:
                self.activate()
            return
        
        move_y = self.vel_y
        self.check_cars_on_same_lane(enemy_cars_group, move_y)
        self.rect.y+=move_y

        if self.rect.top>self.SCREEN_HEIGHT:
            self.respawn()








