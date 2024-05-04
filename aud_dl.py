import os
import yt_dlp
os.chdir(os.path.dirname(os.path.abspath(__file__)))

notAllowList = ["/","\\","*","?","<",">","\"","|",":","-",""]

def urlproc(url,pl):
    string = str(url)
    #TODO https://youtu.be/MFa0wY6zfD8 like this
    if 'list=' in string:
        listlocate = string.find("list=")
        listid = string[listlocate:listlocate+39] 
    else:
        listid = "None"



    if "watch?v=" in string:
        titlocate = string.find("watch?v=")
        id = string[titlocate:titlocate+19]
    elif "youtu.be" in string:
        locate = string.find("be/")
        id = string[locate+3:locate+14]
        listid = "None"
    else:
        id = "None"
        
    if "None" in listid and "watch" not in id:
        vidurl = "https://www.youtube.com/watch?v=" + f"{id}"
        listurl = "None"
    if "None" in listid and "watch" in id:
        vidurl = "https://www.youtube.com/" + f"{id}"
        listurl = "None"
    if "list" in listid and "None" in id:
        vidurl = "None"
        listurl = "https://www.youtube.com/playlist?" + f"{listid}"
    if "list" in listid and "watch" in id:
        vidurl = "https://www.youtube.com/" + f"{id}"
        listurl = "https://www.youtube.com/playlist?" + f"{listid}"
        
    

    if pl == True:
        return listurl,vidurl
        
    if pl == False:
        return vidurl


def downloader(url):
    url = urlproc(url,False)
    filename = get_title(url) + ".m4a"
    filename = str(filename)
    for i in notAllowList:
        filename = filename.replace(f'{i}',"")
        
    print(filename)
    
    os.system(f"yt-dlp.exe -f m4a/bestaudio/best -x -o \"{filename}\" --console-title --audio-format m4a --ffmpeg-location ffmpeg.exe --postprocessor-args FixupM4a: {url}")
    return filename


def embedDownloader(url):
    ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

def get_title(url):
    with yt_dlp.YoutubeDL() as ydlp:
        info = ydlp.extract_info(url,download=False)
    return info.get('title')

def tomp3(filename):
    
    ftype = str(filename).split('.')[-1]
    fname = str(filename).replace('.m4a',"")
    
    cmd = f'ffmpeg -i {filename} -vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000 {fname}.mp3' # 回去抓abr速度會掉 所以直接預設用160k encode mp3
    try:
        os.system(cmd)
        os.remove(f'{filename}')
    except:
        return(None)
    return f"{fname}.mp3"

def main():
    while True:
        url = input("請輸入連結:")
        print(downloader(urlproc(url,False)))
        url = ""


if __name__ == '__main__':
    main()
