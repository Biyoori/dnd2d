import os
import pygame
from exceptions.graphic_exceptions import InvalidImageError, MissingAssetError
from debugging import logger

def load_image(path: str, alpha: bool = True) -> pygame.Surface | None:
    if not os.path.exists(path):
        return None
        
    
    try: 
        surface = pygame.image.load(path)
        return surface.convert_alpha() if alpha else surface.convert()
    except MissingAssetError as e:
        logger.log(f"Loading Error {path}: {str(e)}", "ERROR")
        return None
    except InvalidImageError as e:
        logger.log(f"Invalid or damaged file: {e.path}", "ERROR")
        return None