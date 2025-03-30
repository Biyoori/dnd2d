import pygame

screen_width, screen_height = 1280, 720
framerate = 60

COLOR_PALETTE = {
    "black": (0,0,0),
    "white": (255,255,255),
    "gray": (100,100,100),
    "red": (248, 156, 116),
    "blue": (102, 197, 204),
    "green": (135, 197, 95),
    "light-gray": (200,200,200),
    "gold": (224, 214, 181)
}

def get_color(color) -> tuple[int, int, int]:
    return COLOR_PALETTE[color]
