import pygame, sys, random
from street_class import Street
from player_car_class import PlayerCar
from enemy_car_class import EnemyCar
from data import colors_codes


SCREEN_WIDTH, SCREEN_HEIGHT = 900, 680

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() # for sound effects

        pygame.display.set_caption("Car Drive")
        self.screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        #game variables
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.running_game = True
        self.state = "MENU" # MENU, PLAYING, GAME_OVER
        self.start_ticks = 0
        self.end_ticks = 0
        self.crashed = False

        # sounds
        self.engine_sound_path = "assets/sounds/angine_sound.mp3"
        self.crash_sound_path = "assets/sounds/crash_sound.mp3"

        self.crash_sound = pygame.mixer.Sound(self.crash_sound_path)
        self.crash_sound.set_volume(1.0)

        # font
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)

        #create street
        self.street = Street(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.street_group = pygame.sprite.GroupSingle()
        self.street_group.add(self.street)

        # create player car
        self.player_car = PlayerCar(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_car_group = pygame.sprite.GroupSingle()
        self.player_car_group.add(self.player_car)

        # create enemy cars
        self.enemy_cars_count = 3
        self.enemy_cars_group = pygame.sprite.Group()
        for i in range (self.enemy_cars_count+1):
            enemy_car=EnemyCar(SCREEN_WIDTH, SCREEN_HEIGHT, self.street)
            self.enemy_cars_group.add(enemy_car)

    def reset_game(self):

        pygame.mixer.music.load(self.engine_sound_path)
        pygame.mixer.music.set_volume(1.0)   # optional
        pygame.mixer.music.play(-1)  

        # Reset player
        self.player_car.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.player_car.vel_x = 0
        self.player_car.vel_y = 0

        for enemy in self.enemy_cars_group:
            enemy.rect.y = -random.randint(350, 400)
            enemy.rect.centerx = self.street.get_random_lane_center()
            enemy.active = False  # activate so they start moving
            enemy.vel_y = random.choice(enemy.enemy_speed_list)
        
        self.start_ticks = pygame.time.get_ticks()
        self.crashed = False

        self.state = "PLAYING"

    def draw_menu(self):
        self.screen.fill(colors_codes.get("green"))
        title_text = self.font.render("Car Drive", True, colors_codes.get("white"))
        prompt_text = self.small_font.render("Press Enter or Space to Start", True, colors_codes.get("white"))
        self.screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
        self.screen.blit(prompt_text, prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

        pygame.display.update()


    def draw_playing(self, dt):
        self.screen.fill(colors_codes.get("green"))
        
        # Timer
        seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        timer_text = self.small_font.render(f"Time: {seconds}", True, colors_codes.get("white"))
        self.screen.blit(timer_text, (10, 10))

        # draw street
        self.street_group.update()
        self.street_group.draw(self.screen)

        # draw player car
        self.player_car_group.update(self.street)
        self.player_car_group.draw(self.screen)

        # draw enemy cars
        self.enemy_cars_group.update(dt, self.enemy_cars_group)
        self.enemy_cars_group.draw(self.screen)

        if not self.crashed:
            if pygame.sprite.spritecollide(self.player_car, self.enemy_cars_group, False):
                self.state="GAME_OVER"
                self.end_ticks=pygame.time.get_ticks()
                self.crashed=True

                pygame.mixer.music.stop()  # stop the engine
                self.crash_sound.play()


        pygame.display.update()

    def draw_game_over(self):
        self.screen.fill(colors_codes.get("green"))
        title_text=self.font.render("GAME OVER!", True, colors_codes.get("white"))

        #survived time
        seconds= (self.end_ticks - self.start_ticks)//1000 if self.end_ticks>self.start_ticks else 0
        score_text = self.small_font.render(f'You Survived: {seconds} sec', True, colors_codes.get("white"))
        prompt_text =  self.small_font.render(f'Press Enter ot Space to Restart', True, colors_codes.get("white"))

        self.screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50)))
        self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.screen.blit(prompt_text, prompt_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50)))

        pygame.display.update()
                         

    def main_loop(self):
        while self.running_game:
            dt=self.clock.tick(self.FPS) / 1000  # Amount of seconds between each loop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_game = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == "MENU" and (event.key==pygame.K_RETURN or event.key==pygame.K_SPACE):
                        self.reset_game()
                    elif self.state == "GAME_OVER" and (event.key==pygame.K_RETURN or event.key==pygame.K_SPACE):
                        self.reset_game()


            if self.state == "MENU":
                self.draw_menu()    
            elif self.state == "PLAYING":
                self.draw_playing(dt)
            elif self.state == "GAME_OVER":
                self.draw_game_over()
    
        pygame.quit()
        sys.exit()

game = Game()

if __name__ == "__main__":
    game.main_loop()    


