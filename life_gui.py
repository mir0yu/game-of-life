import pathlib

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 25, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode(
            (self.life.cols * self.cell_size, self.life.rows * self.cell_size)
        )

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows * self.cell_size)
            )
        for y in range(0, self.life.rows * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.life.cols * self.cell_size, y)
            )

    def draw_grid(self) -> None:
        for i, g in enumerate(self.life.curr_generation):
            for j, v in enumerate(g):
                if v == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    )
                elif v == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:
        # pylint: disable=no-member
        pygame.init()
        # pylint: enable=no-member
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        RUNNING, PAUSE = 0, 1
        state = RUNNING
        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # type: ignore
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        state = PAUSE
                    if event.key == pygame.K_c:
                        state = RUNNING
                    if event.key == pygame.K_s:
                        self.life.save(pathlib.Path("test_gui.txt"))
                if event.type == pygame.MOUSEBUTTONUP:
                    j, i = pygame.mouse.get_pos()
                    i = i // self.cell_size
                    j = j // self.cell_size
                    self.life.curr_generation[i][j] = int(not bool(self.life.curr_generation[i][j]))
            if state == RUNNING:
                # Выполнение одного шага игры (обновление состояния ячеек)
                self.life.step()
            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        # pylint: disable=no-member
        pygame.quit()
        # pylint: enable=no-member


if __name__ == "__main__":
    life = GameOfLife((10, 20), max_generations=50)
    game = GUI(life)
    game.run()
