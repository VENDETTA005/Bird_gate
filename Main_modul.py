#from pygame import *
import pygame
import pygame_gui

pygame.init()

WIN_WIDTH = 284 * 2      # Размер окна
WIN_HEIGHT = 512
size = (WIN_WIDTH, WIN_HEIGHT)

ARIAL_30 = pygame.font.SysFont('arial', 50)



class Start_Menu: # класс стартового меню
    def __init__(self):
        pygame.display.set_caption('BIRD GATE')
        self.screen = pygame.display.set_mode(size) # размер холста
        self.background_image = pygame.image.load('Images/Start_pingvin.jpg') # фоновое изображение стартового меню
        self.background_image = pygame.transform.scale(self.background_image, (WIN_WIDTH, WIN_HEIGHT)) # преобразование изображения под размер холста
        self.manager = pygame_gui.UIManager(size)


        self.font = pygame.font.SysFont('times', 60)

        self.current_level = 'ОБЫЧНЫЙ УРОВЕНЬ'
        self.test_drop_down_menu = pygame_gui.elements.UIDropDownMenu(
            ['ОБЫЧНЫЙ УРОВЕНЬ', 'СЛОЖНЫЙ УРОВЕНЬ'],
            self.current_level,
            pygame.Rect((50, 50), (200, 50)),
            self.manager
            #container=self
        )

        self.Play_Btn = pygame_gui.elements.UIButton(
             relative_rect=pygame.Rect((50, 100), (200, 50)),
             text= "ИГРАТЬ",
             manager = self.manager
            )

        self.Quit_Btn = pygame_gui.elements.UIButton(
             relative_rect=pygame.Rect((50, 150), (200, 50)),
             text= "ВЫХОД",
             manager = self.manager
            )


    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.manager.draw_ui(self.screen)


def main():

    start_menu = Start_Menu()
    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            start_menu.manager.process_events(e)
        start_menu.manager.update(time_delta)

        start_menu.draw()

        pygame.display.flip()



if __name__ == '__main__':
    main()