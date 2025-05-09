#coding=UTF-8
import asyncio
import datetime
import discord
import os
import random
import threading
import time
import queue

from dotenv import load_dotenv

import gr
import imageProc
import aud_dl
from bin import arena_gm_list,arena_channel_list,arena_emoji_list,room_list

os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()
token = os.environ.get('TOKEN')
client = discord.Client(intents=discord.Intents.all())
arena_board = []


class Arena:
    def __init__(self, father_message: discord.message.Message, workloop: asyncio.AbstractEventLoop):
        self._workloop = workloop
        self._stat = "START"
        self._dashboard_state = 'Not Created'
        self._future_dashboard = ''
        
        self._father_message = father_message
        self.gm = self._father_message.author

        self._member_list = {
            '1-3':'',
            '3-5':'',
            '5-7':'',
            '7-9':'',
            '9-11':'',
            '11-15':''
        }
        self._dashboard_message = None
        self.url = ""
    
    def create_dashboard(self):
        content = f"===={datetime.datetime.now().astimezone().isoformat()}====\n\
**{self.gm.name}**開競技場了唷。\n<@&1093203033724301393>\n==========\n報名人員:"
        self._future_dashboard = asyncio.run_coroutine_threadsafe(send_message(self._father_message,content),self._workloop)
        self._dashboard_state = 'Pending'
        
    def update_dashboard(self):
        if self._dashboard_state == 'Pending':
            self._dashboard_message = self._future_dashboard.result(timeout = 5)
        ori = self._dashboard_message.content
        edited = ori + self.member_msg()
        asyncio.run_coroutine_threadsafe(edit_message(self._dashboard_message,edited),self._workloop)

    def member_msg(self):
        rt = ""
        for key,value in self._member_list.items():
            if value != "":
                rt += f"{key}:{value}\n"
        rt = "```\n" + rt + "```"
        return rt
    
    def set_arena_url(self,lvl = -1):
        try:
            if type(room_list[self.gm.id]) == list:
                self.url = room_list[self.gm.id][lvl]
            else:
                self.url = room_list[self.gm.id]
        except:
            self.url = '請至列表查詢。'

    def create_end_message(self):
        content = f'========拉線========\n報名人員:{self.member_msg()}\n==========房間=========\n<{self.url}>'
        asyncio.run_coroutine_threadsafe(send_message(self._father_message,content),self._workloop)
    
    def __str__(self) -> str:
        return f'Starter:{self.gm.name}, Status:{self._stat}, msg_obj:{self._father_message}\n'
    def __repr__(self):
        return 'Starter:'f'{self.gm} as {self.gm.name}\n'+'Status:' f'{self._stat}'
    
   
        
async def send_message(message_obj: discord.message.Message, msg: str = '', file: discord.File = None):
    message = message_obj
    if file != None:
        rt_message_obj = await message.channel.send(f"{msg}", file = file, reference = message)
        print(file.filename)
        os.remove(file.filename)
    else:
        rt_message_obj = await message.channel.send(f"{msg}")
    print(rt_message_obj)
    return rt_message_obj

async def edit_message(message_obj: discord.message.Message, msg: str = ''):
    await message_obj.edit(content=msg)

async def delete_activity(filename: str):
    print(filename)
    await os.remove(filename)



@client.event
# 當機器人完成啟動時在終端機顯示提示訊息
async def on_ready():
    print(f'目前登入身份：{client.user}')

@client.event

async def on_message(message: discord.message.Message):
    currentWorkLoop = asyncio.get_event_loop()
    if message.author == client.user:
        return

    if message.content.startswith('.1d'):
        await message.channel.send(f'1D6 => {gr.oned()}')

    if message.content.startswith('.gr'):
        prefer =[]
        contents = message.content.lower().split(' ')
        contents.pop(0)
        if contents[0] not in ['a','b','c']:
            
            for i in contents:
                prefer.append(int(i))
            grCount = prefer.pop(0)
            if grCount > 1000000:
                await message.channel.send('最多僅支援1000000次。')
                return
        
            if len(prefer) != 6:
                await message.channel.send('格式錯誤。')
                return
            handler = threading.Thread(target=gr_action,args=(message,grCount,prefer,currentWorkLoop))
            handler.start()
        else:
            sp = contents.pop(0)
            for i in contents:
                prefer.append(int(i))
            grCount = int(prefer.pop(0))
            if grCount > 1000000:
                await message.channel.send('最多僅支援1000000次。')
                return
            if len(prefer) != 6:
                await message.channel.send('格式錯誤。')
                return
            handler = threading.Thread(target=gr_action,args=(message,grCount,prefer,currentWorkLoop,sp))
            handler.start()
    if message.content.startswith('好的鬥技場'):
        id_check = message.channel.id in arena_channel_list
        member_check = message.author.id in arena_gm_list
        if id_check and member_check:
            current_arena = Arena(message,currentWorkLoop)
            current_arena.create_dashboard()
            arena_board.append(current_arena)
        else:
            return
    if message.content.startswith('.stop'):
        
        fetched_arena = [x for x in arena_board if x.gm == message.author and x._stat == "START"]
        
        contents = message.content.split(' ')
        
        if len(contents) == 1:
            lvl = -1
        else:
            lvl = contents[1]
        
        print(fetched_arena)
        if fetched_arena:
            if len(fetched_arena) == 1:
                #####
                arena: Arena = fetched_arena[0]
                arena.update_dashboard()
                arena.set_arena_url(lvl)
                arena.create_end_message()
                arena._stat = "STOP"

                pass
            else:
                #####
                await message.channel.send('侯偷偷開兩場抓到之還沒做好')
                for i in fetched_arena:
                    i.update_dashboard()
                    i._stat = "STOP"
                pass
            for fetched in fetched_arena:
                arena_board.remove(fetched)
            print(arena_board)
        else:
            await message.channel.send('你並沒有啟動任何場次。')
        
        
    
    if message.content.startswith('.rembg'):
        if message.attachments:
            filename = imageProc.toWhitebg(message.attachments[0].url)
            img = discord.File(f'{filename}')
            await message.channel.send(file = img, reference = message)
            os.remove(filename)
        else:
            await message.channel.send('這則訊息不包含圖片。')
    if message.content.startswith('.dl'):
        contents = message.content.split(' ')
        if len(contents) == 1:
            return
        url = contents[1]
        if 'youtu' not in url:
            await message.channel.send('不支援的網站。')
            return
        if 'mp3' in contents[0]:
            mp3 = True
        else:
            mp3 = False
        handler = threading.Thread(target=audio_download_action,args=(message,url,currentWorkLoop,mp3))
        handler.start()

    
    if message.content.startswith('.debug'):
        content = '===debug===\n'
        for i in arena_board:
            i: Arena
            content += i._father_message.jump_url
            content += '\n'
            ref = i._father_message.reference.jump_url
        await message.channel.send(content)
        
@client.event
async def on_reaction_add(reaction: discord.Reaction,user: discord.User):
    if str(reaction) not in arena_emoji_list:
        return
    fetched_arena = [x for x in arena_board if x._father_message.id == reaction.message.id and x._stat == "START"]
    if fetched_arena:
        fetch_lst = ['1-3', '3-5', '5-7', '7-9', '9-11', '11-15']
        arena: Arena = fetched_arena[0]
        for i in range(len(arena_emoji_list)):
            if str(reaction) == arena_emoji_list[i]:
                if f'{user.name}' not in arena._member_list[fetch_lst[i]]:
                    arena._member_list[fetch_lst[i]] += f'\n{user.name}'
        arena.update_dashboard()
        
    else:
        return
    
@client.event
async def on_reaction_remove(reaction: discord.Reaction,user: discord.User):
    if str(reaction) not in arena_emoji_list:
        return
    fetched_arena = [x for x in arena_board if x._father_message.id == reaction.message.id and x._stat == "START"]
    if fetched_arena:
        fetch_lst = ['1-3', '3-5', '5-7', '7-9', '9-11', '11-15']
        arena: Arena = fetched_arena[0]
        for i in range(len(arena_emoji_list)):
            if str(reaction) == arena_emoji_list[i]:
                if f'{user.name}' in arena._member_list[fetch_lst[i]]:
                    arena._member_list[fetch_lst[i]] = arena._member_list[fetch_lst[i]].replace(f'\n{user.name}',"")
        arena.update_dashboard()
    
    
        

def gr_action(message_obj: discord.message.Message, grCount: int, prefer: list, workLoop: asyncio.AbstractEventLoop, sp: bool = False):
    rawGrResultQueue = queue.Queue(0)
    for _ in range(grCount):
        rawGrResultQueue.put(gr.normal())
    if sp:
        asyncio.run_coroutine_threadsafe(send_message(message_obj,gr.main(prefer,rawGrResultQueue)),workLoop)
    else:
        asyncio.run_coroutine_threadsafe(send_message(message_obj,gr.prH(sp,prefer,rawGrResultQueue)),workLoop)

def audio_download_action(message_obj: discord.message.Message, url: str, workLoop: asyncio.AbstractEventLoop, mp3: bool):
    filename = aud_dl.downloader(url)
    if mp3:
        rndname = f"{random.random()}".replace('.','')
        os.rename(filename, f'fx{rndname}xf.m4a')
        rd = aud_dl.tomp3(f"fx{rndname}xf.m4a")
        filename = filename.replace(".m4a","")
        os.rename(f"{rd}",f"{filename}.mp3")
        filename = f'{filename}.mp3'
    rt = discord.File(f'{filename}')
    asyncio.run_coroutine_threadsafe(send_message(message_obj, file = rt),workLoop)
    



token = os.environ.get('TOKEN')
client.run(token)