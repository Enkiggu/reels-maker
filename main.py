from pinterestModules import pinterestPin,pinterestVideo
from subtitleAdder import addSubtitle
import argparse

parser = argparse.ArgumentParser(description="Pinterestten reels oluşturma scripti")
parser.add_argument("-q","--query", help="Aranacak öğe")
parser.add_argument("-ml","--model", help="Dil öğrenme modeli (small,medium,large). Default: medium",default="medium")
parser.add_argument("-fv","--fromVideo", help="Videodan reels oluşturur.",action="store_true",default=False)
parser.add_argument("-fi","--fromImage", help="Resimden reels oluşturur.",action="store_true",default=False)
parser.add_argument("-sc","--scroll", help="Kaç kere kaydırma yapacağını gösterir")
parser.add_argument("-st","--scrollTime", help="Kaydırma yaparken bekleme süresi")
parser.add_argument("-m","--music", help="Müzik dosyasının ismi (Uzantıyı belirtin)")
parser.add_argument("-bi","--bulkImage", help="Bulduğu tüm resimleri indirir. Default: False" ,action="store_true",default=False)
parser.add_argument("-r","--reels", help="Reels yapmayı sağlar. Default: True",action="store_true",default=True)
parser.add_argument("-vt","--videoTime", help="Aranacak videonun süresi. (Saniye cinsinden)")
args = parser.parse_args()

if args.fromVideo == True:
    print("Creating reels using video...")
    videoName = pinterestVideo(args.query,int(args.scroll),int(args.scrollTime),int(args.videoTime))
    addSubtitle( videoName + ".mp4",args.music,args.model)
    print("Video is ready!")
elif args.fromImage == True:
    print("Creating reels using image...")
    pinterestPin(args.query,int(args.scroll),int(args.scrollTime),args.music,args.model,args.bulkImage,args.reels)
else:
    print("You can get help by using the command 'python main.py -h'.\nExample usage for creating reels from images: 'python main.py -fi -q \"aesthetic sky\" -sc 2 -st 3 -m \"music.mp3\"'\n"
          "Example usage for creating reels from videos: 'python main.py -fv -q \"aestetic sky\" -sc 2 -st 3 -m \"music.mp3\" -vt 10'")