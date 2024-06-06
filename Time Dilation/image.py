import pygame
import os

class Image:
    def __init__(self, image_path, position):
        super().__init__()
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"No such file or directory: '{image_path}'")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        