import pygame

screen_width, screen_height = 1280, 720
framerate = 60
font_path = "Assets/UI/Fonts/IM_Fell_DW_Pica/IMFellDWPica-Regular.ttf"

COLOR_PALETTE = {
    "black": (0,0,0,),
    "white": (255,255,255),
    "gray": (100,100,100),
    "red": (248, 156, 116, 255),
    "blue": (102, 197, 204, 255),
    "green": (135, 197, 95, 255),
    "light-gray": (200,200,200),
    "dark-gray": (26,26,26,217),
    "gold": (224, 214, 181),
    "yellow": (255, 255, 0),
    "silver": (192, 192, 192, 255),
    "dim-gray": (105, 105, 105, 255),
    "charcoal": (54, 54, 54, 255)
    
}

def get_color(color) -> tuple[int, int, int]:
    return COLOR_PALETTE[color]
