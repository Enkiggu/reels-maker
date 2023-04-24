import os
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import VideoFileClip,TextClip,CompositeVideoClip
from moviepy import editor
from subtitleMaker import transcribeAudio

def addSubtitle(videoName,musicName,model):
    #Remove the music background
    video = editor.VideoFileClip(f"Pinterest/Videos/{videoName}")
    video_without_audio = video.set_audio(None)
    video_without_audio.write_videofile("Pinterest/Videos/nonesound.mp4")

    #Add the music background
    video = editor.VideoFileClip("Pinterest/Videos/Nonesound.mp4")
    audio = editor.AudioFileClip(f"{musicName}")
    duration = audio.duration
    final = video.set_audio(audio)
    final.write_videofile(f"Pinterest/Videos/{videoName}")

    videoDuration = video.duration
    if videoDuration > duration:
        video = video.subclip(0, duration)

    srtFileName = transcribeAudio(f"{musicName}",model)
    video = VideoFileClip(f"Pinterest/Videos/{videoName}")
    generator = lambda txt: TextClip(txt, font='Roboto-Bold', fontsize=28, color='white')
    subs = SubtitlesClip(srtFileName,generator)
    subtitle = SubtitlesClip(subs,generator).set_position('center', relative=True)
    result = CompositeVideoClip([video, subtitle])

    result.write_videofile(f"{videoName}",fps=60)
    os.remove(srtFileName)
    os.remove("Pinterest/Videos/nonesound.mp4")

