# Модуль реализации игры

import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *


FPS = 60 # частота смены кадров в сек.
ANIMATION_SPEED = 0.18*1  # скорость движения в пикселях в миллисек.
WIN_WIDTH = 284 * 2      # размер окна в пикселях
WIN_HEIGHT = 512


class Bird(pygame.sprite.Sprite):
    # класс птичка (пингвин), наследуемая от Sprite

    WIDTH = HEIGHT = 32     # ширина картинки птички (пингвина)
    SINK_SPEED = 0.18       # скорость спуска по вертикали в пикселях в миллисек.
    CLIMB_SPEED = 0.3*0.8   # скорость подъема по вертикали в пикселях в миллисек.
    CLIMB_DURATION = 333.3*1.0  # длительность подъема по вертикали в миллисек.

    def __init__(self, x, y, msec_to_climb, images):
        # x: координата X птицы
        # y: координата Y птицы.
        # msec_to_climb: количество миллисекунд, оставшееся до конца подъема, длительностью CLIMB_DURATION
        # images: кортеж, содержащий изображения птицы: элемент 0 - с поднятыми крыльями; 1 - с опущенными

        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup) # создаем маски изображений без прозрачного фона
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)
        self.diff = 0 # атрибут сложности 0 - обычная, 1 - усложненная


    def update(self, delta_frames=1):
        # функция рассчета новой координаты y  птицы
        # при diff=0 подъем равномерный, при diff=1 в расчете координаты y используется косинус,
        # которая дает медленный подъем в начале и конце и быстрый в середине

        if self.msec_to_climb > 0:  # если подъем не завершен
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION # текущая доля подъема от полного
            self.y -= (Bird.CLIMB_SPEED * (1 - self.diff*math.cos(frac_climb_done * math.pi)) * # скорость,
                        frames_to_msec(delta_frames) )       # умноженная на число миллисек. между кадрами
            self.msec_to_climb -= frames_to_msec(delta_frames)  # уменьшаем число миллисек. до конца подъема
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames) # если подъем завершен, то увеличиваем y

    @property
    def image(self):
        # функция возвращает текущее изображение птицы. Функция может использоваться как атрибут
        if pygame.time.get_ticks() % 500 >= 250: # если остаток от деления числа миллисекунт с момента запуска
            return self._img_wingup              # на 500 больше 250, то поднятые крылья
        else:
            return self._img_wingdown

    @property
    def mask(self):
        # функция возвращает текущую маску изображения птицы. Функция может использоваться как атрибут
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
        # фукция возвращает прямоугольник с текущими координатами птицы
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


class IcePair(pygame.sprite.Sprite):  # класс ледяная пара (ворота) от Sprite

    WIDTH = 80  # ширина ледяных ворот 80 пикселей
    PIECE_HEIGHT = 32  # высота одной части ледяных ворот 32 пикселя
    ADD_INTERVAL = 3000  # интервал между появлением ворот в миллисек.

    def __init__(self, ice_end_img, ice_body_img):

        # для новых ледяных ворот устанавливается x = float(WIN_WIDTH - 1)

        #ice_end_img: картинка конца ворот
        #ice_body_img: картинка части ворот высотой 32 пикселя

        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False # атрибут, показывающий учитывались ли данные ворота в подсчете очков

        self.image = pygame.Surface((IcePair.WIDTH, WIN_HEIGHT), SRCALPHA) # создать поверхность с прозрачным фоном
        self.image.convert()   # увеличивает скорость отображения при выполнении blit
        #self.image.fill((0, 0, 0, 0))
        total_ice_body_pieces = int(  # вычисление числа частей ворот без проема и двух концевых
             WIN_HEIGHT / IcePair.PIECE_HEIGHT - 2 - 3    # полное число минус два концевых и минус проем (три части)
        )
        self.bottom_pieces = randint(1, total_ice_body_pieces) # случайное число частей ворот, которое будет сверху
        self.top_pieces = total_ice_body_pieces - self.bottom_pieces

        # рисуем на поверхности image нижнюю "половину" ворот
        for i in range(1, self.bottom_pieces + 1):  # цикл для отрисовки частей ворот (их число равно bottom_pieces)
            piece_pos = (0, WIN_HEIGHT - i*IcePair.PIECE_HEIGHT)
            self.image.blit(ice_body_img, piece_pos) # отрисовка части ворот на поверхность image
        # определяем координату y для отрисовки конца нижней половины ворот
        bottom_ice_end_y = WIN_HEIGHT - self.bottom_height_px # координата y верхнего края уже отрисованной половины ворот
        bottom_end_piece_pos = (0, bottom_ice_end_y - IcePair.PIECE_HEIGHT) # отнимаем еще высоту конца ворот
        self.image.blit(ice_end_img, bottom_end_piece_pos) # отрисовка конца ворот на поверхность image

        # рисуем на поверхности image верхнюю "половину" ворот
        for i in range(self.top_pieces): # цикл для отрисовки частей ворот (их число равно top_pieces)
            self.image.blit(ice_body_img, (0, i * IcePair.PIECE_HEIGHT)) # отрисовка части ворот на поверхность image
        top_ice_end_y = self.top_height_px # координата y нижнего края уже отрисованной половины ворот
        self.image.blit(ice_end_img, (0, top_ice_end_y)) # отрисовка конца ворот на поверхность image

        # увеличиваем число нижних и верхних частей из-за добавления концевых частей
        self.top_pieces += 1
        self.bottom_pieces += 1

        # создаем маску полученного на поверхности image полного изображения ворот
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        # функция возвращает высоту self.top_pieces-частей ророт в пикселях. Может вызываться как атрибут
        return self.top_pieces * IcePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        # функция возвращает высоту self.bottom_pieces-частей ророт в пикселях. Может вызываться как атрибут
        return self.bottom_pieces * IcePair.PIECE_HEIGHT

    @property
    def visible(self):
        # функция возвращает True, если часть ворот находится в пределах окна. Может вызываться как атрибут
        return -IcePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        # функция возвращает прямоугольник, к котором заключены ворота в данный момент
        return Rect(self.x, 0, IcePair.WIDTH, IcePair.PIECE_HEIGHT)

    def update(self, delta_frames=1):
        # метод обновляет позицию x ворот; delta_frames - число кадров, за которые нужно обносить x
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames) # (скорость в пикс/мс) * (длительность кадров в мс)

    def collides_with(self, bird):
        # функция возвращает True при столкновении маски ворот с объектом bird (птицей)
        return pygame.sprite.collide_mask(self, bird)


# функция загрузки файлов с изображениями. Возвращает словарь с картинками
def load_images():

    def load_image(img_file_name):
        # функция принимает название файла, добавляет к нему путь и возвращает загруженную картинку из этого файла

        file_name = os.path.join(os.path.dirname(__file__),
                                 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'background': load_image('background.jpg'),
            'ice-end': load_image('ice_end_02.png'),
            'ice-body': load_image('ice_body_02.png'),
            'bird-wingup': load_image('bird_wing_up.png'),
            'bird-wingdown': load_image('bird_wing_down.png')}


# функция вычисляет число миллисекунд, которые прощли при смене frames - кадров
def frames_to_msec(frames, fps=FPS):
    return 1000.0 * frames / fps


# функция, обратная предыдущей
def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0


# функция реализации кнопки Play в меню
def Play(surf, difficulty):

    display_surface = surf # присваиваем переданную из главного меню поверхность

    clock = pygame.time.Clock() # создаем объект типа Clock(часы) для вызова метода clock.tick(FPS),
                                # который устанавливает число кадров с сек
    score_font = pygame.font.SysFont('times', 32, bold=True)  # шрифт для вывода числа очков
    images = load_images() # вызов загругки словаря с изображениями

    # созбаем объект птичка и устанавливаем его посередине по вертикали
    bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                (images['bird-wingup'], images['bird-wingdown']))

    bird.diff = difficulty # устанавливаем переданную из меню трудность

    ices = deque() # создаем последовательность ices из модуля colletions

    frame_clock = 0  # счетчик кадров с начала игры (не увеличивается во время паузы)
    score = 0
    done = paused = False
    while not done:
        clock.tick(FPS) # устанавливает число FPS = 60 кадров с сек

        # добавляем новые ворота в последовательность ices когда не пауза или
        # число кадров frame_clock стало кратно интервалу между появлением ворот в кадрах
        if not (paused or frame_clock % msec_to_frames(IcePair.ADD_INTERVAL)):
            pp = IcePair(images['ice-end'], images['ice-body'])
            ices.append(pp)

        # обработка событий во время игры
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE): # если нажата ESC, то зывершение
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p): # если пауза, то инвертируем paused
                paused = not paused
            elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                    e.key in (K_UP, K_SPACE)):
                bird.msec_to_climb = Bird.CLIMB_DURATION # присвоить атрибуту "сколько до конца подъёма" полную длительность подъёма

        if paused:
            continue  # если пауза, то ничего не делаем и переходим к следующей итерации цикла

        # проверяем столкновение птицы со всеми воротами из последовательности ices
        ice_collision = any(p.collides_with(bird) for p in ices)
        if ice_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT: # если столкновение или птица
            return score # столкнулась с границей окна, то возврат из функции с текущим значением score

        # рисуем на рабочей поверхности фоновый рисунок, при этом "стираются" все объекты предыдущего кадра
        display_surface.blit(images['background'], (0, 0))

        # удаляем слева все объекты(ворота) из последовательности ices, у которых атрибут visible(видимость)=False
        while ices and not ices[0].visible:
            ices.popleft()

        # для всех объектов(ворот) из последовательности ices обновляем координаты и
        # рисуем их на рабочей поверхности на новых координатах
        for p in ices:
            p.update()
            display_surface.blit(p.image, p.rect)

        # для объекта птица обновляем координаты и
        # рисуем его на рабочей поверхности на новых координатах
        bird.update()
        display_surface.blit(bird.image, bird.rect)

        # обновление и вывод числа очков
        for p in ices:
            if p.x + IcePair.WIDTH < bird.x and not p.score_counted: # птица правее данных ворот и ворота не учитывались
                score += 1
                p.score_counted = True # данные ворота учтены в подсчете очков

        # создаем поверхность, выводим на нее надпись с числом очков
        score_surface = score_font.render('пройдено ворот: ' + str(score), True, (255, 255, 255))
        score_x = WIN_WIDTH/2 - score_surface.get_width()//2
        display_surface.blit(score_surface, (score_x, 10)) # рисуем надпись на рабочей поверхпости

        pygame.display.flip() # показ нового сформированного варианта рабочей поверхности в игровом окне
        frame_clock += 1 # увеличение счетчика кадров