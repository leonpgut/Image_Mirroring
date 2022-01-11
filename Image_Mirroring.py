from PIL import Image, ImageOps, ImageTk
import tkinter as tk
from tkinter import filedialog as fd
import sys
from functools import partial
import pyglet


def getpath():
    rot = tk.Tk()
    rot.withdraw()
    files = [('Image', ['*.png', '*.jpg', "*.jpeg"])]
    name = fd.askopenfilename(filetypes = files, defaultextension = files)
    rot.destroy()
    return name

def checkfile(path):
    if not path:
        sys.exit("Didn't choose a file.")
    filetype = path.split('.')[-1].lower()
    possiblefiles = ["png", "jpg", "jpeg"]
    if not filetype in possiblefiles:
        sys.exit("File not supported. Try png or jpg.")
    
def on_main_click(canvas, rect, event):
    global posi, move
    if move:
        x, y = event.x, event.y
        canvas.coords(rect, x-2, 0, x+2, h)
        posi = x

def click(canvas, rect, event):
    global move
    x, y = event.x, event.y
    if canvas.coords(rect)[0] - 5 < x and x < canvas.coords(rect)[2] + 5:
        move = True
    else:
        move = False

def mouse_motion(canvas, rect, event):
    x, y = event.x, event.y
    if canvas.coords(rect)[0] - 5 < x and x < canvas.coords(rect)[2] + 5:
        canvas.config(cursor="hand2")
    else:
        canvas.config(cursor="")

def quit(root, event):
    name = path.split('/')[-1]
    ml = mirrorleft(img)
    mr = mirrorright(img)
    print("Mirrored " + name + " successfully.")
    root.destroy()
    print("Choose a location to save the mirrored left half.")
    saveas(ml)
    print("Choose a location to save the mirrored right half.")
    saveas(mr)

def mirrorleft(img):
    h = img.size[1]
    lefthalf = img.crop([0, 0, posi, h])
    lefthalfmir = ImageOps.mirror(lefthalf)
    return concatenate(lefthalf, lefthalfmir)

def mirrorright(img):
    w, h = img.size
    righthalf = img.crop([posi, 0, w, h])
    righthalfmir = ImageOps.mirror(righthalf)
    return concatenate(righthalfmir, righthalf)

def concatenate(img1, img2):
    result = Image.new('RGB', (img1.width + img2.width, img1.height))
    result.paste(img1, (0, 0))
    result.paste(img2, (img1.width, 0))
    return result

def saveas(img):
    rot = tk.Tk()
    rot.withdraw()
    files = [('PNG', '*.png'),
             ('JPEG', '*.jpg')]
    savepath = fd.asksaveasfile(filetypes = files, defaultextension = files)
    if savepath:
        img.save(savepath.name)
        print("Saved image successfully at " + savepath.name + ".")
    else:
        print("Did not save the image.")
    rot.destroy() 

def gui(img):
    root = tk.Tk()
    root.title("Image Mirroring")
    root.focus_force()
    root.geometry(str(w) + "x" + str(h))
    root.resizable(0,0)
    canvas = tk.Canvas(root, width = w, height = h)      
    canvas.pack()   
    tkimage = ImageTk.PhotoImage(master=canvas, image=img)
    canvas.create_image(0,0, anchor=tk.NW, image=tkimage)
    rect = canvas.create_rectangle(posi-2, 0, posi+2, h, fill="black", outline="white")
    canvas.bind('<B1-Motion>', partial(on_main_click, canvas, rect))
    canvas.bind('<1>', partial(click, canvas, rect))
    canvas.bind('<Motion>', partial(mouse_motion, canvas, rect))
    root.bind('<KeyPress>', partial(quit, root))
    root.mainloop()

print("Choose an image to be mirrored.")
path = getpath()
checkfile(path)
print("Click to place the mirror axis.\nPress any key to confirm.")
img = Image.open(path).convert("RGBA")
w, h = img.size
posi = w/2
move = False
gui(img)