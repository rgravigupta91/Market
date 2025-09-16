from pytube import YouTube
import moviepy
#print(moviepy.__file__)
#from moviepy.editor import VideoFileClip
import os

def download_youtube_audio(url, output_folder='./downloads'):
    # Create folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Step 1: Download YouTube video
    yt = YouTube(url)
    print(f"Downloading video: {yt.title}")
    #video_stream = yt.streams.filter(only_video=False, file_extension='mp4').first()
    #downloaded_video_path = video_stream.download(output_path=output_folder)

    # Step 2: Convert video to audio
    #print("Converting to audio...")
    #video_clip = moviepy.videotools.VideoFileClip(downloaded_video_path)
    #audio_path = os.path.splitext(downloaded_video_path)[0] + ".mp3"
    #video_clip.audio.write_audiofile(audio_path)
    #video_clip.close()

    #print(f"Audio saved to: {audio_path}")
    #return audio_path

url = "www.youtube.com/watch?v=mr8GBzTsWqM"
download_youtube_audio(url=url)