# -*- coding: utf-8 -*-
import Image
import colorsys
import types



def calculateColor(filepath):
    # 色彩范围无交叉
    colors = { '红':(342,18, 9), '橙':(18,54, 10), 
               '黄':(54,90, 11),  '黄绿':(90,126, 12), 
               '绿':(126,162, 13), '青绿':(162,198, 14),
               '蓝':(198,234, 15), '蓝紫':(234,270, 16),
               '紫':(270,306, 17), '紫红':(306,342, 18)
            }
    weight = { '红':0, '橙':0, 
               '黄':0,  '黄绿':0, 
               '绿':0, '青绿':0,
               '蓝':0, '蓝紫':0,
               '紫':0, '紫红':0
            }
    
    print '^^^计算中...^^^', filepath
    img = Image.open(filepath)
    if img.size[0] > 200:
        img.thumbnail((200, 200))
    print '^img.size', img.size
    pix = img.load()
    blackWhiteCount = 0
    for i in range(0, img.size[0] ):
        # 每一点的像素
        for j in range(0, img.size[1]):
#            print pix[i,j]
            if type(pix[i,j]) is not types.TupleType:
                continue
                
            rv = pix[i,j][0]
            gv = pix[i,j][1]
            bv = pix[i,j][2]
            hsvs = colorsys.rgb_to_hsv(rv/255.0, gv/255.0, bv/255.0)
            hv = hsvs[0]*360
            sv = hsvs[1]
            vv = hsvs[2]
#            print 'rgb', pix[i,j]
#            print 'hsv', hv,sv,vv
            if sv == 0:
                blackWhiteCount = blackWhiteCount + 1
            # 判断hv的范围
            for name,value in colors.items():
                # 亮度大于0.5, 饱和度大于0.5,,  且色彩在范围内
                if sv>0.4 and vv>0.4 :
                    if value[0] > value[1]:
                        if hv >= value[0] or hv <= value[1]:
                            weight[name]= weight[name] + 1
                    else:
                        if hv>=value[0] and hv<=value[1]:
                            weight[name] = weight[name] + 1
    # 最后打印权重
    if blackWhiteCount > img.size[0]*img.size[1] * 0.8:
#        print blackWhiteCount, img.size[0]*img.size[1]
        return 15
    max_score = 0
    max_score_id = ''
    print '----'
    for name,value in weight.items():
        if value > 5 and value > max_score:
            max_score = value
            max_score_id = colors[name][2]
        print name,value
    print '----'
    if max_score != 0:
        return max_score_id
    else:
        return None

#     ^^^计算中...
#^img.size (114, 114)
#----
#Blue 446
#Yellow 1415
#Green 0
#Cyan 74
#Magenta 0
#Red 1419       
def get_dominant_color(image):
    """
    Find a PIL image's dominant color, returning an (r, g, b) tuple.
    """

    image = image.convert('RGBA')
    
    # Shrink the image, so we don't spend too long analysing color
    # frequencies. We're not interpolating so should be quick.
    image.thumbnail((200, 200))
    
    max_score = None
    dominant_color = None
    
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # Skip 100% transparent pixels
        if a == 0:
            continue
        
        # Get color saturation, 0-1
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[0]
        print saturation
        # Calculate luminance - integer YUV conversion from
        # http://en.wikipedia.org/wiki/YUV
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        
        # Rescale luminance from 16-235 to 0-1
        y = (y - 16.0) / (235 - 16)
        
        # Ignore the brightest colors
        if y > 0.9:
            continue
        # (201, 201, 203)
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    
    return dominant_color

#if __name__ == '__main__':
#     print calculateColor( '114.png' )
    
    
    
    
