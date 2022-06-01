from PIL import Image


def find_square(image: Image.Image, max_length: int = 10) -> list[int]:  # returns a list of the size of the squares
    """
    Finds the size of the squares present in the image.
    :param image: image object to process.
    :param max_length: maximum number of square to find.
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
            if len(square_list) == max_length:
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
    square_list = find_square(image)  # find
    pixel_width = most_frequent(square_list)

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

    # created a new blank image
    fixed_img = Image.new(
        mode='RGBA',
        size=(new_width // pixel_width, new_height // pixel_width)
    )
    fixed_img_px = fixed_img.load()

    # copy pixels of the original image
    xi = 0
    for x in range(fixed_img.width):
        yi = 0
        for y in range(fixed_img.height):
            fixed_img_px[x, y] = image_px[xi, yi]
            yi += pixel_width
        xi += pixel_width

    # save the image if :param save: is True
    if save:
        new_file_name = "resized_" + file_name + ".png"
        fixed_img.save(new_file_name)
        print(f"{new_file_name} created !\n")

    return fixed_img


def most_frequent(input_list):
    """
    Returns the most frequent value in the list.
    :param input_list: list to process.
    :return: most frequent value.
    """
    counter = 0
    num = input_list[0]

    for element in input_list:
        curr_frequency = input_list.count(element)
        if curr_frequency > counter:
            counter = curr_frequency
            num = element

    return num
