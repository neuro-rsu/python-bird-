import tkinter as tk

import config as conf
from scripts.game_screen import Game


class Frame(tk.Frame):
    """Создает участок формы для ввода параметров генетического алгоритма."""

    def __init__(self, master):
        super().__init__(master)

        # Метки со значениями полей ввода
        labels = [
            "Число повторений", "Вероятность мутации, %", "Размер популяции", "Количество поворотов"
        ]
        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="W")

        # Поля для ввода
        self.repeat = tk.Entry(self)
        self.mutation = tk.Entry(self)
        self.population = tk.Entry(self)
        self.rotations = tk.Entry(self)

        # Позиционирование полей для ввода
        self.repeat.grid(row=0, column=1, sticky="E", pady=10)
        self.mutation.grid(row=1, column=1, sticky="E", pady=10)
        self.population.grid(row=2, column=1, sticky="E", pady=10)
        self.rotations.grid(row=3, column=1, sticky="E", pady=10)

        self.set_default_values()

    def set_default_values(self):
        """Устанавливает генетические параметры по умолчанию."""
        self.repeat.insert(0, "1")
        self.mutation.insert(0, "40")
        self.population.insert(0, "10")
        self.rotations.insert(0, "10")


class Form(tk.Tk):
    """Генерирует форму для передачи данных и запуска игры."""

    def __init__(self):
        super().__init__()

        self.frame = Frame(self)
        self.frame.pack(side="top", padx=10)

        # Кнопка запуска и ее позиционирование
        self.button = tk.Button(self, text="Запустить", command=self.launch)
        self.button.pack(pady=10)

        # Размещение окна в центре экрана
        self.update()
        self.geometry(self.set_window_coord())

    def set_window_coord(self):
        """Возвращает координаты центра экрана для окна."""
        width, height = self.winfo_width(), self.winfo_height()
        x = round((self.winfo_screenwidth() - width) / 2)
        y = round((self.winfo_screenheight() - height) / 2)
        coord = f"{width}x{height}+{x}+{y}"
        return coord

    def transform_data_to_dict(self):
        """Возвращает словарь с данными, введенными в форму."""
        return {
            "repeat": int(self.frame.repeat.get()),
            "mutation": int(self.frame.mutation.get()) / 100,
            "population": int(self.frame.population.get()),
            "rotations": int(self.frame.rotations.get())
        }

    def launch(self):
        """Запускает игру с передачей необходимых параметров."""
        self.withdraw()
        for _ in range(int(self.frame.repeat.get())):
            game = Game(self.transform_data_to_dict())
            game.run()

        self.destroy()