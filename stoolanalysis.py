from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def get_pixel_intensity(image, x, y):
    # Get the RGB values of the pixel at the specified coordinate
    r, g, b = image.getpixel((x, y))
    # Normalize the RGB values and return as a list
    return [r / 255, g / 255, b / 255]


def split_rgb(image_path):
    # Open the image
    img = Image.open(image_path)

    # Check if the image mode is RGB
    if img.mode != 'RGB':
        raise ValueError("Image mode must be JPG")

    # Split the image into red, green, and blue channels
    r, g, b = img.split()

    # Create zero-filled images for other channels
    zero_array = Image.new("L", img.size, 0)

    # Merge each channel with zero-filled channels to create a full-color image
    red_img = Image.merge("RGB", (r, zero_array, zero_array))
    green_img = Image.merge("RGB", (zero_array, g, zero_array))
    blue_img = Image.merge("RGB", (zero_array, zero_array, b))

    return red_img, green_img, blue_img


# Example usage:
image_path = r"C:\Users\alexg\OneDrive\Stanford\Research\highcontrastshrek.jpg"
try:
    red_channel, green_channel, blue_channel = split_rgb(image_path)
except ValueError as e:
    print(e)
    exit()

# Plot the original full-color image
plt.figure(figsize=(8, 6))
original_image = Image.open(image_path)
plt.imshow(original_image)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Select Pixel(s) on the Original Full-Color Image')

# Use ginput to select the pixels
selected_points = plt.ginput(n=6, timeout=0)

# Close the figure after selecting the pixel
plt.close()

# Get the intensity of the selected pixels for each channel
intensities = []
for point in selected_points:
    pixel_x, pixel_y = int(point[0]), int(point[1])
    red_intensity = get_pixel_intensity(red_channel, pixel_x, pixel_y)
    green_intensity = get_pixel_intensity(green_channel, pixel_x, pixel_y)
    blue_intensity = get_pixel_intensity(blue_channel, pixel_x, pixel_y)
    intensities.append((pixel_x, pixel_y, red_intensity, green_intensity, blue_intensity))

# Define colors for each selected pixel
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'magenta']



# Plot the intensity vs wavelength figure as a line graph
plt.figure(figsize=(8, 6))
for i, (_, _, red_intensity, green_intensity, blue_intensity) in enumerate(intensities):
    plt.plot(['Red', 'Green', 'Blue'], [red_intensity[0], green_intensity[1], blue_intensity[2]], marker='o',
             linestyle='-', color=colors[i], label=f'Pixel {i + 1}')
plt.ylim(0, 1)  # Set y-axis limits from 0 to 1
plt.xlabel('Color Channel')
plt.ylabel('Intensity')
plt.title('Intensity at Red, Green, and Blue Wavelengths for Selected Pixels')
plt.legend()
plt.grid(True)
# Plot the original full-color image with pixel locations marked
plt.figure(figsize=(8, 6))
plt.imshow(original_image)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Pixel(s) on the Original Full-Color Image')

# Mark selected pixels on the image
for point, color in zip(selected_points, colors):
    plt.scatter(point[0], point[1], color=color, s=5)


# Define the color channel positions for Red, Green, Blue
color_positions = np.array([0, 1, 2])

plt.figure(figsize=(10, 8))

color_labels = ['Red', 'Green', 'Blue']

# Iterate over the intensities to fit a quadratic function and calculate curvature
for i, (pixel_x, pixel_y, red_intensity, green_intensity, blue_intensity) in enumerate(intensities):
    # Intensity values for the quadratic fit
    intensity_values = np.array([red_intensity[0], green_intensity[1], blue_intensity[2]])

    # Fit the quadratic function
    coefficients = np.polyfit(color_positions, intensity_values, 2)
    a, b, c = coefficients

    # Generate a smooth range of x values for plotting the quadratic curve
    x_smooth = np.linspace(color_positions[0], color_positions[-1], 100)
    # Calculate the y values of the quadratic curve
    y_smooth = a * x_smooth ** 2 + b * x_smooth + c

    # Plot the intensity points without labels
    plt.scatter(color_positions, intensity_values, marker='o', color='black')

    # Plot the quadratic fit curve with the corresponding color and label
    plt.plot(x_smooth, y_smooth, color=colors[i], label=f'Pixel {i + 1} Quadratic Fit')

    # Optional: print the curvature information
    curvature = 2 * a
    print(f"Point {i + 1} - ({pixel_x}, {pixel_y}):")
    print(f"  Curvature (Quadratic Fit): {curvature}")



plt.xticks(color_positions, color_labels)  # Set the x-axis labels to color names
plt.ylim(0, 1)  # Ensure the y-axis ranges from 0 to 1 as intensities are normalized
plt.xlabel('Color Channel')
plt.ylabel('Intensity')
plt.title('Quadratic Curve Fits for Selected Pixel Intensities')
plt.legend()
plt.grid(True)
plt.show()

# Save the modified image
plt.savefig('original_image_with_pixels_marked.jpg')


# Get the intensity of the selected pixels for each channel
intensities = []
for point in selected_points:
    pixel_x, pixel_y = int(point[0]), int(point[1])
    red_intensity = get_pixel_intensity(red_channel, pixel_x, pixel_y)
    green_intensity = get_pixel_intensity(green_channel, pixel_x, pixel_y)
    blue_intensity = get_pixel_intensity(blue_channel, pixel_x, pixel_y)
    intensities.append((pixel_x, pixel_y, red_intensity, green_intensity, blue_intensity))