import os


class GraphicsError(Exception):
    pass

class MissingAssetError(GraphicsError):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Asset not found: {path}")

class InvalidImageError(GraphicsError):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Invalid image file: {path}")