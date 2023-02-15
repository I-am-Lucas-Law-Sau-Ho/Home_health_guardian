import controller as controller
import cv2
import mediapipe as mp
import numpy as np
from tkinter import messagebox 
from matplotlib import pyplot as plt
import subprocess
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import *
import os
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import *
import webbrowser
import PIL.Image

ws = Tk()
ws.title('try_btn')
new = 1
url = 'https://www.canva.com/design/DAE7Y9mhbWI/PBOKmoB1WWus2jsTu12KWA/view?utm_content=DAE7Y9mhbWI&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton'
ws.geometry('354x633')

bg = PhotoImage(file = "canuseinterface.PNG")

canvas = Canvas(
    ws,
    width=500,
    height=400
)
canvas.create_image(0,0,anchor="nw",image=bg)
canvas.pack(fill='both', expand=True)

def nutrients():
    subprocess.call(["python", "d_project.py"])
    #os.system('d_project.py')
def recipe():
    subprocess.call(["python", "recipe_request.py"])
    #os.system('recipe_request.py')
def sports():
    subprocess.call(["python", "register.py"])


def openbrowser():
    webbrowser.open(url, new=new)

#canvas.create_image(0, 0, anchor="nw", image=bg)
#########recipe#########
recipe_btn = Button(ws,text='    ',bg ="#4ED1C1" ,command=recipe,width=6,height=2,borderwidth=0,font=('arial', 18))
btn_canvas = canvas.create_window(72,360,anchor="nw",window=recipe_btn)
#########recipe#########

########nutrients######

nutrient_btn = Button(ws,text='    ',bg ="#F0657A" ,command=nutrients,width=6,height=2,borderwidth=0,font=('arial', 18))
btn_canvas = canvas.create_window(240,360,anchor="nw",window=nutrient_btn)
########nutrients######

##########sport######
# sport_btn = Button(ws,text='    ',bg ="#FFD386" ,command=recipy,width=6,height=2,borderwidth=0,font=('arial', 18))
# btn_canvas = canvas.create_window(72,498,anchor="nw",window=sport_btn)
#sport_btn = Button(ws,text='    ',bg ="#FFD386" ,command=quitwindows())
sport_btn = Button(ws,text='    ',bg ="#FFD386" ,command=sports,width=6,height=2,borderwidth=0,font=('arial', 18))
btn_canvas = canvas.create_window(72,498,anchor="nw",window=sport_btn)


#squart_btn = Button(chooseme, text="Squart",command = square)
##########sport######
#########project link####################
project_link_btn = Button(ws,text='    ',bg ="#86DDFF" ,command=openbrowser,width=6,height=2,borderwidth=0,font=('arial', 18))
btn_canvas = canvas.create_window(240,498,anchor="nw",window=project_link_btn)
#########project link####################




ws.mainloop()

#cv2.destroyAllWindows()
