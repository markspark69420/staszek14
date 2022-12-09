import os
from PIL import Image

def load(folder):
    imgs = []
    read = {}
    for i in os.listdir(folder):
        if i.endswith(".txt"):
            pass
        else:
            imgs.append(Image.open(folder+'/'+i))
    return read, imgs
def run():
    check = 3
    l
    for i in 
if __name__ == "__main__":
    print(load("./res/pipes-code-train")[1])
