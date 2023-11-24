import time
import pygame
from helpers import (
    itr_add,
)  # type:ignore
from pygame import (
    draw as pgDraw,
    mouse as pgMouse,
)
from utils import (  # type:ignore
    Colors,
    PlayAudio,
    Window,
    BoundingBox,
    State,
)

SPEAKER = PlayAudio()


def place_pieces(grid: list[list[str]], window: Window, box: BoundingBox):
    padding = 10
    max_area = (box.width) if box.width < box.height else box.height
    for x_indx, i in enumerate(grid):
        for y_indx, j in enumerate(i):
            pos = box.pos_from_index(x_indx, y_indx)
            if j == "X":
                pgDraw.line(
                    window.screen,
                    [255, 0, 255],
                    itr_add(pos, [padding]),
                    itr_add(pos, [box.width - padding, box.height - padding]),
                    5,
                )
                pgDraw.line(
                    window.screen,
                    [255, 0, 255],
                    itr_add(pos, [box.width - padding, padding]),
                    itr_add(pos, [padding, box.height - padding]),
                    5,
                )

            elif j == "O":
                radius = (max_area - padding) // 2
                pgDraw.circle(window.screen, [255, 0, 0], itr_add(pos, [box.width // 2, box.height // 2]), radius, 5)


def chart(grid: list[list[str]], window: Window, cols=3, rows: int = 3) -> BoundingBox:
    start_pos = int(0), window.header_size
    end_pos = window.width, window.height
    width = (end_pos[0] - start_pos[0]) // cols
    height = (end_pos[1] - start_pos[1]) // rows

    box = BoundingBox(start_pos, end_pos, width, height)
    # vertical
    for i in range(cols):
        pgDraw.line(
            window.screen,
            BLACK,
            [start_pos[0] + (i * width), start_pos[1]],
            [start_pos[0] + (i * width), start_pos[1] + (rows * height)],
            3,
        )
    # horizontal
    for i in range(rows):
        pgDraw.line(
            window.screen,
            BLACK,
            [start_pos[0], start_pos[1] + (i * height)],
            [end_pos[0], start_pos[1] + (i * height)],
            3,
        )
    place_pieces(grid, window, box)

    return box


def horizontal(grid: list[list[str]]) -> tuple[State, str]:
    _s: tuple[State, str] = (State.CON, "")
    for row, items in enumerate(grid):
        if grid[row][0] and all([x == grid[row][0] for x in items]):
            return (State.WON, f"{grid[row][0]}")
    return _s


def vertical(grid: list[list[str]]) -> tuple[State, str]:
    _s: tuple[State, str] = (State.CON, "")
    for col, item in enumerate(grid[0]):
        if item and all([x[col] == item for x in grid]):
            return (State.WON, f"{item}")
    return _s


def diagonal(grid: list[list[str]]) -> tuple[State, str]:
    _s: tuple[State, str] = (State.CON, "")
    if grid[0][0] and all([x[n] == grid[0][0] for n, x in enumerate(grid)]):
        return (State.WON, f"{grid[0][0]}")
    elif grid[0][-1] and all([x[-1 - n] == grid[0][-1] for n, x in enumerate(grid)]):
        return (State.WON, f"{grid[0][-1]}")
    return _s


def display_state(window: Window, state: State, player: str, /) -> None:
    offset = 30
    state_msg = "WON" if state == State.WON else "TIE"
    state_message = "[{}] {} the Other".format(player, state_msg)
    retry_message = "(q to quit, click to playagain)"
    state_text_surface = window.font.render(state_message, True, BLACK)
    retry_text_surface = window.font.render(retry_message, True, BLACK)
    (f_w, f_h) = state_text_surface.get_size()
    (r_w, r_h) = state_text_surface.get_size()
    d_h = f_h + r_h + offset
    pgDraw.line(
        window.screen,
        (255, 0, 0),
        (0, (window.height // 2) - (f_h * 2)),
        (window.width, (window.height // 2) - (f_h * 2)),
        d_h * 2,
    )
    window.screen.blit(state_text_surface, (window.width // 2 - (f_w // 2), (window.height // 2) - (f_h * 2)))
    window.screen.blit(retry_text_surface, (window.width // 2 - (r_w // 2), ((window.height // 2) - (f_h))))
    SPEAKER.play("win.wav", volume=50, fadeout=1000)


def mtch_fixer(grid: list[list[str]]) -> tuple[State, str]:
    winner: str = ""
    # horizontal
    state, winner = horizontal(grid)
    if state == State.WON:
        return state, winner
    # veritcal
    state, winner = vertical(grid)
    if state == State.WON:
        return state, winner
    # diagonal
    state, winner = diagonal(grid)
    if state == State.WON:
        return state, winner
    return state, ""


def plotter(grid: list[list[str]], player: str, window: Window, box: BoundingBox) -> tuple[State, str]:
    index = box.index_of(*pgMouse.get_pos())

    if grid[index[0]][index[1]]:
        print("invalid location choose next location")
        SPEAKER.play("invalid.mp3", volume=30, fadeout=1000)
        return State.INV, player

    grid[index[0]][index[1]] = player
    SPEAKER.play("hacker.wav", volume=50, fadeout=1000)
    place_pieces(grid=grid, window=window, box=box)
    return mtch_fixer(grid)


if __name__ == "__main__":
    BLACK = (0, 0, 0)
    WHITE = [255, 255, 255]
    TURN = time.time_ns() % 2
    RUN = True
    PLAYER = ["O", "X"]
    GRID = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
    ]

    WINDOW = Window(width=400, height=400, caption="TicTacToe")
    WINDOW.load_font()
    FPS: int = 60
    COMPLETED = False
    board = BoundingBox((0, 0), (0, 0), 0, 0)
    pygame.mixer_music.load("lol1.wav")
    pygame.mixer_music.play()
    while RUN == True:
        if not COMPLETED:
            WINDOW.screen.fill([255, 255, 255])
            board = chart(GRID, WINDOW, len(GRID), len(GRID[0]))
            WINDOW.header(f"{PLAYER[TURN % 2]}'s TURN....")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                print("quit")
            elif event.type == pygame.KEYDOWN and (event.dict.get("unicode", "").lower() == "q"):
                RUN = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not COMPLETED:
                player = PLAYER[TURN]
                (state, player) = plotter(GRID, player, WINDOW, board)
                if state != State.CON:
                    COMPLETED = True
                    GRID = [
                        ["", "", ""],
                        ["", "", ""],
                        ["", "", ""],
                    ]
                    display_state(WINDOW, state, player)
                elif state == State.CON:
                    TURN ^= 1
            elif event.type == pygame.MOUSEBUTTONDOWN and COMPLETED:
                COMPLETED = False
            elif event.type == pygame.WINDOWRESIZED:
                WINDOW.update()
        pygame.display.update()
        time.sleep(1 / FPS)
