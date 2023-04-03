"""Модуль описывает игровой экран и логику игры."""

import os

import pygame as pg

# import time
import config as conf
from scripts.bird import Bird
from scripts.neural_network import NeuralNetwork


class Game:
    """Описывает игровой экран и процесс игры."""
    FPS = 60
    BACKGROUND = (0, 178, 255)
    SURF_INDENT = 10
    population_count = 10

    def __init__(self, game_data):
        # Установка параметров окна
        pg.init()
        self.screen = pg.display.set_mode((conf.WIDTH, conf.HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(conf.APP_NAME)
        self.icon = self.load_icon()
        pg.display.set_icon(self.icon)

        # Состояние игрового процесса
        self.is_running = True
        self.clock = pg.time.Clock()

        # Инициализация игровых объектов
        self.win_score = 1000
        self.population = 1

        self.game_surf = pg.Surface((conf.WIDTH,
                                conf.HEIGHT - self.get_text_surf_height()))

        Game.set_game_data(game_data)
        self.birds = pg.sprite.Group()
        birds = self.create_objects()
        self.birds.add(birds)

    @staticmethod
    def load_icon():
        """Загружает и возвращает иконку игрового окна."""
        img_folder = os.path.join(conf.PROJECT_FOLDER, "images")
        bird_img = pg.image.load(os.path.join(img_folder, "bird.png")).convert_alpha()
        bird_img = pg.transform.scale(bird_img, Bird.SIZE)
        return bird_img

    @staticmethod
    def set_game_data(data):
        # conf.repeat_count = data[""]
        Bird.mutation = data["mutation"]
        Bird.rotations = data["rotations"]
        Game.population_count = data["population"]

    def create_objects(self):
        """Создаёт экземпляры класса Bird
        и возвращает их в качестве списка.
        """
        birds = []

        # number_of_birds = int(self.game_surf.get_height() / Bird.SIZE[0])
        # for i in range(number_of_birds):
        for i in range(10):
            for _ in range(int(Game.population_count / 10)):
            # Картинка с птичкой используется как иконка игры и как спрайт,
            # поэтому загружается в этом классе
                bird = Bird(self.icon, Bird.SIZE[0] * i)
                birds.append(bird)
        return birds

    def get_text(self):
        """Возвращает текстовый объект с текущим номером популяции птичек."""
        font = pg.font.Font(None, 36)
        text = f"Популяция: {self.population}"
        text_surface = font.render(text, True, (255, 255, 255), Game.BACKGROUND)
        return text_surface

    def get_text_surf_height(self):
        """Возвращает высоту текста с популяциями."""
        return self.get_text().get_height() + 2 * Game.SURF_INDENT

    def get_game_height(self):
        """Возвращает высоту поверхности игры."""
        return self.screen.get_height() - self.get_text_surf_height()

    def draw(self):
        """Отрисовывает объекты на главный экран."""
        self.screen.fill(Game.BACKGROUND)
        self.screen.blit(self.get_text(), (Game.SURF_INDENT, Game.SURF_INDENT))
        self.screen.blit(self.game_surf, (0, self.get_text_surf_height()))
        self.game_surf.fill(Game.BACKGROUND)
        self.birds.draw(self.game_surf)

        #print(conf.best_brain)

    def update(self):
        """Обновляет экран игры."""
        pg.display.update()
        self.game_surf = pg.transform.scale(self.game_surf,
                                (self.screen.get_width(), self.get_game_height()))

        game_size = (self.game_surf.get_width(), self.game_surf.get_height())
        self.win_score = round(1000 * game_size[0] / conf.WIDTH * Bird.rotations / 10)
        self.birds.update(game_size)

        # Создание новых популяций птичек
        if not self.birds.sprites():
            self.birds.add(self.create_objects())
            self.population += 1

        # Для теста
        # if conf.best_brain.cost > 500:
        #     Bird.mutation = 0.1

    def handle_events(self):
        """Отслеживает нажатия клавиш и кнопок."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
        
            # Нажатие клавиш клавиатуры
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print(Bird.count)
                    # print(conf.best_brain.get_params())

    def run(self):
        """Запускает и контролирует игровой процесс."""
        while self.is_running:
            self.handle_events()
            self.draw()

            # Тест
            if conf.best_brain.cost > self.win_score:
                #print(conf.best_brain.get_params())
                conf.best_brain = NeuralNetwork(conf.NN_TOPOLOGY, False)
                return

            self.update()

            # if self.count == 0:
            #     time.sleep(3)
            # if self.count >= 0:
            #     self.count-= 1
            self.clock.tick(Game.FPS)

        pg.quit()