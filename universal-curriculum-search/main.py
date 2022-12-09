import moviepy.editor as mp
import os

chunk_increment = 2

# Load the video
video = mp.VideoFileClip("street.mp4")

# Iterate over the video in 30-second increments
for i in range(0, round(video.duration)):
    # Get the timestamp range for the current chunk
    start_time = i
    end_time = min(i + chunk_increment, video.duration)

    # Create a new clip for the current chunk and add it to the list
    chunk = video.subclip(start_time, end_time)
    file_path = f"chunks/{start_time}-{end_time}.mp4"
    # save
    chunk.write_videofile(file_path)
    # convert to audio
    video = mp.VideoFileClip("street.mp4")
    chunk.write_audiofile(f"chunks/{start_time}-{end_time}.mp3")
