""" Coursework 1: Bucket Fill
"""


def load_image(filename):
    """Load image from file made of 0 (unfilled pixels) and 1 (boundary pixels) and 2 (filled pixel)

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
    """Convert image representation into a human-friendly string representation

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
    """Show image in terminal.

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)
    """
    print(stringify_image(image))


def fill(image, seed_point):
    """Fill the image from seed point to boundary.

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
    # Extract row and col coordinates of the seed
    (row, col) = seed_point

    # Calculate num rows and cols of the image
    num_rows = len(image)
    num_cols = len(image[0])

    # Return original image if seed has non integer coordinates
    if not (isinstance(row, int) and isinstance(col, int)):
        return image

    # Return original image if seed has coordinates outside of the image
    is_inside_row = (0 <= row < num_rows)
    is_inside_col = (0 <= col < num_cols)
    if not (is_inside_row and is_inside_col):
        return image

    # Only fill current cell if it is unfilled
    is_unfilled = (image[row][col] == 0)
    if is_unfilled:
        # Fill current cell
        image[row][col] = 2

        # Apply fill function to all four adjacent cells
        image = fill(image, (row-1, col))
        image = fill(image, (row, col+1))
        image = fill(image, (row+1, col))
        image = fill(image, (row, col-1))

    return image


def create_square_image(n=25):
    """Write an image of zeros and an image of ones to separate files.

    Args:
        n (int) : size of the desired images

    Returns:
        tuple : (path_to_unfilled_image, path_to_filled_image) where each entry is a string
    """
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


def test_invalid_seed():
    """Check that the fill function returns the original image when given invalid seeds."""
    # Create a list of invalid seeds
    seed_list = [(1.5, 2), (-2, 0), ("myseed", 3)]
    image_input = load_image("data/bar.txt")

    # Check that the input image is returned with invalid seeds
    for seed in seed_list:
        image_output = fill(image=image_input, seed_point=seed)
        assert (image_input == image_output), f"Input seed {seed} should return the original image."


def test_image(image_path, image_expected_path, seed_point):
    """Check that the fill function returns the expected image.

    Args:
        image_path (str) : path to file containing the image representation
        image_expected_path (str) : path to file containing the expected image representation
        seed_point (tuple) : a 2-element tuple representing the (row, col)
                       coordinates of the seed point to start filling

    """
    image = load_image(image_path)
    image_expected = load_image(image_expected_path)

    print("Before filling:")
    show_image(image)

    image_filled = fill(image=image, seed_point=seed_point)

    print("-" * 25)
    print("After filling:")
    show_image(image_filled)

    print("Expected image:")
    show_image(image_expected)

    assert (image_filled == image_expected), "Your image does not look as expected!\n"
    print("Your image looks as expected!\n")


def test_large_image():
    """Check that the fill function returns the original image
    when given a large 25x25 image input.
    """
    # Create empty square image of size n
    n = 25
    (image_file, expected_image_file) = create_square_image(n)
    image = load_image(image_file)
    image_expected = load_image(expected_image_file)

    print("Before filling:")
    show_image(image)

    image_filled = fill(image=image, seed_point=(round(n/2), round(n/2)))

    print("-" * 25)
    print("After filling:")
    show_image(image_filled)

    print("Expected image:")
    show_image(image_expected)

    assert (image_filled == image_expected), "Your image does not look as expected!\n"
    print("Your image looks as expected!\n")


if __name__ == '__main__':
    # Test invalid seeds
    test_invalid_seed()

    # Test that a seed on the boundary returns the original image
    test_image("data/bar.txt", "data/bar.txt", (3, 7))

    # Test bar.txt image
    test_image("data/bar.txt", "data/expected_bar.txt", (7, 7))

    # Test smiley.txt image
    test_image("data/smiley.txt", "data/expected_smiley.txt", (7, 7))

    # Test snake image
    test_image("data/snake.txt", "data/expected_snake.txt", (6, 7))

    # Test large 25x25 image
    test_large_image()
