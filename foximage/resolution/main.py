from PIL import Image
import os
import glob
from multiprocessing import Process


def find_square(image: Image.Image) -> list[int]:  # returns a list of the size of the squares
    """
    Finds the size of the squares present in the image.
    :param image: image object to process.
    :return: list of the size of the squares.
    """
    square_list = []
    for y in range(round(image.height * 1 / 4), round(image.height * 3 / 4)):
        for x in range(round(image.width * 1 / 4), round(image.width * 3 / 4)):
            cy = y
            cx = x
            ly1 = 0
            lx1 = 0
            ly2 = 0
            lx2 = 0

            while cy + 1 < image.height and image.getpixel((cx, cy)) == image.getpixel((cx, cy + 1)):
                cy += 1
                ly1 += 1

            while cx + 1 < image.width and image.getpixel((cx, cy)) == image.getpixel((cx + 1, cy)):
                cx += 1
                lx1 += 1
            else:
                if lx1 == ly1:
                    pass
                else:
                    continue

            while cy - 1 >= 0 and image.getpixel((cx, cy)) == image.getpixel((cx, cy - 1)):
                cy -= 1
                ly2 += 1
            else:
                if ly2 == ly1:
                    pass
                else:
                    continue

            while cx - 1 >= 0 and image.getpixel((cx, cy)) == image.getpixel((cx - 1, cy)):
                cx -= 1
                lx2 += 1
            else:
                if lx2 == ly1:
                    pass
                else:
                    continue
            square_list.append(ly1 + 1)
            if len(square_list) == 10:
                return square_list
    return square_list


def fix(image: Image.Image, save: bool = False, file_name: str = "image") -> Image.Image:
    """
    Fixes the resolution of the image.
    :param image: image to fix.
    :param save: if True, saves the image.
    :param file_name: output file name.
    :return: fixed image.
    """
    process_pid = os.getpid()
    square_list = find_square(image)
    pixel_width = most_frequent(square_list)

    print(f"Process {process_pid} is running.\n")

    if pixel_width == 1:
        print(f"{file_name} is already at the right resolution.\n")
        return image

    new_width, new_height = image.size
    if image.width % pixel_width > 0:
        new_width -= image.width % pixel_width
    if image.height % pixel_width > 0:
        new_height -= image.height % pixel_width
    cropped_image = image.crop((0, 0, new_width, new_height))

    image_px = cropped_image.load()

    fixed_img = Image.new(
        mode='RGBA',
        size=(new_width // pixel_width, new_height // pixel_width)
    )
    fixed_img_px = fixed_img.load()

    xi = 0
    for x in range(fixed_img.width):
        yi = 0
        for y in range(fixed_img.height):
            fixed_img_px[x, y] = image_px[xi, yi]
            yi += pixel_width
        xi += pixel_width

    if save:
        new_file_name = "resized_" + file_name + ".png"
        fixed_img.save(new_file_name)
        print(f"{new_file_name} created !\n")

    print(f"Process {process_pid} is done.")

    return fixed_img


def most_frequent(input_list):
    """
    Returns the most frequent value in the list.
    :param input_list: list to process.
    :return: most frequent value.
    """
    counter = 0
    num = input_list[0]

    for i in input_list:
        curr_frequency = input_list.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i

    return num


# FIXME:
if __name__ == '__main__':  # if we're running file directly and not importing it as a module
    while True:
        inp = input("""Convert an specific file (1) or every image in this directory (2) ?
        >> """)
        if inp == "1":
            path = input("""Path of the image/folder
    >> """)
            try:
                img = Image.open(path)
            except Exception as e:
                input(e)
            else:
                fix(image=img, file_name=path, save=True)

        elif inp == "2":
            processes = []
            ext = str
            while True:
                ext = input("Extention des images ?\n\t>> ")
                if ext not in ['png', 'jpg']:
                    os.system('cls')
                    print("Extention not supported.\n")
                else:
                    break

            for filename in glob.glob(f'*.{ext}'):
                img = Image.open(filename)
                p = Process(target=fix, args=(img, True, filename))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            else:
                input("Everything done !")
                exit(0)
        else:
            os.system('cls')
