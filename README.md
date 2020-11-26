# OSU2CH

This is a python script used to convert OSU maps into CloneHero charts.

Shit's fucked right now. I swear it was working last time i checked.

Right now the program only runs from an IDE.
You need to have installed FFmpeg and the python libraries pydub, tkinter and shutil for it to work.
Additionally you need to uncompress the .osz file before you're able to use the script.

Open an IDE(I used Visual studio community 2019) then hit run. The window that pops-up is for selecting the folder that appeared after you uncompressed the .osz file.
After the script is done you will have a new folder ending with CH. Copy that folder into your CH songs folder and scan for new songs.
Every map is made as a different CH song because you can't correlate the number of CH difficulties with the number of OSU maps that a song might have.


Known issues:

-Synchronization can be way off depeding on the OSU map

-Sliders and Spinners are converted into a single note as opposed to a long note

Plans for the future:

-Fix synchronization

-Convert sliders and spinners into long notes

-Implement a second mapping option that orders notes differently

-Make an installer(i doubt i'll be able to do this one)
