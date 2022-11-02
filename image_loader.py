"""
Takes in a filepath to a texture image and a dictionary of image names, and corner coordinates.
Returns a dictionary of pygame surfaces for each sprite.
"""
import pygame


def get_textures(image_path, image_index):
    """
    Function to take in the overall texture image and split it into images for each sprite according to the image index.

    Image index takes the format of a dictionary with the name of the texture as the key and a list of two corners as
    the value.


    Image index takes the form {"sprite_name":((corner_1x, corner_1y), (corner_2x, corner_2y))}
    :param image_path:
    :param image_index:
    :return sprites:
    """
    full_image = pygame.image.load(image_path)
    full_image = full_image.convert_alpha(full_image)
    sprites = {}

    for sprite in image_index:
        img_data = image_index[sprite]

        width = img_data[1][0] - img_data[0][0]
        height = img_data[1][1] - img_data[0][1]
        blit_pos = (-img_data[0][0], -img_data[0][1])

        sprite_image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        sprite_image.fill((0, 0, 0, 0))
        sprite_image.blit(full_image, blit_pos)
        sprite_image = sprite_image.convert_alpha(sprite_image)

        sprites[sprite] = sprite_image

    return sprites
