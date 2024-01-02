from csv import reader
import pygame
import os


def import_csv_map(path):
    '''Загружает и делает из csv карту, как матрицу.'''
    result_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            result_map.append(list(row))
    return result_map


def import_folder_images(path):
    '''Из папки достаёт изображения и возвращает список их.'''
    surface_list = []
    for _, _, image_files in os.walk(path):
        for name_image in image_files:
            full_path = path + '/' + name_image
            image = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image)
    return surface_list


def import_folder_folder(path):
    '''Из папки достаёт папку и возвращает список их.'''
    folders = [path + '/' + f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return folders
