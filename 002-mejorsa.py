import cv2
import numpy as np
import os
from datetime import timedelta

# Define the font, colors, and other parameters
font = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_HERSHEY_DUPLEX  # Bold font
font_thickness = 10  # Bold thickness
font_color = (220, 220, 220)  # RGB for text
bg_color = (50, 50, 50)  # RGB for background
frame_size = (3840, 2160)  # 4K resolution
fps = 1  # 1 frame per second

# Durations in seconds for each video
durations = [10, 20, 30, 60, 120, 180, 240, 300, 600, 1200, 1800, 2400, 3000, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200]

# Output directory
output_dir = "render"
os.makedirs(output_dir, exist_ok=True)

def calculate_max_font_scale(text, frame_size, font, font_thickness):
    """ Calculate the maximum font scale that fits within the frame. """
    scale = 1
    while True:
        text_size = cv2.getTextSize(text, font, scale, font_thickness)[0]
        if text_size[0] >= frame_size[0] or text_size[1] >= frame_size[1]:
            return scale - 1
        scale += 1

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

    # Determine the maximum font scale that will fit
    max_scale = calculate_max_font_scale("00:00:00", frame_size, font, font_thickness)

    # Loop through each second in the duration
    for t in range(duration, -1, -1):
        # Create a black background image
        img = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)
        img[:] = bg_color

        # Convert seconds to HH:MM:SS format
        time_remaining = str(timedelta(seconds=t))

        # Calculate text size and position
        text_size = cv2.getTextSize(time_remaining, font, max_scale, font_thickness)[0]
        text_x = (frame_size[0] - text_size[0]) // 2
        text_y = (frame_size[1] + text_size[1]) // 2

        # Put the text on the image
        cv2.putText(img, time_remaining, (text_x, text_y), font, max_scale, font_color, font_thickness)

        # Write the frame to the video
        out.write(img)

        # Save the final frame as an image if it's 00:00:00
        if t == 0:
            final_frame_path = os.path.join(output_dir, "timer_00_00_00.png")
            cv2.imwrite(final_frame_path, img)
            print(f"Final frame saved as {final_frame_path}")

    # Release the VideoWriter object
    out.release()
    print(f"{output_filename} has been created.")

# Loop through each duration and create the corresponding video
for duration in durations:
    create_timer_video(duration)
