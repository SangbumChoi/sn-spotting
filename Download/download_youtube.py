import os

import cv2
from pytube import YouTube


def download_video(url, output_path, output_name):
    try:
        # Create a YouTube object using the provided URL
        yt = YouTube(url)
        download_path = os.path.join(output_path, output_name)

        # Download the video with the highest resolution (720p in this case) to the specified output path
        yt.streams.filter(file_extension="mp4", res="720p").first().download(
            output_path
        )
        print("Video downloaded successfully")
        return download_path
    except Exception as e:
        print(f"Error during video download: {e}")


def split_video_to_images(video_path, output_folder):
    try:
        # Open the video file using OpenCV
        cap = cv2.VideoCapture(video_path)

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Read the first frame of the video
        success, image = cap.read()

        # Initialize a frame count variable
        count = 0

        # Loop through all frames in the video
        while success:
            # Save the current frame as an image in the specified output folder
            image_path = os.path.join(output_folder, f"frame_{count}.png")
            cv2.imwrite(image_path, image)

            # Read the next frame
            success, image = cap.read()

            # Increment the frame count
            count += 1

        # Release the video capture object
        cap.release()

        # Print a message indicating the successful conversion to images and the number of frames generated
        print(f"Video converted to images successfully. {count} frames created.")
    except Exception as e:
        print(f"Error during video to image conversion: {e}")


if __name__ == "__main__":
    # Specify the YouTube video URL and the output folder
    video_url = "https://www.youtube.com/watch?v=4w4mUxh6jzA"
    output_folder = "Download/data/test/"
    video_name = "Football Wide Angle Footage.mp4"

    # Download the video from YouTube
    download_path = download_video(video_url, output_folder, video_name)

    # Split the video into images
    # split_video_to_images(download_path, output_folder)
