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
    try:
        result_image.save(path_to_result)
    except PermissionError:
        return False
    return True


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


def is_ratios_equal(width_one, height_one, width_two,
                               height_two, delta):
    return abs(width_one/height_one - width_two/height_two) <= delta


def check_validity_params(dir_to_result, width, height, scale):

    if not all(param > 0 for param in [width, height, scale] if param):
        return False, 'Параметр не может быть отрицательным числом'

    if scale and (width or height):
        return False, 'Параметры ширина и высота не задаются с параметром масштаб'

    if not (scale or width or height):
        return False, 'Не заполнен не один из параметров для ' \
                      'изменения размера изображения'

    if dir_to_result and not os.path.isdir(dir_to_result):
        return False, 'Путь к директории результата задан не верно'

    return True, None

def get_parser():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('path_file', help='Path to the image file')
    parser.add_argument('--width', type=int, help='Width new image')
    parser.add_argument('--height', type=int, help='Height new image')
    parser.add_argument('--scale', type=float, help='Image resizing factor')
    parser.add_argument(
        '--output', type=str,
        help='Path to the output file directory'
    )
    return parser


def main():

    delta = 0.001
    parser = get_parser()
    params = parser.pase_args()
    path_to_original = params.path_file
    dir_to_result = params.output
    width = params.width
    height = params.height
    scale = params.scale

    check_passed, error = check_validity_params(dir_to_result, width, height, scale)
    if not check_passed:
        parser.error(error)

    original_image = open_image(path_to_original)
    if not original_image:
        exit('Ошибка открытия файла изображения')

    result_image = resize_image(original_image, width, height, scale)

    width_result, height_result = result_image.size

    path_to_result = get_path_to_result(path_to_original, dir_to_result,
                                        width_result, height_result)

    if not save_image(result_image, path_to_result):
        exit('Не удалось записать файл')

    print('Измененное изображение {}'.format(path_to_result))

    width_original, height_original = original_image.size

    if not is_ratios_equal(width_original, height_original,
                                      width_result, height_result, delta):
        print('Пропорции изображения изменены')


if __name__ == '__main__':
    main()
