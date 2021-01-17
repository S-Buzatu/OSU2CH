# OSU2CH

This is a python script used to convert OSU maps into CloneHero charts.

Right now the program only runs from an IDE.
You need to have installed FFmpeg and the python libraries pydub, tkinter and shutil for it to work.
Additionally you need to uncompress the .osz file before you're able to use the script.

To install FFMPEG copy the ffmpeg folder i have in the repo to any location you want, or even leave it in it's current location. Open your windows environment variables and add to the "Path" variable the path to ffmpeg.exe.
e.g: If your ffmpeg folder is in C:\Users then the path you need to add to the "Path" variable is C:\Users\ffmpeg\bin\ffmpeg.exe

I installed the other libraries directly from the Visual Studio Community IDE.

Open an IDE(I used Visual studio community 2019) then hit run. The window that pops-up is for selecting the folder that appeared after you uncompressed the .osz file.
After the script is done you will have a new folder ending with CH. Copy that folder into your CH songs folder and scan for new songs.
Every map is made as a different CH song . Right now every map is turned into a CH different song so you will have a lot songs in the CH menu.


Known issues:

-Converting every map an osu song will put a few notes in the wrong position.

-Notes seem sligthly off (might just be my imagination)

-Sliders and Spinners are converted into a single note as opposed to a long note

Plans for the future:

-Convert sliders and spinners into long notes

-See if i can group all OSU maps for one song into one chart

-Implement a second mapping option that orders notes differently

-Make an installer(i doubt i'll be able to do this one)
