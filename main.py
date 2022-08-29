from gtts import gTTS
from moviepy.editor import *
from pytube import YouTube
import random
# import os



def generate_audio(text):
    # Generate an audio file from Google's text-to-speech library
    print('Generating audio file')
    tts = gTTS(text)
    tts.save('audio.mp3')

def download_youtube(url):
    # Download a YouTube video to a file.
    # Choose the best quality available.
    print("Downloading video from YouTube")
    yt = YouTube(url)
    out_file = yt.streams.filter(file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first() \
        .download()
    os.rename(out_file, 'youtube.mp4')

def generate_video(text, filename):
    print("Editing Video")
    # AUDIO
    # Open audio file
    audio_file_clip = AudioFileClip("audio.mp3")
    
    # Get Text-To-Speech total audio duration
    tts_duration = audio_file_clip.duration

    # Create a MoviePy-Audio-Clip
    audio_clip = CompositeAudioClip([audio_file_clip])

    # Reduce the audio volume (Optional)
    # audio_clip = videoclip.volumex(0.8)

    # VIDEO
    # Open the video file from YouTube
    videoclip = VideoFileClip("youtube.mp4")
    youtube_duration = videoclip.duration

    # Pick a random part in the YouTube video. Make it the same tts_duration of the text-to-speech audio.
    part = random.randint(0, int(youtube_duration)-int(tts_duration))

    # Cut the video at the random part
    videoclip = videoclip.subclip(0 + part, tts_duration + part)
    
    # Get Video size
    width, height = videoclip.size

    # Crop the video so if would fit in landscape mode.
    videoclip = videoclip.crop(x_center=width/2, width=height)

    # Video from YouTube could be at any resolution.
    # This shrinks, streches or does nothing if the video is already 1080x1920.
    videoclip = videoclip.resize((1080, 1920))
    
    # AUDIO VIDEO mix
    # Change the audio of the YouTube video to the text-to-speech audio.
    videoclip.audio = audio_clip

    # TEXT LABELS (overlays)
    # Here we'll store each sentence/label as seperate MoviePy-Clips.
    overlays = []

    # Keep track of when each sentance/label will begin. (Audioclip start time)
    text_start_time = 0  # [Seconds]

    # Seperate the full-text to a list of sentences. (After each newline)
    sentences = text.splitlines()

    # Number of sentences
    n = len(sentences)

    # Foreach sentence
    for sentence in sentences:
        # Create a MoviePy-Text-Clip with the one sentence
        txt = (TextClip(sentence.strip(), fontsize=50, size=(1080, 1920), font='Amiri-regular',
                color='white', method='caption'))

        # Edit the MoviePy-Text-Clip by adding a semi-transparent white background to the text.
        txt_col = txt.on_color(size=(videoclip.w, 150),
                            color=(0, 0, 0), pos=(6,"center"), col_opacity=0.8).set_duration(tts_duration/n).set_start(text_start_time)

        # Store the MoviePy-Text-Clip in the list.
        overlays.append(txt_col)

        # Update the Audioclip start time for the next sentence.
        # Timed in equal lenths. Unlike the audio. FIXME: (May not sit perfect w/ the audio)
        text_start_time += tts_duration/len(sentences)

    # Concatenate all seperate MoviePy-Text-Clips to one.
    # Set the location of the labels on the video (horizontally, vertically) from the top-left.
    final_textclip = concatenate_videoclips(overlays).set_position(('center', 300))


    # Generate the video, mixing the YouTube video with the overlay texts and Text-To-Speech audio.
    print("Stiching Video")
    result = CompositeVideoClip([videoclip,final_textclip])

    # Bob's your uncle
    print("Rendering Video")
    result.write_videofile(filename, fps=24)




def main():

    text1 = """Don't you just love listening to loud music?
Careful you don't get Hyperacusis
People you know can't listen to music anymore
Find out why in the details
"""

    text2 = """Did you know that 1 in 7 people is sick with Tinnitus?
Most of them don't tell anyone
Click here to find out why"""
   
    texts = []
    texts.append(text1)
    texts.append(text2)


    # Create 'Videos' folder
    print(os.getcwd())
    if not os.path.isdir('videos'):
        os.makedirs('videos')



    for i, text in enumerate(texts):
        print()
        print('****************************************')
        print(f"starting video {i+1} out of {len(texts)}")
        print('****************************************')
        print(text)
        print('****************************************')

        generate_audio(text)
        download_youtube(url = 'https://youtu.be/2lAe1cqCOXo')
        generate_video(text=text, filename=os.path.join('videos',f"T{i+1}.mp4"))
        
        print('****************************************')




if __name__=='__main__':
    main()