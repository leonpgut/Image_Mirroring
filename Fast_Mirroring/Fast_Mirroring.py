from PIL import Image, ImageOps
import os

def mirrorleft():
    lefthalf = img.crop([0, 0, width/2, height])
    lefthalfmir = ImageOps.mirror(lefthalf)
    return concatenate(lefthalf, lefthalfmir)

def mirrorright():
    righthalf = img.crop([width/2, 0, width, height])
    righthalfmir = ImageOps.mirror(righthalf)
    return concatenate(righthalfmir, righthalf)

def concatenate(img1, img2):
    result = Image.new('RGB', (img1.width + img2.width, img1.height))
    result.paste(img1, (0, 0))
    result.paste(img2, (img1.width, 0))
    return result


toconvert = os.listdir("to_convert/")
converted = os.listdir("converted/")
for i in toconvert:
    if converted.__contains__(i + "_leftmirrored.png"):
        continue
    img = Image.open("to_convert/" + i).convert("RGBA")
    width, height = img.size
    leftmirrored = mirrorleft()
    rightmirrored = mirrorright()
    leftmirrored.save("converted/" + i + "_leftmirrored.png", format="png")
    rightmirrored.save("converted/" + i + "_rightmirrored.png", format="png")
    print("Finished mirroring for " + i)