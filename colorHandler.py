import colorsys
def toHex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b);
def toRGB(h,s,v):
    color = colorsys.hsv_to_rgb(h/255.0, s/255.0, v/255.0)
    return [int(a * 255) for a in color]
