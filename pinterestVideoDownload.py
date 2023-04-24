import requests

def pinterestVideoDownloader(url):
    url = "https://tr.pinterest.com{}".format(url)
    apiUrl = 'https://pinterest-backend.onrender.com/video/'
    response = requests.get(apiUrl+url)
    videoDownloadLink = response.json()['url']
    pinId = url.split('/')[-2]
    with open('Pinterest/Videos/{}.mp4'.format(pinId), 'wb') as f:
        f.write(requests.get(videoDownloadLink).content)
        print("Video downloaded as {}.mp4!".format(pinId))
    return pinId
