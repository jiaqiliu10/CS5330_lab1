# Jiaqi Liu
# Pingqi An
# CS 5330 lab1
# 09/30/2024

import cv2
import numpy as np
from PIL import Image
import gradio as gr

# Create an ASCII character set
ASCII_SYMBOLS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Convert the images to grayscale
def convert_to_grayscale(uploaded_img):
    gray_image = cv2.cvtColor(np.array(uploaded_img), cv2.COLOR_BGR2GRAY)
    return gray_image

# Enhance the contrast of the image and improve the detail in the image
def improve_image_details(gray_img):
    enhanced_image = cv2.normalize(gray_img, None, 0, 255, cv2.NORM_MINMAX)
    return enhanced_image

# Converts the input image to ASCII character art
def pixels_to_ascii(img_data, max_width=100):
    # Extract the height and width of the image
    img_height, img_width = img_data.shape[:2]
    # Calculate the ratio of height to width of the image
    aspect_ratio = img_height / img_width
    # Make sure the adjusted width does not exceed the original image
    new_width = min(max_width, img_width)
    # Calculate the scaled height based on the aspect ratio of the image
    new_height = int(aspect_ratio * new_width * 0.55)
    
    # Scale to the specified size using new width and new height
    scaled_image = cv2.resize(img_data, (new_width, new_height))

    # Initializes an empty list for storing the generated ASCII art lines
    ascii_art_result = []
    i = 0
    # Using a while loop to iterate through each row of the image
    while i < len(scaled_image):
        row = scaled_image[i]
        ascii_row = []
        j = 0
        # Using a while loop to iterate through each pixel in the row
        while j < len(row):
            pixel = row[j]
            ascii_row.append(ASCII_SYMBOLS[pixel // 25])
            j += 1
        # Append the ASCII string of the row to the result list
        ascii_art_result.append("".join(ascii_row))
        i += 1

    # Return the final ASCII art joined with newlines
    return "\n".join(ascii_art_result)

# Calculate brightness difference between original and ASCII image
def calculate_brightness_difference(original_img, ascii_img_content):
    original_brightness = np.mean(original_img)
    
    # Map ASCII characters to brightness levels
    ascii_brightness = []
    for line in ascii_img_content.splitlines():
        ascii_brightness.extend([ASCII_SYMBOLS.index(char) * 25 for char in line])
    
    # Calculate the average brightness of the ASCII art
    ascii_brightness_avg = np.mean(ascii_brightness)
    
    # Return the brightness difference
    return abs(original_brightness - ascii_brightness_avg)

# Convert the input img to ASCII art
def generate_ascii_art(img):
    # Convert to grayscale images
    gray_img = convert_to_grayscale(img)
    # Enhance image details
    detailed_img = improve_image_details(gray_img)  
    # Maps pixels to ASCII characters
    ascii_result = pixels_to_ascii(detailed_img, max_width=100)
    return ascii_result

# Save the generated ASCII art as a text file
def save_ascii_file(ascii_content):
    with open("ascii_art_output.txt", "w") as file:
        file.write(ascii_content)
    return "ascii_art_output.txt"

# Provides the ability to download ASCII art and evaluates brightness difference
def generate_ascii_and_evaluate(img):
    ascii_art_content = generate_ascii_art(img)
    brightness_diff = calculate_brightness_difference(convert_to_grayscale(img), ascii_art_content)
    download_link = save_ascii_file(ascii_art_content)
    return ascii_art_content, f"Brightness Difference: {brightness_diff:.2f}", download_link

# Define CSS styles to ensure ASCII art output areas have equal width fonts and are properly aligned
css_custom = """
.ascii-container {
    white-space: pre;
    font-family: monospace;
    font-size: 10px;
    overflow-y: auto;
    height: auto;
    width: 800px;
}
"""

# Create Gradio interface and apply custom CSS styles
ascii_interface = gr.Interface(
    # Generate ASCII art and evaluate brightness difference, also provide download
    fn=generate_ascii_and_evaluate,
    # Image input in 'PIL' format
    inputs=gr.Image(type="pil"),
    # ASCII art display, brightness evaluation, and downloadable file
    outputs=[gr.HTML(label="ASCII Art Display", elem_classes="ascii-container"), "text", "file"],
    # File title and description
    title="ASCII Art Converter with Brightness Evaluation",
    description="Upload an image to convert it into ASCII art and evaluate the brightness difference.",
    css=css_custom
)

# Launch the Gradio app
ascii_interface.launch(share=True)
