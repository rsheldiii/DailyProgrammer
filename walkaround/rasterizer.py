import Image,sys,struct,time,os

BLACK,WHITE = 0,1
def rasterToImg(name,width,height,directions):
    name,ext = os.path.splitext(name)
    arr = [WHITE for j in range(0,width*height)]
    x,y = 0,0
    size = width,height
        
    dic = {"N":(0,-1), "S" : (0,1) , "E" : (1,0), "W" : (-1,0)}
       
    for char in directions:#brunt of the work
        ans = dic.get(char)
        if not ans:
            arr[x+y*width] = BLACK
        else:
            x += ans[0]
            y += ans[1]
            
    #image processing portion        
            
    data = struct.pack('B'*len(arr), *[pixel*255 for pixel in arr])#packs all values into binary string
    img = Image.fromstring('P', size, data)
    filename = name +" "+time.strftime("%a %b %y %X")+".png"
    img.save(filename) 
    
    return filename
       
#true means the array will be stamped with a BLACK pixel. 
def modeL(pixel):
    if pixel < 128:
        return True
    return False
    
def modeRGBA(pixel):#converting to L just destroys transparency
    #calculations on a white matte background, normalizing into RGB
    r,g,b,a = pixel
    aa = a/255.0
    opa = 1-(a/255.0)
    
    r = aa * r + opa * 255
    g = aa * g + opa * 255
    b = aa * b + opa * 255
    total = sum((r,g,b))
    if total < (765 / 2):
        return True
    return False
   
def nullify(pixel):
    return False 
        
def imgToRaster(img):
    modeDict = {"L" : modeL, "RGBA" : modeRGBA}
    incompatible = ["RGBA"]
    directions = ""
    im = Image.open(img)
    width,height = im.size
    if im.mode not in incompatible:
        im = im.convert('L')
    mode = im.mode
    pixels = im.load()
    print(img,mode)

    for y in range(0,height):
        for x in range(0,width):
            if modeDict.get(mode,nullify)(pixels[(x,y)]):#pass the pixel to the correctly moded b/w parser
                directions += "P"
            directions += "E"
        directions = directions[:-1]#last E isnt needed
        directions += "S"+"W"*(width-1)#rewind like a typewriter
    return img,width,height,directions
                
if len(sys.argv) > 1:
    for img in sys.argv[1:]:
        rasterToImg(*imgToRaster(img))
else:
    rasterToImg(*imgToRaster("RGB.png"))
