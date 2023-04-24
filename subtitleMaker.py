from datetime import timedelta
import whisper

def transcribeAudio(path,model="medium"):
    model = whisper.load_model(model) # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path,fp16=False)
    segments = transcribe['segments']
    srtFilename = "deneme.srt"
    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    input("Are you sure about this transcription? If you are not please change the whisper model bigger and try again. Press enter to continue...")
    return srtFilename
