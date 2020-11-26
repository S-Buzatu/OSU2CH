#OSU2CH v0.1
#Check this for slider calculations https://osu.ppy.sh/community/forums/topics/606522
#Slider duration (600* sliderlength)/(slidervelocity*bpm) ; 600* sliderlength * beatduration/slidervelocity
#Formula translation from time to CH position. coef=768/beatLength. pos=coef*time. You fogot to account for the offset dumbass
#It compiles, but the positions are wrong.
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
from shutil import copyfile

timing_point_list = []

root = tk.Tk()
root.withdraw()

osu_folder_path = filedialog.askdirectory()
if not os.path.exists(osu_folder_path + " CH"):
        os.makedirs(osu_folder_path + " CH")
ch_folder_path = osu_folder_path + " CH"
read_objects = 0
read_timing = 0
timing_point_number = 0
#osu_file_path = filedialog.askopenfilename()
#song_file_path = filedialog.askopenfilename()

class Timingpoint:
    def __init__(self, time, beat_length):
        self.time = time
        self.beat_length = beat_length



for entry in os.listdir(osu_folder_path):
    if os.path.isfile(os.path.join(osu_folder_path, entry)):
        if entry.find(".mp3")>-1:
            print(entry)
            song = AudioSegment.from_mp3(os.path.join(osu_folder_path, entry))
            print("Song duration "+str(int(song.duration_seconds*1000)))
            song.export(ch_folder_path+'/song.ogg', format="ogg")

for entry in os.listdir(osu_folder_path):
    if os.path.isfile(os.path.join(osu_folder_path, entry)):
        if entry.find(".osu")>-1:
            print(entry)
            map_name = entry
            map_name = map_name.replace(".osu","")
            if not os.path.exists(ch_folder_path + "/"+map_name):
                os.makedirs(ch_folder_path + "/"+map_name)

            r = open(os.path.join(osu_folder_path, entry),'r', errors="ignore")
            chart = open(ch_folder_path + "/"+map_name+'/notes.chart','w')
            ini = open(ch_folder_path + "/"+map_name+'/song.ini','w')
            copyfile(ch_folder_path+"/song.ogg", ch_folder_path + "/"+map_name+"/song.ogg")
            file_lines = r.readlines()

            ini.write("[Song]\n")
            ini.write("name = "+map_name+"\n")
            ini.write("artist = 1TEST\n")
            ini.write("album = OSU\n")
            ini.write("genre = Anime\n")
            ini.write("year = 1\n")
            ini.write("song_length = "+str(int(song.duration_seconds*1000))+"\n")
            ini.write("count = 0\n")
            ini.write("diff_band = -1\n")
            ini.write("diff_guitar = -1\n")
            ini.write("diff_bass = -1\n")
            ini.write("diff_drums = -1\n")
            ini.write("diff_keys = -1\n")
            ini.write("diff_guitarghl = -1\n")
            ini.write("diff_bassghl = -1\n")
            ini.write("preview_start_time = 0\n")
            ini.write("frets = 0\n")
            ini.write("charter = OSU2CH\n")
            ini.write("icon = 0\n")

            ini.close()

            chart.write("[Song]")
            chart.write("\n")
            chart.write("{")
            chart.write("\n")
            chart.write("Name = \"1TEST\"")
            chart.write("\n")
            chart.write("Artist = \"1TEST\"")
            chart.write("\n")
            chart.write("Charter = \"OSU2CH\"")
            chart.write("\n")
            chart.write("Album = \"1TEST\"")
            chart.write("\n")
            chart.write("Year = \", 1\"")
            chart.write("\n")
            chart.write("Offset = 0")
            chart.write("\n")
            chart.write("Resolution = 192")
            chart.write("\n")
            chart.write("Player2 = bass")
            chart.write("\n")
            chart.write("Difficulty = 0")
            chart.write("\n")
            chart.write("PreviewStart = 0")
            chart.write("\n")
            chart.write("PreviewEnd = 0")
            chart.write("\n")
            chart.write("Genre = \"Anime\"")
            chart.write("\n")
            chart.write("MediaType = \"cd\"")
            chart.write("\n")
            chart.write("MusicStream = \"song.ogg\"")
            chart.write("\n")
            chart.write("}")
            chart.write("\n")


            for line in file_lines:
                #Add timing 
                result = line.find("TimingPoints")
                if result > -1:
                    read_timing=1
                    chart.write("[SyncTrack]\n")
                    chart.write("{\n")
                    chart.write("  0 = TS 4\n")
                    chart.write("  0 = B 200000\n")
                    chart.write("}\n")
                    chart.write("[Events]\n")
                    chart.write("{\n")
                    chart.write("}\n")
                    continue

                if read_timing:
                    words = line.split(",")
                    if words[0] != '\n':
                        if float(words[1]) > 0:
                            #x=Timingpoint
                            #x.time=int(words[0])
                            #x.beat_length=float(words[1])
                            timing_point_list.append(Timingpoint(int(words[0]),float(words[1])))
                            print("Append timing point "+str(int(words[0]))+" , "+str(float(words[1])))
                    else:
                        read_timing=0
                        print("Timing points: "+str(len(timing_point_list)))
                 

                
                #Add notes
                result = line.find("HitObjects")
                if result > -1:
                    read_objects=1
                    chart.write("[ExpertSingle]\n")
                    chart.write("{\n")

                    for point in timing_point_list:
                        print("Position: "+str(timing_point_list.index(point))+" Time: "+str(point.time))
                    print("Initial timing point number: "+str(timing_point_number))

                    continue
                if read_objects:
                    words = line.split(",")
                    if words[0] != '\n':
                        lane = int(int(words[0])/102)
                        if lane == 5:
                            lane=lane-1
                        #position = str(round(int(words[2])*0.5441
                        if ((int(words[2]) >= timing_point_list[len(timing_point_list)-1].time)) :
                            coef = 768/timing_point_list[timing_point_number].beat_length
                            print("Keep current timing point")
                            print("Timing point: Value: "+str(timing_point_list[timing_point_number].time)+" Number: "+str(timing_point_number))
                            position = round(coef * int(words[2])/4)
                            newline = "  "+str(position)+" = N "+str(lane)+" 0\n"
                            chart.write(newline)
                        elif ((timing_point_list[timing_point_number].time <= int(words[2])) & (int(words[2]) < timing_point_list[timing_point_number+1].time)):
                            coef = 768/timing_point_list[timing_point_number].beat_length
                            print("Keep current timing point")
                            print("Timing point: Value: "+str(timing_point_list[timing_point_number].time)+" Number: "+str(timing_point_number))
                            position = round(coef * int(words[2])/4)
                            newline = "  "+str(position)+" = N "+str(lane)+" 0\n"
                            chart.write(newline)
                        else :
                            timing_point_number += 1
                            print("Timing point added: Value: "+str(timing_point_list[timing_point_number].time)+" Number: "+str(timing_point_number))
                            coef = 768/timing_point_list[timing_point_number].beat_length
                            position = round(coef * int(words[2])/4)
                            newline = "  "+str(position)+" = N "+str(lane)+" 0\n"
                            chart.write(newline)
            chart.write("}\n")
            r.close()
            chart.close()
            read_objects=0
if os.path.exists(ch_folder_path+"/song.ogg"):
    os.remove(ch_folder_path+"/song.ogg")

    