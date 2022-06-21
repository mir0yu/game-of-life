import curses
import pathlib

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")
        screen.refresh()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i, g in enumerate(self.life.curr_generation):
            for j, v in enumerate(g):

                if v == 0:
                    try:
                        screen.addch(i + 1, j + 1, " ")
                    except (curses.error):
                        pass
                elif v == 1:
                    try:
                        screen.addch(i + 1, j + 1, "*")
                    except (curses.error):
                        pass
        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()  # type: ignore
        curses.cbreak()
        screen.keypad(True)
        screen.nodelay(True)
        curses.noecho()
        win = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_borders(win)
            self.draw_grid(win)
            key = screen.getch()
            if key == ord("q"):
                exit()
            if key == ord("s"):
                self.life.save(pathlib.Path("test.txt"))
            if key == ord("p"):
                state = "paused"
                while state == "paused":
                    key = screen.getch()
                    if key == ord("q"):
                        exit()
                    if key == ord("s"):
                        self.life.save(pathlib.Path("test.txt"))
                    if key == ord("p"):
                        state = "unpaused"
            self.life.step()
            curses.napms(1000)
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((25, 25), max_generations=10)
    ui = Console(life)
    ui.run()
