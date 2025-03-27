from ui.radial_menu.components.icon import ImageIcon
from ui.radial_menu.components.sector import RadialSector


class SectorFactory:
    @staticmethod
    def create_attack_sector() -> RadialSector:
        return RadialSector("Assets/UI/Rand_Menu/Sectors/rand_menu_sector1.png")
    
    @staticmethod
    def create_magic_sector() -> RadialSector:
        return RadialSector("Assets/UI/Rand_Menu/Sectors/rand_menu_sector2.png")