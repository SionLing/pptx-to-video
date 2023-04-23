import decode_ppt
from gtts import gTTS
from playsound import playsound
from moviepy.editor import *
from pydub import AudioSegment
import process_text
import make_srt

CONFIG = {
    'fps': 24,
    'duration': 2,
    'audio_dir': 'audios',
    'video_dir': 'videos',
    'image_dir': 'images',
    'output_file': 'final.mp4',
    'default_lang': 'en'
}

# Create silent audio file
def make_silent_audio(out_file, duration = 2):
    silence = AudioSegment.silent(duration=duration*1000, frame_rate=44100)
    silence.export(out_file, format="mp3")
    return out_file

# make audio from text using gTTS
def make_audio(index,text):
    print(text)
    out_file = f"{CONFIG['audio_dir']}/{index}.mp3"
    if text == '':
        return make_silent_audio(out_file)
    else:
        tts = gTTS(text)
        tts.save(out_file)
    # playsound(out_file)
    return out_file

# make video from a single image and audio
def make_video(index, image, audio):
    out_file = f"{CONFIG['video_dir']}/{index}.mp4"
    audioclip = AudioFileClip(audio)
    clip = ImageClip(image).set_duration(audioclip.duration)
    videoclip = clip.set_audio(audioclip)
    videoclip.write_videofile(out_file, fps=CONFIG['fps'])
    return out_file, audioclip.duration

# Jion all videos into one using moviepy
def join_videos(videos, output_file):
    clips = [VideoFileClip(v) for v in videos]
    final_clip = concatenate_videoclips(clips)
    # final_clip.write_videofile(output_file, fps=CONFIG['fps'])
    final_clip.write_videofile(output_file, fps=CONFIG['fps'], audio_codec='aac')
    pass

# Split text into sentences
def split_text(notes):
    new_notes = []
    for note in notes:
        sentences = process_text.text_to_sentences(note['text'])
        if len(sentences) == 0:
            new_notes.append({'text':'', 'image':note['image']})
        else:
            for i,sentence in enumerate(sentences):
                new_notes.append({'text':sentence, 'image':note['image']})
    return new_notes

# make audio and video for each slide
def make_all(pptx_file, output_file=CONFIG['output_file']):
    notes = decode_ppt.export_pptx(pptx_file, CONFIG['image_dir'])
    # Split text into sentences
    notes = split_text(notes)
    videos = []
    for i,note in enumerate(notes):
        audio_file = make_audio(i, note['text'])
        note["audio"] = audio_file
        video_file,duration = make_video(i, note['image'], note["audio"])
        note['duration'] = duration
        videos.append(video_file)
    # join clips into one video
    join_videos(videos, output_file)
    # make srt file
    srt_filename =os.path.splitext(output_file)[0] + '.srt'
    make_srt.make_srt(notes, srt_filename)
    pass

# Clean up all files
def clean_up():
    import os
    import shutil
    shutil.rmtree(CONFIG['audio_dir'], ignore_errors=True)
    shutil.rmtree(CONFIG['video_dir'], ignore_errors=True)
    shutil.rmtree(CONFIG['image_dir'], ignore_errors=True)
    if os.path.exists(CONFIG['output_file']):
        os.remove(CONFIG['output_file'])
    pass

# Create directorys
def create_dir():
    import os
    os.makedirs(CONFIG['audio_dir'], exist_ok=True)
    os.makedirs(CONFIG['video_dir'], exist_ok=True)
    os.makedirs(CONFIG['image_dir'], exist_ok=True)
    pass

# Create video from pptx file
def pptx_to_video(pptx_file, output_file):
    clean_up()
    create_dir()
    make_all(pptx_file, output_file)

# Test code
if __name__ == '__main__':
    pptx_file = 'test.pptx'
    output_file = 'final.mp4'
    pptx_to_video(pptx_file, output_file)
