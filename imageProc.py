from rembg.bg import remove,new_session
import cv2
import PIL
import os
import requests
import asyncio
os.chdir(os.path.dirname(os.path.abspath(__file__)))

allowed_attach = ["png","jpg","jpeg","jfif","webp"]
def toWhitebg(url):
    filename = url.split('/')[-1]
    filename = filename.split('?')[0]
    filename,sub = filename.split('.')[0],filename.split('.')[1]
    if sub not in allowed_attach:
        return "File type not allowed."
    if sub == 'webp':
        sub = 'png'
    img = requests.get(url,allow_redirects=True)

    with open(f"{filename}.{sub}",'wb') as handler:
        handler.write(img.content)

    
    output_path = f"{filename}_rembg.png"
    session = new_session('isnet-anime')
    pic = cv2.imread(f"{filename}.{sub}")
    output = remove(pic,session=session)
    cv2.imwrite(output_path,output)

    os.remove(f'{filename}.{sub}')
    return f"{filename}_rembg.png"
    

