import os.path
from os import walk

import pygame


def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for img in sorted(img_files):
            surface_list.append(pygame.image.load(os.path.join(path, img)).convert_alpha())

    return surface_list
