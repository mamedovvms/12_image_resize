import argparse
from PIL import Image
import os


def get_path_to_result(path_to_original, path_to_result, result_images):
    if path_to_result:
        dir_to_result = os.path.dirname(path_to_result)
        if os.path.isdir(dir_to_result):
            return path_to_result

    new_width, new_height = result_images.size
    root, ext = os.path.splitext(path_to_original)

    return '{}__{}x{}{}'.format(root, new_width, new_height, ext)


def resize_image(path_to_original, path_to_result,
                 width=None, height=None, scale=None):

    original_image = Image.open(path_to_original)
    proportions_saved = True
    if width and height:
        result_image = original_image.resize((width, height))
        original_width, original_height = original_image.size
        proportions_saved = original_width/original_height == width/height
    else:
        result_image = scaling_image(original_image, width, height, scale)

    path_to_result = get_path_to_result(path_to_original,
                                        path_to_result, result_image)

    result_image.save(path_to_result)

    return proportions_saved


def scaling_image(original_image, width=None, height=None, scale=None):

    original_width, original_height = original_image.size

    if scale:
        supposed_new_size = (
            int(original_width * scale),
            int(original_height * scale)
        )
    elif width:
        supposed_new_size = (width, original_height)
    else:
        supposed_new_size = (original_width, height)

    original_image.thumbnail(supposed_new_size)
    return original_image


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

    for param in (width, height, scale):
        if param and param < 0:
            exit('Параметр не может быть меньше нуля')

    try:
        proportions_saved = resize_image(path_to_original, path_to_result, width, height, scale)
    except OSError:
        print('Файл не является картинкой')

    if not proportions_saved:
        print('Пропорции изображения изменены')


if __name__ == '__main__':
    main()
