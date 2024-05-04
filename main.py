#coding=UTF-8

import datetime
import discord
import os
import random
import time
import queue

from dotenv import load_dotenv

import gr
import imageProc
import aud_dl

os.chdir(os.path.dirname(os.path.abspath(__file__)))
arena_gm_list = [281435226012647434,645177694543282186,321298677547139072,449370483880755210,185811604439433216,561727016689467403,473304405697888267,417011631873064960,456830632404844554,576386278858162186,462978744030593045,368728169680732170,462978744030593045,505762064602497034,191131198184095744,251721315185197056]
arena_channel_list = [1092254995052777604,1085647579615862925,808301142776872983,1170716932262076416]
arena_emoji_list = ["<:Excuseme:1092137211832573952>","<:FBK:1092296776385572925>","<:koishiShock:1092297314594472076>","<:hahaha:1092297884935925800>","<:WTFcat:1092137424706085025>","<:Socute:1092137269617492100>"]
room_list = {
    645177694543282186 : "https://ccfolia.com/rooms/-GRlewmU_",
    505762064602497034 : "https://ccfolia.com/rooms/o8NGZkdd_",
    462978744030593045 : "https://ccfolia.com/rooms/9-r454gRk",
    576386278858162186 : "https://ccfolia.com/rooms/pwv77nPu8",
    456830632404844554 : "https://ccfolia.com/rooms/UsIc3XOCT",
    417011631873064960 : "https://ccfolia.com/rooms/LyIj8OQd1",
    473304405697888267 : "https://ccfolia.com/rooms/16LcVjZr-",
    185811604439433216 : "https://ccfolia.com/rooms/y0WXRABLV",
    561727016689467403 : "https://ccfolia.com/rooms/wLFsR1QEB",
    281435226012647434 : ["https://ccfolia.com/rooms/ywoGpS2e-","https://ccfolia.com/rooms/_HVF5kBLQ"],
    321298677547139072 : ["https://ccfolia.com/rooms/0sY-QLcmK","https://ccfolia.com/rooms/hsuelNy6b"],
    449370483880755210 : ["https://ccfolia.com/rooms/kGwc5FoDJ","https://ccfolia.com/rooms/nG2HrGtVK","https://ccfolia.com/rooms/j4pVV4hVL","https://ccfolia.com/rooms/_RaqOSck5"],
    191131198184095744 : "https://ccfolia.com/rooms/iUdefQiQW",
    251721315185197056 : "https://ccfolia.com/rooms/0YLk5t2Qb"
}
rawGrResultQueue = queue.Queue(0)
grPrefer = []

client = discord.Client(intents=discord.Intents.all())
def initialize():
    global join_list,name_list,target,ctx,Gm,endMessage,rawGrResultQueue,grPrefer
    join_list = {"1-3":"","3-5":"","5-7":"","7-9":"","9-11":"","11-15":""}
    name_list = ["1-3","3-5","5-7","7-9","9-11","11-15"]
    target= 0
    ctx = ""
    endMessage = ""
    Gm = ""
    rawGrResultQueue = queue.Queue(0)
    grPrefer = []
    


initialize()



@client.event
# 當機器人完成啟動時在終端機顯示提示訊息
async def on_ready():
    print(f'目前登入身份：{client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    if message.content.startswith(".1d"):
        await message.channel.send(f"1D6 = {gr.oned()}")
    if message.content.startswith(".gr"):
        pf = []
        contents = message.content.lower().split(" ")
        contents.pop(0)
        print(contents[0])
        print(contents[0] not in ["a","b","c"])
        if contents[0] not in ["a","b","c"]:
            print("Format:Normal")
            for i in contents:
                pf.append(int(i))
        
        
            grCount = pf[0]
            pf.pop(0)
        
            if len(pf) != 6:
                await message.channel.send("格式錯誤。")
                return
            for i in range(grCount):
                rawGrResultQueue.put(gr.normal())
            print(pf)
            await message.channel.send(gr.main(pf,rawGrResultQueue))
        else:
            print("Foramat:SP")
            for i in contents:
                pf.append(i)
            sp = pf[0]
            pf.pop(0)
            grCount = int(pf[0])
            pf.pop(0)
            if len(pf) != 6:
                await message.channel.send("格式錯誤。")
                return
            for i in range(grCount):
                rawGrResultQueue.put(gr.normal())
            intPf = []
            for j in pf:
                intPf.append(int(j))
            print(sp,intPf,rawGrResultQueue.empty())
            await message.channel.send(gr.prH(sp,intPf,rawGrResultQueue))
            

        
    if message.content.startswith("好的鬥技場"):
        print(f"{message.author.name}:目標字串-開團")
        if message.channel.id in arena_channel_list:
            print(f"{message.author.name}:目標頻道")
            if message.author.id in arena_gm_list:
                print(f"{message.author.name}:目標人員")
                
                global ctx
                ctx = ""
                global join_list
                join_list = {"1-3":"","3-5":"","5-7":"","7-9":"","9-11":"","11-15":""}
                ctx = await message.channel.send(f"===={datetime.datetime.now().astimezone().isoformat()}====\n{deadManTimeDetect(time.localtime().tm_hour)}\n\
**{message.author.name}**開競技場了唷。\n<@&1093203033724301393>\n==========\n報名人員:")
                #
                
                global target
                
                target = message.id

                global Gm
                Gm = message.author.id
                
                
                print(target)
    
    if message.content.startswith(".stop"):
        if target == 0:
            return
        contents = message.content.lower().split(" ")
        if len(contents) == 1:
            level = ""
        else:
            try:
                level = int(contents[1])
            except:
                level = ""
                pass
            print(contents[1])
        print(f"{message.author.name}:目標字串-拉線")
        if message.channel.id in arena_channel_list:
            print(f"{message.author.name}:目標頻道-拉線")
            if message.author.id == Gm:
                global endMessage
                
                print(f"{message.author.name}:目標成員-拉線")


                endMessage = await message.channel.send(f"========拉線========\n報名人員:{level_detect(join_list)}\n==========房間(測試中)=========\n<{returnRoom(Gm,level)}>")

                initialize()

    if message.content.startswith(".rembg"):
        if message.attachments:
            
            
            filename = imageProc.toWhitebg(message.attachments[0].url)
            img = discord.File(f'{filename}')
            await message.channel.send(file = img, reference = message)
            os.remove(filename)
    
            
        else:
            await message.channel.send(f"====這則訊息不包含圖片====")
    
    if message.content.startswith(".dl"):
        contents = message.content.split(" ")
        if len(contents) == 1:
            return
        
        url = contents[1]
        if 'youtu' not in url:
            print("Not suiteble url")
            await message.channel.send("====不支援的網址====")
            return
        filename = aud_dl.downloader(url)
        try:
            if 'mp3' in contents[0]:
                rndname = f"{random.random()}".replace('.','')
                os.rename(filename, f'fx{rndname}xf.m4a')
                aud_dl.tomp3(f"fx{rndname}xf.m4a")
                filename = filename.replace(".m4a","")
                os.rename(f"fx{rndname}xf.mp3",f"{filename}.mp3")
                filename = f'{filename}.mp3'


        except:
            print('No mp3 dec')
            pass
        aud = discord.File(f'{filename}')
        await message.channel.send(file = aud, reference = message)
        os.remove(filename)




            


@client.event
async def on_reaction_add(reaction,user):
    if reaction.message.id == target:
        pass
    else:
        return

    
    if str(reaction) not in arena_emoji_list:
        print("nah")
        return
    else:
        
        for i in arena_emoji_list:
            print(arena_emoji_list.index(i))
            print(str(reaction)==i)
            if str(reaction) == i:
                print("wry")
                if f"{user.name}" not in join_list[name_list[arena_emoji_list.index(i)]]:
                    
                    join_list[name_list[arena_emoji_list.index(i)]] += f"\n{user.name}"
        
        messageRN=ctx.content
        messageRN = messageRN + level_detect(join_list)
        
        await ctx.edit(content=messageRN)

@client.event
async def on_reaction_remove(reaction,user):
    if reaction.message.id == target:
        pass
    else:
        return
    
    if str(reaction) not in arena_emoji_list:
        print("still nah")
        return
    else:

        for i in arena_emoji_list:
            print(arena_emoji_list.index(i))
            print(str(reaction)==i)
            if str(reaction) == i:
                print("E?")
                if f"{user.name}" in join_list[name_list[arena_emoji_list.index(i)]]:
                    join_list[name_list[arena_emoji_list.index(i)]] = join_list[name_list[arena_emoji_list.index(i)]].replace(f"\n{user.name}","")
                    print(join_list)
        global messageRN
        messageRN = ctx.content
        messageRN = messageRN + level_detect(join_list)

        await ctx.edit(content=messageRN)
                    




def level_detect(joindict):
    readyToReturn=''
    
    joindict = dict(joindict)
    for key,values in joindict.items():
        
        if values!="":
            readyToReturn = readyToReturn + f"\n{key}:{values}"
            
            #phrase[int(joinlist.index(i))] = name_list[int(joinlist.index(i))]
            #phrase[int(joinlist.index(i))] += i
    
    print(readyToReturn)
    readyToReturn = "```" + readyToReturn + "```"
    return readyToReturn

def returnRoom(GM,level):
    room = room_list.get(GM,"找不到房間")
    if type(room) == list:
        try:
            if level == "":
                rt = "請至列表查詢"
            else:
                rt = room[level-1]
        except:
            rt = "請至列表查詢"
        return rt
    else:
        return room
        
    







    

def deadManTimeDetect(hour):
    if hour >= 2 and hour <=6:
        return f"現在時間是{time.localtime().tm_hour}點{time.localtime().tm_min}分了呢，常常這個時間還不睡會死的唷。"
    else:
        return f"現在時間是{time.localtime().tm_hour}點{time.localtime().tm_min}分了呢。"    
    
        
load_dotenv()
token = os.environ.get('DCBOT_TOKEN')
client.run(token)
