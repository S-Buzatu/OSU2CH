#OSU2CH v0.5
#Check this for slider calculations https://osu.ppy.sh/community/forums/topics/606522
#Slider duration (600* sliderlength)/(slidervelocity*bpm) ; 600* sliderlength * beatduration/slidervelocity
#Beat duration to BPM formula : BPM = 1000*60/beatLength
#Formula translation from time to CH position. coef=768/beatLength. pos=coef*time/4. 
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
from shutil import copyfile
from IniWritter import write_ini
from ChartWritter import write_song_data

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
offset_time = 0
offset_position = 0

class Timingpoint:
    def __init__(self, time, beat_length, position):
        self.time = time
        self.beat_length = beat_length
        self.position = position

def calc_pos( time ):

    print("Timing point: Value: "+str(timing_point_list[timing_point_number].time)+" Number: "+str(timing_point_number))
    coef = 768/timing_point_list[timing_point_number].beat_length
    dtime = time - timing_point_list[timing_point_number].time
    dpos = round(coef * dtime/4)
    position = dpos + timing_point_list[timing_point_number].position
    newline = "  "+str(position)+" = N "+str(lane)+" 0\n"

    return newline


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
            copyfile(ch_folder_path+"/song.ogg", ch_folder_path + "/"+map_name+"/song.ogg")
            file_lines = r.readlines()
            write_ini(ch_folder_path,map_name,song)
            chart = open(ch_folder_path + "/"+map_name+'/notes.chart','w')
            write_song_data(chart)

            for line in file_lines:
                #Add timing 
                result = line.find("TimingPoints")
                if result > -1:
                    read_timing=1
                    chart.write("[SyncTrack]\n")
                    chart.write("{\n")
                    chart.write("  0 = TS 4\n")
                    chart.write("  0 = B 100000\n")
                    timing_point_list.append(Timingpoint(0,600,0))
                    continue

                if read_timing:
                    words = line.split(",")
                    if words[0] != '\n':
                        if float(words[1]) > 0:
                            time = int(words[0])
                            beat_length = float(words[1])
                            dtime = time - timing_point_list[len(timing_point_list)-1].time
                            coef = 768/timing_point_list[len(timing_point_list)-1].beat_length
                            dpos = round(coef * dtime/4)
                            position = dpos + timing_point_list[len(timing_point_list)-1].position
                            chart.write("  "+str(position) + " = B "+ str(round(60 * 1000 / beat_length)) +"000\n")
                            timing_point_list.append(Timingpoint(time,beat_length,position))
                            print("Append timing point "+str(time)+" , "+str(beat_length)+" , "+ str(position))
                    else:
                        read_timing=0
                        chart.write("}\n")
                        chart.write("[Events]\n")
                        chart.write("{\n")
                        chart.write("}\n")
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
                        if ((int(words[2]) >= timing_point_list[len(timing_point_list)-1].time)) :
                            print("Keep current timing point")
                            chart.write(calc_pos(int(words[2])))
                        elif ((timing_point_list[timing_point_number].time <= int(words[2])) & (int(words[2]) < timing_point_list[timing_point_number+1].time)):
                            print("Keep current timing point")
                            chart.write(calc_pos(int(words[2])))
                        else :
                            while (int(words[2]) >= timing_point_list[timing_point_number].time) :
                                timing_point_number += 1
                                if timing_point_number > len(timing_point_list)-1:
                                    break
                            timing_point_number -= 1
                            chart.write(calc_pos(int(words[2])))
            chart.write("}\n")
            r.close()
            chart.close()
            read_objects=0
if os.path.exists(ch_folder_path+"/song.ogg"):
    os.remove(ch_folder_path+"/song.ogg")

    