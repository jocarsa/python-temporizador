import cv2
import numpy as np
import os
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont

# Define the font, colors, and other parameters
font_path = "Ubuntu-Bold.ttf"  # Path to your TTF font file
font_size = 200  # Initial font size, will be adjusted later
font_color = (220, 220, 220)  # RGB for text
bg_color = (50, 50, 50)  # RGB for background
frame_size = (3840, 2160)  # 4K resolution
fps = 1  # 1 frame per second

# Durations in seconds for each video
durations = [10, 20, 30, 60, 120, 180, 240, 300, 600, 1200, 1800, 2400, 3000, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200]

# Output directory
output_dir = "render"
os.makedirs(output_dir, exist_ok=True)

def calculate_max_font_size(text, frame_size, font_path):
    """ Calculate the maximum font size that fits within the frame. """
    img = Image.new("RGB", frame_size, bg_color)
    draw = ImageDraw.Draw(img)
    font_size = 10  # Start with a small font size

    while True:
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        if text_width >= frame_size[0] or text_height >= frame_size[1]:
            return font_size - 1
        font_size += 1

def create_timer_video(duration):
    # Calculate the output filename
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_label = f"{int(hours):02d}_{int(minutes):02d}_{int(seconds):02d}"
    output_filename = f"timer_{time_label}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    # Skip the file if it already exists
    if os.path.exists(output_path):
        print(f"{output_filename} already exists, skipping...")
        return

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    # Determine the maximum font size that will fit
    max_font_size = calculate_max_font_size("00:00:00", frame_size, font_path)
    font = ImageFont.truetype(font_path, max_font_size)

    # Loop through each second in the duration
    for t in range(duration, -1, -1):  # Adjusted to include 00:00:00
        # Create a black background image using PIL
        img_pil = Image.new("RGB", frame_size, bg_color)
        draw = ImageDraw.Draw(img_pil)

        # Convert seconds to HH:MM:SS format
        time_remaining = str(timedelta(seconds=t))

        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), time_remaining, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (frame_size[0] - text_width) // 2
        text_y = (frame_size[1] - text_height) // 2

        # Put the text on the image
        draw.text((text_x, text_y), time_remaining, font=font, fill=font_color)

        # Convert PIL image back to OpenCV format
        img = np.array(img_pil)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Write the frame to the video
        out.write(img)

    # Add 5 additional frames of 00:00:00 to last for 5 seconds
    for _ in range(5):
        out.write(img)  # The img from the last loop is 00:00:00

    # Release the VideoWriter object
    out.release()
    print(f"{output_filename} has been created.")

# Loop through each duration and create the corresponding video
for duration in durations:
    create_timer_video(duration)
