from PIL import Image

no_of_divisions = 2



def crop(filename, number):
    im = Image.open(filename)
    w, h = im.size
    unit = w // no_of_divisions
    for n in range(number):
        im1 = im.crop((unit * n, 0, unit * (n + 1), h))
        im1.save(filename[:-4] + "-" +str(n + 1) + ".png")