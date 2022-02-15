from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
from PIL import Image, ImageTk

def showimage():
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("ALL Files", "*.*")))
    fln2 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("ALL Files", "*.*")))
    img1 = Image.open(fln)
    img2 = Image.open(fln2)
    
    result=make_stereopair3(img1,img2,"color","testresult.jpg")
    # result=make_anaglyph(img1,img2,"color","testresult.jpg") #aqui se crea la imagen en anaglyph
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

btn = Button(frm, text="Cargar imagen", command=showimage)
btn.pack(side=tk.LEFT)

btn2 = Button(frm, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT, padx=10)


root.title("Image Browser")
root.geometry("300x350")
root.mainloop()