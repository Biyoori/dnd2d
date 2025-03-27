import os
import pygame
from exceptions.graphic_exceptions import InvalidImageError, MissingAssetError

def load_image(path: str, alpha: bool = True) -> pygame.Surface | None:
    print(path)
    if not os.path.exists(path):
        print("lololo")
        return None
        
    
    try: 
        surface = pygame.image.load(path)
        return surface.convert_alpha() if alpha else surface.convert()
    except MissingAssetError as e:
        print(f"Loading Error {path}: {str(e)}")
        return None
    except InvalidImageError as e:
        print(f"Invalid or damaged file: {e.path}")
        return None