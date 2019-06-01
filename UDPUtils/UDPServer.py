import socket
import threading
import time
import zlib
import PIL
# 解压
def decompress(b):
    return zlib.decompress(b)

# 字节转图像
def bytesToImg(height, width, b, type="RGBA"):
    img = PIL.Image.frombytes("RGBA", (height, width), b)
    return img