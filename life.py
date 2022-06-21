import copy
import pathlib
import random
import typing as tp

# import numpy as np
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for j in range(self.cols)] for i in range(self.rows)]
        return [[0 for j in range(self.cols)] for i in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        neighbours = []

        for i in range(y - 1, y + 2):
            if i < 0 or i >= self.rows:
                continue
            for j in range(x - 1, x + 2):
                if j < 0 or j >= self.cols:
                    continue
                neighbours.append(self.curr_generation[i][j])
        neighbours.remove(self.curr_generation[y][x])

        return neighbours

    def get_next_generation(self) -> Grid:
        next_grid = copy.deepcopy(self.curr_generation)
        for i, g in enumerate(self.curr_generation):
            for j, v in enumerate(g):
                neighbours = self.get_neighbours((i, j))
                count = 0
                if neighbours:
                    for n in neighbours:
                        if n:
                            count = count + 1
                    if v:
                        if count in (2, 3):
                            next_grid[i][j] = 1
                        else:
                            next_grid[i][j] = 0
                    else:
                        if count == 3:
                            next_grid[i][j] = 1
        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            if self.generations < self.max_generations:
                return False
        return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        data = []
        rows = 0
        with open(filename, "r") as f:
            for line in f:
                for i in line.split():
                    values = []  # type: ignore
                    cols = 0
                    for j in i:
                        values.append(int(j))
                        cols += 1
                    if values:
                        data.append(values)
                        rows += 1
        size = (rows, cols)
        life = GameOfLife(size)
        life.curr_generation = data
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for line in self.curr_generation:
                for i in line:
                    f.write(str(i))
                f.write("\n")
            f.close()
