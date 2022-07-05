from csv import reader
from settings import tile_size
from os import walk
import pygame


def import_folder(path):
    surface_list = []

    # the _ and __ means you don't care whats being returned. usually they are folder, sub_folders
    # image_files are all the png pictures
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:  # storing all csv into map
        # csv data, delimiter(what you are using to separate data(which is a comma))
        level = reader(map, delimiter=',')
        for row in level:
            # convert row to a list then append to terrain_map
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()  # grab the image
    # slice each image [0] is the width / 64
    tile_num_x = int(surface.get_size()[0] / tile_size)
    # slice each image [1] is the height / 64
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    # don't need enumerate because tile_nums are already numbers
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface(  # create a new surface that is 64x64 pixels
                (tile_size, tile_size), flags=pygame.SRCALPHA)  # SRCALPHA sets the pixels that aren't being used invisible
            new_surf.blit(surface, (0, 0), pygame.Rect(
                x, y, tile_size, tile_size))  # pygame.Rect will be a mask
            cut_tiles.append(new_surf)  # add it to list

    return cut_tiles  # return the list
