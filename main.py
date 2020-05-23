import pygame, threading,os,glob,datetime,timeit
import time as Time
from pydub import AudioSegment
import tkinter as tkr
import multiprocessing
from itertools import product
temp=threading.activeCount()
player=tkr.Tk()
rate=1
player.title("Audio player")
player.geometry("405x240")
file=tkr.StringVar()
file_name=tkr.StringVar()
time_text_str=tkr.StringVar()
time=tkr.StringVar()
time.set("0.0")

time_text_end=tkr.StringVar()
time_text_end.set("/ 0:00:00")
time_text_str.set("0:00:00")

wf=""
next_bool=False
pause=False
index_time=0
song_list=[]
song_list_not_org=[]
elements=5
global p
progress=""
#default_index=0
playlist=tkr.Listbox(player,highlightcolor="blue",selectmode=tkr.SINGLE)
songs=[]

lst=[]
def works(song):
    global song_list,song_list_not_org,pos
    if os.path.getsize(os.getcwd() + "\\" + song)//1000000<40:
        try:
            # print(song)
            print("Fail" + song, os.path.getsize(os.getcwd() + "\\" + song))
            #wf = AudioSegment.from_file_using_temporary_files(song)
            song_list.append(song)
            char_list = [song[j] for j in range(len(song)) if ord(song[j]) in range(65536)]
            song = ''
            for j in char_list:
                song = song + j
            song_list_not_org.append(str(song_list_not_org.__len__()+1)+"."+song)
            #playlist.delete(0, tkr.END)
            #for song in song_list_not_org:
            #    playlist.insert(pos, song)
            #    pos += 1
            ## print("Pass-------" + song, os.path.getsize(os.getcwd() + "\\" + song))
        except:
            print("Fail" + song, os.path.getsize(os.getcwd() + "\\" + song))
            pass

for song in glob.glob("*.mp3"):
    #song_list.append(song)
    works(song)
    #t = threading.Thread(target=works, args=(song,))
    #t.start()
pos=0
for song in song_list_not_org:
    playlist.insert(pos, song)
    pos += 1
stream=""
stop_threads=False
def stream_builder(file):
    import pyaudio
    import wave
    global p
    filename = file

    # Set chunk size of 1024 samples per data frame
    chunk = 1024

    # Open the sound file
    # wf = wave.open(filename, 'rb')
    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format=p.get_format_from_width(wf.sample_width),
                    channels=wf.channels,
                    rate=wf.frame_rate,
                    output=True)

    return stream
def Play():
    global file,index_time,time,progress,next_bool
    global stream,wf,stop_threads,time_text_end

    #if next_bool:
    #    next_bool=False
    #    index_time=0
    #    file.set(playlist.selection_get())
    #    wf = AudioSegment.from_file(str(file.get()))
    #    stream=stream_builder(str(file.get()))
    #    temp=wf.frame_count()/wf.frame_rate
#
    #    progress = tkr.Scale(player, from_=0.0, to_=round(temp,1), orient=tkr.HORIZONTAL, resolution=0.1)
    #    progress.grid(row=2,columnspan=elements,sticky=tkr.EW)
    if  file.get()!=playlist.get(tkr.ACTIVE) or next_bool:
        index_time=0
        file.set(playlist.get(tkr.ACTIVE))
        file_name.set(song_list[song_list_not_org.index(file.get())])
        print(file.get())
        #file_w="Øfdream - Thelema [ Bass boosted,Slowed ]-y5C.mp3"

        wf = AudioSegment.from_file_using_temporary_files(song_list[song_list_not_org.index(file.get())])
        #wf = AudioSegment.from_file_using_temporary_files(file_w)
        stream=stream_builder(song_list[song_list_not_org.index(file.get())])###

        temp=wf.frame_count()/wf.frame_rate
        time_str_format = str(datetime.timedelta(seconds=wf.frame_count()//wf.frame_rate))
        if temp<3600:
            time_str_format=time_str_format[2:]
        time_text_end.set("/"+time_str_format)


        progress = tkr.Scale(player, from_=0.0, to_=wf.frame_count()//wf.frame_rate, orient=tkr.HORIZONTAL, resolution=0.1)
        progress.grid(row=2,columnspan=elements,sticky=tkr.EW)

    # Read data in chunks

    # Play the sound by writing the audio data to the stream
    i=index_time*4410+1
    data = wf.get_frame(i-1)
    print(wf.frame_rate, wf.frame_count()/wf.frame_rate)

    while data != ''  and stop_threads==False:
        while i % 4410 != 0 and stop_threads==False:
            stream.write(data)
            data = wf.get_frame(i)
            i += 1
        while pause and stop_threads==False:
            pass
        print(progress.get())
        if progress.get() < round(i / 44100, 2) - 1 or progress.get() > round(i / 44100, 2) + 1:
            i = int(progress.get() * 4410) * 10
            data = wf.get_frame(i)
        else:
            index_time = i // 4410

        ## time
        time_str_format=str(datetime.timedelta(seconds=i // 44100))
        if wf.frame_count()/wf.frame_rate<3600:
            time_str_format=time_str_format[2:]
        time_text_str.set(time_str_format)
        # print(round(i / 44100,2),wf.__len__()//4410,progress.get())

        progress.set(round(i / 44100, 2))
        stream.write(data)
        data = wf.get_frame(i + 1)
        i += 1
    x = threading.Thread(target=Play, args=())
    stop_threads = False
    # Close and terminate the stream
global x
def Stop():
    global pause,x
    pause=True

def test():
    global pause,x,stop_threads
    pause=False
    try:
        if x.is_alive() == False:
            x.start()
        else:
            if file.get()!=song_list[song_list_not_org.index(playlist.get(tkr.ACTIVE))]:
                stop_threads = True
                test()
    except:

        x = threading.Thread(target=Play, args=())
        x.start()

def Next():
    global file,stop_threads,next_bool,x,pause
    pause=False
    next_song=""
    lst=[]
    for song in song_list_not_org:
        lst.append(song)
        print(song)


    if lst[-1]==file.get():
        file.set(lst[0])
    else:
        file.set(lst[lst.index(file.get())+1])
    playlist.activate(lst.index(file.get()))
    playlist.selection_clear(0,lst.__len__())
    playlist.select_set(lst.index(file.get()))
    print(tkr.ACTIVE)
    next_bool=True
    if x.is_alive():
        stop_threads = True
        Time.sleep(1)
        x = threading.Thread(target=Play, args=())
        x.start()

Butten_play=tkr.Button(player,text="PLAY",command=test)
Butten_stop=tkr.Button(player,text="PAUSE",command=Stop)
Butten_next=tkr.Button(player,text="NEXT",command=Next)
current_song=tkr.Label(player,textvariable=file_name)
time_text_str.set("0.0")
time_text=tkr.Label(player,textvariable=time_text_str)
time_end=tkr.Label(player,textvariable=time_text_end)


progress=tkr.Scale(player,from_=0.0,to_=time.get(),orient=tkr.HORIZONTAL,resolution=0.1)

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
stream.close()
p.terminate()
