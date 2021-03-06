from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import os
import tkinter as tk
from PIL import Image, ImageTk

global init
init=0
global fln
global fln2
global img1
global img2
def showimage():
    valor=comboExample.get()
    if valor is "":
        print("indefinido")
    else:
        global init
        global fln
        global fln2
        global img1
        global img2
        if init==0:
            fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("IMAGE File", "*.jpg *.jpeg *.png"),("JPG File", "*.jpg"),("JPGE File", "*.jpeg"), ("PNG file", "*.png"), ("ALL Files", "*.*")))
            fln2 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("IMAGE File", "*.jpg *.jpeg *.png"),("JPG File", "*.jpg"),("JPGE File", "*.jpeg"), ("PNG file", "*.png"), ("ALL Files", "*.*")))
            img1 = Image.open(fln)
            img2 = Image.open(fln2)
        init=1
        if valor == "anaglifo":
            result=make_anaglyph(img1,img2,"color","testresult.jpg")
        if valor == "anaglifo2":
            result=make_anaglyph(img1,img2,"mono","testresult.jpg")
        if valor == "anaglifo3":
            result=make_anaglyph(img1,img2,"halfcolor","testresult.jpg")
        if valor == "anaglifo4":
            result=make_anaglyph(img1,img2,"optimized","testresult.jpg")
        if valor == "izq-der":
            result=make_stereopair(img1,img2,"color","testresult.jpg")
        if valor == "der-izq":
            result=make_stereopair2(img1,img2,"color","testresult.jpg")
        if valor == "top-down":
            result=make_stereopair3(img1,img2,"color","testresult.jpg") #aqui se crea la imagen en anaglyph
        

        img = ImageTk.PhotoImage(result)
        lbl.configure(image=img)
        lbl.image = img

matrices = {
    'true': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0.299, 0.587, 0.114 ] ],
    'mono': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0.299, 0.587, 0.114, 0.299, 0.587, 0.114 ] ],
    'color': [ [ 1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
    'halfcolor': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
    'optimized': [ [ 0, 0.7, 0.3, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
}
def make_anaglyph(left, right, color, path):
 #redimensionar
    width, height = left.size
    r=900/width
    print(r)
    print(width)
    print(height)
    left= left.resize((int(width*r),int(height*r)), Image.ANTIALIAS)
    right= right.resize((int(width*r),int(height*r)), Image.ANTIALIAS)
    print(left.size)

    width, height = left.size
    leftMap = left.load()
    rightMap = right.load()
    m = matrices[color]

    for y in range(0, height):
        for x in range(0, width):
            r1, g1, b1 = leftMap[x, y]
            r2, g2, b2 = rightMap[x, y]
            leftMap[x, y] = (
                int(r1*m[0][0] + g1*m[0][1] + b1*m[0][2] + r2*m[1][0] + g2*m[1][1] + b2*m[1][2]),
                int(r1*m[0][3] + g1*m[0][4] + b1*m[0][5] + r2*m[1][3] + g2*m[1][4] + b2*m[1][5]),
                int(r1*m[0][6] + g1*m[0][7] + b1*m[0][8] + r2*m[1][6] + g2*m[1][7] + b2*m[1][8])
            )
    left.save(path)
    return left

def make_stereopair(left, right, color, path):
  #redimensionar
    width, height = left.size
    r=560/height
    left= left.resize((int(width*r),int(height*r)), Image.ANTIALIAS)
    right= right.resize((int(width*r),int(height*r)), Image.ANTIALIAS)

    width, height = left.size
    leftMap = left.load()
    rightMap = right.load()
    pair = Image.new('RGB', (width * 2, height))
    pairMap = pair.load()
    for y in range(0, height):
        for x in range(0, width):
            pairMap[x, y] = leftMap[x, y]
            pairMap[x + width, y] = rightMap[x, y]
    if color == 'mono':
        pair = pair.convert('L')
    pair.save(path)
    return pair
def make_stereopair2(right, left, color, path):
  #redimensionar
    width, height = left.size
    r=560/height
    left= left.resize((int(width*r),int(height*r)), Image.ANTIALIAS)
    right= right.resize((int(width*r),int(height*r)), Image.ANTIALIAS)

    width, height = left.size
    leftMap = left.load()
    rightMap = right.load()
    pair = Image.new('RGB', (width * 2, height))
    pairMap = pair.load()
    for y in range(0, height):
        for x in range(0, width):
            pairMap[x, y] = leftMap[x, y]
            pairMap[x + width, y] = rightMap[x, y]
    if color == 'mono':
        pair = pair.convert('L')
    pair.save(path)
    return pair
def make_stereopair3(left, right, color, path):
    #redimensionar
    width, height = left.size
    r=320/height
    left= left.resize((int(width*r*2),int(height*r)), Image.ANTIALIAS)
    right= right.resize((int(width*r*2),int(height*r)), Image.ANTIALIAS)

    width, height = left.size
    leftMap = left.load()
    rightMap = right.load()
    pair = Image.new('RGB', (width , height * 2))
    pairMap = pair.load()
    for y in range(0, height):
        for x in range(0, width):
            pairMap[x, y] = leftMap[x, y]
            pairMap[x, y + height] = rightMap[x, y]
    if color == 'mono':
        pair = pair.convert('L')
    pair.save(path)
    return pair
root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

lbl = Label(root)
lbl.pack()
lbl.pack(fill=BOTH, expand=YES)

btn = Button(frm, text="Cargar imagen", command=showimage)
btn.pack(side=tk.LEFT)

comboExample = Combobox(frm, 
                            values=[
                                    "anaglifo",
                                    "anaglifo2", 
                                    "anaglifo3", 
                                    "anaglifo4",  
                                    "izq-der",
                                    "der-izq",
                                    "top-down"])
comboExample.pack(side=tk.LEFT, padx=10)

btn2 = Button(frm, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT, padx=10)


root.title("Image Browser")
root.geometry("300x350")
root.mainloop()