""" Coursework 1: Bucket Fill
"""

def load_image(filename):
    """ Load image from file made of 0 (unfilled pixels) and 1 (boundary pixels) and 2 (filled pixel)

    Example of content of filename:

0 0 0 0 1 1 0 0 0 0
0 0 1 1 0 0 1 1 0 0
0 1 1 0 0 1 0 1 1 0
1 1 0 0 1 0 1 0 1 1
1 0 0 1 0 0 1 0 0 1
1 0 0 1 0 0 1 0 0 1
1 1 0 1 0 0 1 0 1 1
0 1 1 0 1 1 0 1 1 0
0 0 1 1 0 0 1 1 0 0
0 0 0 0 1 1 0 0 0 0

    Args:
        filename (str) : path to file containing the image representation

    Returns:
        list : a 2D representation of the filled image, where
               0 represents an unfilled pixel,
               1 represents a boundary pixel
               2 represents a filled pixel
    """

    image = []
    with open(filename) as imagefile:
        for line in imagefile:
            if line.strip():
                row = list(map(int, line.strip().split()))
                image.append(row)
    return image


def stringify_image(image):
    """ Convert image representation into a human-friendly string representation

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)

    Returns:
        str : a human-friendly string representation of the image
    """
    
    if image is None:
        return ""

    # The variable "mapping" defines how to display each type of pixel.
    mapping = {
        0: " ",
        1: "*",
        2: "0"
    }

    image_str = ""
    if image:
        image_str += "_ " * (len(image[0]) + 2) + "\n"
    for row in image:
        image_str += "| "
        for pixel in row:
            image_str += mapping.get(pixel, "?") + " "
        image_str += "|"
        image_str += "\n"
    if image:
        image_str += "‾ " * (len(image[0]) + 2) + "\n"

    return image_str


def show_image(image):
    """ Show image in terminal

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)
    """
    print(stringify_image(image))


def fill(image, seed_point):
    """ Fill the image from seed point to boundary

    the image should remain unchanged if:
    - the seed_point has a non-integer coordinate
    - the seed_point is on a boundary pixel
    - the seed_point is outside of the image

    Args:
        image (list) : a 2D nested list representation of an image, where
                       0 represents an unfilled pixel, and
                       1 represents a boundary pixel
        seed_point (tuple) : a 2-element tuple representing the (row, col) 
                       coordinates of the seed point to start filling

    Returns:
        list : a 2D representation of the filled image, where
               0 represents an unfilled pixel,
               1 represents a boundary pixel, and
               2 represents a filled pixel
    """

    # TODO: Complete this function
    # Extract row and col coordinates of the seed
    row,col = seed_point

    # Calculate num rows and cols of the image
    num_rows = len(image)
    num_cols = len(image[0])

    # Return original image if seed has non integer coordinates
    if not (isinstance(row,int) and  isinstance(col,int)):
        # print("Seed does not contain integer coordinates. Returning original image.")
        return image
    
    # Return original image if seed has coordinates outside of the image
    is_inside_row = (0 <= row < num_rows)
    is_inside_col = (0 <= col < num_cols)
    if not (is_inside_row and is_inside_col):
        # print("Seed is outside of image. Returning original image.")
        return image

    # Only fill current cell if it is unfilled
    is_unfilled = (image[row][col] == 0)
    if is_unfilled:
        # Fill current cell
        image[row][col] = 2

        # Apply fill function to all four adjacent cells
        image = fill(image,(row-1,col))
        image = fill(image,(row,col+1))
        image = fill(image,(row+1,col))
        image = fill(image,(row,col-1)) 
    
    return image

def create_square_image(n=25):

    # Define path to unfilled image
    file_path_unfilled = "./data/" + "square_image_" + str(n) + ".txt"

    # Define path to expected filled image
    file_path_filled = "./data/" + "expected_" + "square_image_" + str(n) + ".txt"
    
    # Write image to file
    with open(file_path_unfilled, 'w') as f:
        line = n*"0 "+"\n"
        for i in range(n):
            f.write(line)

    # Write expected image to file
    with open(file_path_filled, 'w') as f:
        line = n*"2 "+"\n"
        for i in range(n):
            f.write(line)

    # Return path of created files
        return (file_path_unfilled, file_path_filled)

def example_fill():
    image = load_image("data/bar.txt")

    print("Before filling:")
    show_image(image)

    image = fill(image=image, seed_point=(7, 3))

    print("-" * 25)
    print("After filling:")
    show_image(image)

def example_fill_custom():
    image = load_image("data/smiley.txt")

    print("Before filling:")
    show_image(image)
    import random
    seed_point_random = (random.randint(0,len(image)),random.randint(0,len(image[0])))
    image = fill(image=image, seed_point=(7,7))

    print("-" * 25)
    print("After filling:")
    show_image(image)
def test_fill():
    test_image = [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1]]
    test_seed = (1,2)
    output_image = fill(test_image,test_seed)
    return output_image

def test_large_image(n=25):

    image_file,expected_image_file = create_square_image(n)
    image = load_image(image_file)
    image_expected = load_image(expected_image_file)

    print("Before filling:")
    show_image(image)

    image_filled = fill(image=image, seed_point=(round(n/2), round(n/2)))

    print("-" * 25)
    print("After filling:")
    show_image(image_filled)
    
    if image_filled == image_expected:
        print("Your image looks as expected!")
        return True
    else:
        print("Your image does not look as expected!")
        return False      



if __name__ == '__main__':
    #example_fill_custom()
    test_large_image(28)
