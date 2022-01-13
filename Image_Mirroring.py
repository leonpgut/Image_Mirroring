from PIL import Image, ImageOps, ImageTk
import tkinter as tk
from tkinter import filedialog as fd
import sys
from functools import partial


def getpath():
    print("Choose an image to be mirrored.")
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
    global posi, move, w
    if move:
        x, y = event.x, event.y
        if x > 1 and x < w - 2:
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
    showresults(ml, mr)

def showresults(left, right):
    root = tk.Tk()
    root.title("Image Mirroring")
    root.focus_force()
    w = left.size[0] + right.size[0]
    h = left.size[1]
    root.geometry(str(w) + "x" + str(h + 60))
    root.resizable(0,0)
    canvas = tk.Canvas(root, width = w, height = h)      
    canvas.pack()   
    l = ImageTk.PhotoImage(master=canvas, image=left)
    r = ImageTk.PhotoImage(master=canvas, image=right)
    canvas.create_image(0, 0, anchor=tk.NW, image=l)
    canvas.create_image(left.size[0], 0, anchor=tk.NW, image=r)
    frame = tk.Frame(root, width = w, height = 60)
    frame.pack()
    butl = tk.Button(frame, text="Save left", command=partial(saveas, left))
    butl.place(x=0, y=0, height=60, width=left.size[0])
    butr = tk.Button(frame, text="Save right", command=partial(saveas, right))
    butr.place(x=left.size[0], y=0, height=60, width=right.size[0])
    root.mainloop()

def left_key(canvas, rect, event):
    global posi, w
    l = canvas.coords(rect)[0]
    r = canvas.coords(rect)[2]
    if posi > 2:
        canvas.coords(rect, l-1, 0, r-1, h)
        posi -= 1

def right_key(canvas, rect, event):
    global posi
    l = canvas.coords(rect)[0]
    r = canvas.coords(rect)[2]
    if posi < w - 3:
        canvas.coords(rect, l+1, 0, r+1, h)
        posi += 1

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
    result = Image.new('RGBA', (img1.width + img2.width, img1.height))
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

def bind_events(root, canvas, rect):
    canvas.bind('<B1-Motion>', partial(on_main_click, canvas, rect))
    canvas.bind('<1>', partial(click, canvas, rect))
    canvas.bind('<Motion>', partial(mouse_motion, canvas, rect))
    root.bind('<Left>', partial(left_key, canvas, rect))
    root.bind('<Right>', partial(right_key, canvas, rect))
    canvas.bind('<Right>', partial(mouse_motion, canvas, rect))
    root.bind('<Return>', partial(quit, root))
    root.bind('<space>', partial(quit, root))

def gui(img):
    print("Use the mouse to drag the mirror axis or move it using the arrow keys.\nPress the Confirm-Button, Space key or Enter key to confirm.")
    root = tk.Tk()
    root.title("Image Mirroring")
    root.focus_force()
    root.geometry(str(w) + "x" + str(h + 60))
    root.resizable(0,0)
    canvas = tk.Canvas(root, width = w, height = h)      
    canvas.pack()   
    tkimage = ImageTk.PhotoImage(master=canvas, image=img)
    canvas.create_image(0,0, anchor=tk.NW, image=tkimage)
    rect = canvas.create_rectangle(posi-2, 0, posi+2, h, fill="black", outline="white")
    bind_events(root, canvas, rect)
    frame = tk.Frame(root, width = w, height = 60)
    frame.pack()
    but = tk.Button(frame, text="Confirm", command=partial(quit, root, "Button press"))
    but.place(x=0, y=0, height=60, width=w)
    root.mainloop()


path = getpath()
checkfile(path)
img = Image.open(path).convert("RGBA")
w, h = img.size
posi = w/2
move, grab = False, False
gui(img)



# canvas.height = canvas.winfo_reqheight()
# canvas.width = canvas.winfo_reqwidth()
# root.bind("<Configure>", partial(resize, canvas, rect))
# 
# # def resize(canvas, rect, event):
#     # wscale = event.width/canvas.width
#     # hscale = event.height/canvas.height
#     canvas.width = event.width
#     canvas.height = event.height - 60
#     canvas.config(width=canvas.width, height=canvas.height)
#     # canvas.scale("all", 0, 0, wscale, hscale)