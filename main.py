import pygame,glob,datetime,threading,math
from time import sleep
import tkinter as tkr
from mutagen.mp3 import MP3

player=tkr.Tk()
player.title("mp3 player")
player.geometry("505x240")

file_name=tkr.StringVar()
time_text_end=tkr.StringVar()
time_text_str=tkr.StringVar()
time_temp=0
time=tkr.StringVar()
time.set("0")
time_text_end.set("/ 0:00:00")
time_text_str.set("0:00:00")
file=""
elements=5
progress=""
playlist=tkr.Listbox(player,highlightcolor="blue",selectmode=tkr.SINGLE)
next_file=""
pause=False
stop_threads=True
songs=[]
for song in glob.glob("*.mp3"):
    songs.append(song)
song_list_not_org=[]
pos=0
def fix():
 global pos,song_list_not_org
 for song in songs:

  char_list = [song[j] for j in range(len(song)) if ord(song[j]) in range(65536)]
  song = ''
  for j in char_list:
   song = song + j
  song_list_not_org.append(str(song_list_not_org.__len__() + 1) + "." + song)
  playlist.insert(pos,song_list_not_org[-1])
  pos += 1
fix()
def count_time():
 global stop_threads,progress,pause
 print(stop_threads)
 while stop_threads and str(time_text_end.get())[1:]!=str(time_text_str.get()):
  while pause==True:
   pass
  sleep(0.1)
  if progress.get()<float(time.get())-2 or progress.get()>float(time.get())+2:
   time.set(int(progress.get()))
   pygame.mixer.music.stop()
   pygame.mixer.music.load(songs[song_list_not_org.index(file)])
   pygame.mixer.music.play(0,int(float(time.get())))
  else:
   time.set(str(float(time.get())+0.1))
   progress.set(float(time.get()))
  time_text_str.set(str(datetime.timedelta(seconds=round(float(time.get())))))
  #print(time.get())
 time.set("0")
 time_text_str.set("0")
 stop_threads=True

def play():
 global pause,progress,stop_threads,file
 if pause==True and file==playlist.get(tkr.ACTIVE):
  pygame.mixer.music.unpause()
  pause=False
  return 0
 if file!="" and file!=playlist.get(tkr.ACTIVE):
  pause=False
  stop_threads=False
  time.set("0")
 pygame.init()
 pygame.mixer.init()
 temp_file_name=songs[song_list_not_org.index(playlist.get(tkr.ACTIVE))]
 pygame.mixer.music.load(temp_file_name)
 file=playlist.get(tkr.ACTIVE)
 pygame.mixer.music.play(0,int(float(time.get())))
 audio = MP3(temp_file_name)
 print(audio.info.length)
 cutter=int(math.log10(int(song_list_not_org.index(playlist.get(tkr.ACTIVE))))+2)
 file_name.set(str(playlist.get(tkr.ACTIVE))[cutter:])
 time_text_end.set(str("/"+str(datetime.timedelta(seconds=round(audio.info.length,0)))))
 progress = tkr.Scale(player, from_=0, to_=round(audio.info.length,0), orient=tkr.HORIZONTAL, resolution=0.1)
 progress.grid(row=2, columnspan=elements, sticky=tkr.EW)
 x = threading.Thread(target=count_time, args=())
 x.start()

def pause():
 global pause
 pygame.mixer.music.pause()
 pause=True
 return 0

def Next():
 global songsm,file
 stop_threads = False
 if songs[-1] == file_name.get():
  next_file=(songs[0])
 else:
  next_file =(songs[songs.index(file_name.get()) + 1])

 playlist.activate(songs.index(next_file))
 file = playlist.get(tkr.ACTIVE)
 pygame.mixer.music.stop()
 time.set("0")
 time_text_str.set("0")
 play()
 return 0


def test():
 global pause, x, stop_threads
 pause = False
 try:
  if x.is_alive() == False:
   x.start()
  else:
   if file_name.get() !=playlist.get(tkr.ACTIVE):
    stop_threads = False
 except:
  x = threading.Thread(target=play, args=())
  x.start()


Butten_play=tkr.Button(player,text="PLAY",command=play)
Butten_stop=tkr.Button(player,text="PAUSE",command=pause)
Butten_next=tkr.Button(player,text="NEXT",command=Next)
current_song=tkr.Label(player,textvariable=file_name)
time_text_str.set("0.0")
time_text=tkr.Label(player,textvariable=time_text_str)
time_end=tkr.Label(player,textvariable=time_text_end)
progress=tkr.Scale(player,from_=0,to_=time.get(),orient=tkr.HORIZONTAL,resolution=0.1)

Butten_play.grid(row=3,sticky="w")
Butten_stop.grid(row=3,column=1, sticky="w")
Butten_next.grid(row=3,column=2,sticky="w")
time_text.grid(row=3,column=3,sticky="w")
time_end.grid(row=3,column=4,sticky="w")

progress.grid(row=2,columnspan=elements,sticky=tkr.EW)
current_song.grid(row=1,columnspan=elements,sticky=tkr.N)
playlist.grid(row=0,columnspan=elements,sticky="NSEW")

player.columnconfigure(0, weight=1)
player.columnconfigure(1, weight=1)
player.columnconfigure(2, weight=1)
player.columnconfigure(3, weight=1)
player.columnconfigure(4, weight=5000)
player.rowconfigure(0, weight=1)
player.rowconfigure(1, weight=1)
player.rowconfigure(2, weight=1)
player.rowconfigure(3, weight=1)
player.mainloop()

player.mainloop()
