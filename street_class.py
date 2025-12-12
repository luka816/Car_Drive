import pygame, sys, random
from data import colors_codes

class Street(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.width = 550
        self.height = SCREEN_HEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.color = colors_codes.get("very_dark_gray")
        self.image.fill(self.color)
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y=0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # lanes
        self.lanes=6
        self.line_height=50
        self.line_gap=20
        self.line_color=colors_codes.get("white")
        self.line_speed=10

        #calculate lanes positions
        self.lane_lines_x=[]
        self.lane_width=self.width/self.lanes
        for i in range(1,self.lanes):
            lane_x=i*self.lane_width
            self.lane_lines_x.append(lane_x)
        
        self.offset=0
    
    def get_random_lane_center(self):
        lane_width=self.width/self.lanes
        lane_index = random.randint(0, self.lanes - 1)
        lane_center_x=int(self.x+(lane_width*lane_index)+lane_width/2)
        return lane_center_x

    def draw_lanes(self):
        for x in self.lane_lines_x:
            y=-self.line_height + self.offset
            while y<self.height:
                pygame.draw.rect(self.image, self.line_color, (x-5, y, 10, self.line_height))
                y+=self.line_height + self.line_gap
        
        self.offset+=self.line_speed
        if self.offset>=self.line_height + self.line_gap:
            self.offset=0 
                                        
    def update(self):
        self.image.fill(self.color)
        
        self.draw_lanes()
              