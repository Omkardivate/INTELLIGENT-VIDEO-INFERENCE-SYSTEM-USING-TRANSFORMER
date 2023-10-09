import cv2
import os
from transformers import pipeline

import tkinter as tk
from tkinter import filedialog

import json

def videopath(path):
    video_path = path
    output_dir = "C:\\Video_Inference_System\\temp"
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Define the interval for extracting frames (in seconds)
    interval = 1

    # Initialize variables for the frame count and the timestamp of the last extracted frame
    frame_count = 0
    last_extracted = 0

    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Get the timestamp of the current frame
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        # If the interval has elapsed since the last extracted frame, save this frame as an image file
        if timestamp - last_extracted >= interval:
            # Define the output file path for this frame
            output_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")

            # Save the frame as an image file
            cv2.imwrite(output_path, frame)

            # Increment the frame count and update the timestamp of the last extracted frame
            frame_count += 1
            last_extracted = timestamp

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

    path = "C:\\Video_Inference_System\\temp\\"
    for file in os.listdir(path):
        caption_dict = image_to_text(path + file)
        caption_str = json.dumps(caption_dict, indent=4)
        output_label.config(text=output_label.cget("text") + "\n" + caption_str)
        output_label.pack(pady=10)
        os.remove(path + file)


def browse_file():
    file_path = filedialog.askopenfilename()
    videopath(file_path)

#creating tkinter window
root = tk.Tk()
root.title("Video to Text Converter")

#creating label
label = tk.Label(root, text="Click the button to browse for a video file:")
label.pack(pady=20)

#creating button to browse file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

#creating label to display output
output_label = tk.Label(root, text="")
output_label.pack(pady=10)

#run tkinter main loop
root.mainloop()
