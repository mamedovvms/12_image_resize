# -*- coding: utf-8 -*-

import argparse
from PIL import Image
import os


def get_path_to_result(path_to_original, path_to_result, result_images):
    if path_to_result:
        return path_to_result

    new_width, new_height = result_images.size
    root, ext = os.path.splitext(path_to_original)

    return '{}__{}x{}{}'.format(root, new_width, new_height, ext)


def resize_image(path_to_original, path_to_result, width, height):

    original_images = Image.open(path_to_original)
    original_width, original_height = original_images.size
    result_images = original_images.resize((width, height))
    path_to_result = get_path_to_result(path_to_original,
                                        path_to_result, result_images)
    result_images.save(path_to_result)

    return original_width/original_height == width/height


def scaling_image(path_to_original, path_to_result,
                  width=None, height=None, scale=None):

    original_images = Image.open(path_to_original)
    original_width, original_height = original_images.size
    if scale:
        supposed_new_size = (
            int(original_width * scale),
            int(original_height * scale)
        )
    elif width:
        supposed_new_size = (width, original_height)
    else:
        supposed_new_size = (original_width, height)

    original_images.thumbnail(supposed_new_size)
    path_to_result = get_path_to_result(path_to_original,
                                        path_to_result, original_images)
    original_images.save(path_to_result)


def get_cons_params():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('path_file', help='Path to the image file')
    parser.add_argument('--width', type=int, help='Width new image')
    parser.add_argument('--height', type=int, help='Height new image')
    parser.add_argument('--scale', type=float, help='Image resizing factor')
    parser.add_argument('--output', type=str,  help='Image resizing factor')
    return parser.parse_args()


def main():
    params = get_cons_params()
    path_to_original = params.path_file
    path_to_result = params.output
    width = params.width
    height = params.height
    scale = params.scale

    if scale and (width or height):
        exit('Параметры ширина и высота не задаются с параметром масштаб')
    if not(scale or width or height):
        exit('Не заполнен не один из параметров размера и масштаба')
    try:
        if width and height:
            proportions_preserved = resize_image(path_to_original,
                                                 path_to_result, width, height)
            if not proportions_preserved:
                print('Пропорции не сохранены')
        else:
            if scale < 0:
                exit('Масштаб не может быть меньше нуля')
            scaling_image(path_to_original, path_to_result, width, height, scale)
    except OSError:
        print('Файл не является картинкой')

if __name__ == '__main__':
    main()
