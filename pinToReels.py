from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import VideoFileClip,TextClip,CompositeVideoClip
from moviepy import editor
from subtitleMaker import transcribeAudio


def pinToReels(photoList,musicName,model):
    audio = AudioFileClip(f"{musicName}")
    videoDuration = audio.duration
    photoPaths = photoList

    numPhotos = len(photoPaths)
    photoDuration = videoDuration / numPhotos

    photoClips = []
    for photoPath in photoPaths:
        photoClip = ImageClip(photoPath).set_duration(photoDuration)
        photoClips.append(photoClip)

    photos = concatenate_videoclips(photoClips)

    videoWidht = 1080
    videoHeight = 1920

    photos = photos.resize((videoWidht, videoHeight))

    srtFileName = transcribeAudio(f"{musicName}",model)
    generator = lambda txt: TextClip(txt, font='Roboto-Bold', fontsize=28, color='white')
    subs = SubtitlesClip(srtFileName, generator,encoding='utf-8')
    subtitle = subs.set_position('center', relative=True)

    result = CompositeVideoClip([photos, subtitle]).set_audio(audio)

    result.write_videofile("output.mp4", fps=60)
    print("Video downloaded as output.mp4!")
    os.remove(srtFileName)
