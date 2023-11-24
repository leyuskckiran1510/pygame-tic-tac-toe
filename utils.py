import pygame
from enum import Enum
from typing import Sequence
from pygame import (
    draw as pgDraw,
    mixer as pgMixer,
)


class Colors:
    BLACK = [0, 0, 0]


class PlayAudio:
    MUSIC_END = -1
    MUSIC_STOPPED = 0

    def __init__(self, channel=5) -> None:
        self.channel = channel
        self.sounds = {}
        pgMixer.init(channels=channel)

    def get_sound(self, name: str) -> pygame.mixer.Sound:
        sound = self.sounds.get(name, None)
        if not sound:
            sound = pgMixer.Sound(file=name)
            self.sounds[name] = sound
        return sound

    def load_sound(self, filename: str):
        self.get_sound(filename)

    def did_end(self):
        for i in range(self.channel):
            channel = pgMixer.Channel(i)
            if channel.get_endevent() == PlayAudio.MUSIC_END:
                channel.set_endevent(PlayAudio.MUSIC_STOPPED)
                channel.stop()

    def play(self, filename, volume=40, fadeout=500):
        self.did_end()
        sound = self.get_sound(filename)
        avilable_channel = pygame.mixer.find_channel()
        if avilable_channel:
            avilable_channel.play(sound)
            avilable_channel.set_volume(volume)
            avilable_channel.fadeout(fadeout)
            avilable_channel.set_endevent(PlayAudio.MUSIC_END)
        else:
            pgMixer.Channel(0).queue(sound)


class Window:
    def __init__(self, width: int = 400, height: int = 400, caption: str = "this is window") -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(caption)
        self.width: int = width
        self.height: int = height
        self.header_size: int = 100
        self.screen: pygame.Surface = pygame.display.set_mode([width, height], pygame.RESIZABLE)

    def load_font(self, font_name: str = "Comic Sans MS") -> None:
        self.font = pygame.font.SysFont(font_name, 30)

    def header(self, text: str, header_size: int = 100) -> None:
        self.header_size = header_size
        pgDraw.line(self.screen, (255, 0, 0), (0, 0), (self.width, 0), self.header_size)
        textsurface = self.font.render(text, True, Colors.BLACK)
        (f_w, f_h) = textsurface.get_size()
        self.screen.blit(textsurface, (self.width // 2 - (f_w // 2), (self.header_size // 2) - (f_h * 1.5)))

    def update(self):
        self.width, self.height = self.screen.get_size()
        self.header_size = int(self.height * 0.1)  # 10%


class BoundingBox:
    def __init__(self, start_pos: Sequence[int], end_pos: Sequence[int], width: int, height: int) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.height = height

    def is_inside(self, x: int, y: int) -> bool:
        return x >= self.start_pos[0] and x <= self.end_pos[0] and y >= self.start_pos[1] and y <= self.end_pos[1]

    def index_of(self, x: int, y: int) -> tuple[int, int]:
        if not self.is_inside(x, y):
            return -1, -1
        return (x - self.start_pos[0]) // self.width, (y - self.start_pos[1]) // self.height

    def pos_from_index(self, x_indx: int, y_indx: int) -> list[int]:
        return [
            self.start_pos[0] + (self.width * x_indx),
            self.start_pos[1] + (self.height * y_indx),
        ]


class State(Enum):
    CON = 0
    TIE = 1
    WON = 2
    INV = 3
