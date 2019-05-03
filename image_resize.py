import argparse
from PIL import Image
import os


def get_path_to_result(path_to_original, dir_to_result, width, height):

    old_dir, old_file = os.path.split(path_to_original)
    old_name, ext = os.path.splitext(old_file)
    new_name = '{}__{}x{}{}'.format(old_name, width, height, ext)

    if dir_to_result:
        new_dir = dir_to_result
    else:
        new_dir = old_dir

    return os.path.join(new_dir, new_name)


def open_image(path_to_original):

    try:
        original_image = Image.open(path_to_original)
    except OSError:
        return False

    return original_image


def save_image(result_image, path_to_result):
    result_image.save(path_to_result)


def get_ration_changes(original_size, new_size):
    ratio = (new_size / float(original_size))
    return ratio


def resize_image(original_image, width=None, height=None, scale=None):

    original_width, original_height = original_image.size
    if width and height:
        new_size = (width, height)
    elif scale:
        new_size = (
            int(original_width * scale),
            int(original_height * scale)
        )
    elif width:
        ratio = get_ration_changes(original_width, width)
        new_size = (width, int(original_height * ratio))
    else:
        ratio = get_ration_changes(original_height, height)
        new_size = (int(original_width * ratio), height)

    return original_image.resize(new_size)


def compare_images_proportions(width_one, height_one, width_two,
                               height_two, delta):
    if abs(width_one/height_one - width_two/height_two) <= delta:
        return True
    else:
        return False


def check_validity_params(dir_to_result, width, height, scale):

    if not all(param > 0 for param in [width, height, scale] if param):
        exit('Параметр не может быть отрицательным числом')

    if scale and (width or height):
        exit('Параметры ширина и высота не задаются с параметром масштаб')

    if not (scale or width or height):
        exit('Не заполнен не один из параметров для '
             'изменения размера изображения')

    if dir_to_result and not os.path.isdir(dir_to_result):
        exit('Путь к директории результата задан не верно')


def get_params():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('path_file', help='Path to the image file')
    parser.add_argument('--width', type=int, help='Width new image')
    parser.add_argument('--height', type=int, help='Height new image')
    parser.add_argument('--scale', type=float, help='Image resizing factor')
    parser.add_argument(
        '--output', type=str,
        help='Path to the output file directory'
    )
    return parser.parse_args()


def main():

    delta = 0.001

    params = get_params()
    path_to_original = params.path_file
    dir_to_result = params.output
    width = params.width
    height = params.height
    scale = params.scale

    check_validity_params(dir_to_result, width, height, scale)

    original_image = open_image(path_to_original)
    if not original_image:
        exit('Ошибка открытия файла изображения')

    result_image = resize_image(original_image, width, height, scale)

    width_result, height_result = result_image.size

    path_to_result = get_path_to_result(path_to_original, dir_to_result,
                                        width_result, height_result)

    save_image(result_image, path_to_result)

    print('Измененное изображение {}'.format(path_to_result))

    width_original, height_original = original_image.size

    if not compare_images_proportions(width_original, height_original,
                                      width_result, height_result, delta):
        print('Пропорции изображения изменены')


if __name__ == '__main__':
    main()
