#from pygame import *
import pygame
import pygame_gui
import Game_modul

pygame.init()

WIN_WIDTH = 284 * 2      # Размер окна
WIN_HEIGHT = 512
size = (WIN_WIDTH, WIN_HEIGHT)

difficulty = 0

class Start_Menu: # класс стартового меню
    def __init__(self):
        # задаем заголовок окна
        pygame.display.set_caption('BIRD GATE')
        # создаем основную поверхность и задаем размер холста
        self.screen = pygame.display.set_mode(size)
        # загружаем фоновое изображение стартового меню
        self.background_image = pygame.image.load('images/Start_pingvin.jpg')
        # преобразование изображения под размер холста
        self.background_image = pygame.transform.scale(self.background_image, (WIN_WIDTH, WIN_HEIGHT-50))
        # создаем объект - менеджер, который будет включать кнопки меню
        # подгружаем при создании менеджера подготовленный в файле def_theme.json тему с видом кнопок и шрифтами
        self.manager = pygame_gui.UIManager(size, 'themes/def_theme.json')

        # создаем объект - кнопка "Уровень игры" и связываем его с созданным менеджером
        self.Level_Btn = pygame_gui.elements.UIButton(
             relative_rect=pygame.Rect((0, WIN_HEIGHT-50), (250, 50)),
             text= "Уровень: обычный",
             manager = self.manager
            )

        # создаем объект - кнопка "Играть" и связываем его с созданным менеджером
        self.Play_Btn = pygame_gui.elements.UIButton(
             relative_rect=pygame.Rect((250, WIN_HEIGHT-50), (160, 50)),
             text= "ИГРАТЬ",
             manager = self.manager
            )

        # создаем объект - кнопка "Выход" и связываем его с созданным менеджером
        self.Quit_Btn = pygame_gui.elements.UIButton(
             relative_rect=pygame.Rect((410, WIN_HEIGHT-50), (158, 50)),
             text= "ВЫХОД",
             manager = self.manager
            )

        self.difficulty = 0 # атрибут уровень устанавливаем в ноль

        self.screen.blit(self.background_image, (0, 0)) # рисуем фоновый рисунок на поверхности screen


    def draw(self):
        # функция отрисовки меню на поверхности screen
        self.manager.draw_ui(self.screen)


# основная функция
def main():

    start_menu = Start_Menu() # создаем экземпляр стартового меню со стартовым фоновым рисунком и меню
    clock = pygame.time.Clock() # создаем объект clock для задания числа кадров в сек
    score = 0 # обнуляем число очков
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0 # число секунд между кадрами
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame_gui.UI_BUTTON_PRESSED:
                if e.ui_element == start_menu.Level_Btn:
                    # изменяем уровень и надпись на кнопке
                    if start_menu.Level_Btn.text == "Уровень: обычный":
                        start_menu.Level_Btn.set_text('Уровень: сложный')
                        start_menu.difficulty = 1
                    else:
                        start_menu.Level_Btn.set_text('Уровень: обычный')
                        start_menu.difficulty = 0
                if e.ui_element == start_menu.Play_Btn:
                    # запускаем функцию игры на основной поверхности и текущим уровнем
                    score = Game_modul.Play(start_menu.screen, start_menu.difficulty)
                if e.ui_element == start_menu.Quit_Btn:
                    running = False

            start_menu.manager.process_events(e) # проверка событий менеджера меню
        # обновление меню
        start_menu.manager.update(time_delta)
        # отрисовка меню
        start_menu.draw()
        # вывод в рабочее игровое окно текущего вида поверхности
        pygame.display.flip()

    #print('Game over! Score: %i' % score)
    pygame.quit()


if __name__ == '__main__':
    main()