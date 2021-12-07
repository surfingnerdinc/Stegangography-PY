from typing import Iterable
import numpy as np
from PIL import Image


### Preparing message to encoding
def strToBit(message) -> Iterable[int]:
    for char in message:
        ascii_value = ord(char)
        for bit_position in range(8):
            power = 7 - bit_position
            yield 1 if ascii_value & (1 << power) else 0


def clearBits(pixels) -> None:
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            pixels[row, col, 0] &= ~1


def bitsArr(px) -> Iterable[str]:
    ascii_value = 0
    for i, pixel_red_value in enumerate(px):
        ascii_value_bit_position = 7 - i % 8
        if pixel_red_value & 1:
            ascii_value |= 1 << ascii_value_bit_position
        if ascii_value_bit_position == 0:
            char: str = chr(ascii_value)
            if not char.isprintable() and char != '\n':
                return
            yield char
            ascii_value = 0


### Decoding and encoding message 
def encodeMessage(message: str, image, result: str) -> None:
    img = Image.open(image)
    pixels = np.array(img)
    img.close()
    clearBits(pixels)
    for i, bit in enumerate(strToBit(message)):
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        pixels[row, col, 0] |= bit
    out_img = Image.fromarray(pixels)
    out_img.save(result)
    out_img.close()



def decodeMessage(filename: str) -> str:
    img = Image.open(filename)
    arr = ''.join(bitsArr(img.getdata(band=2)))
    print(arr)
    result = ''.join(bitsArr(img.getdata(band=0)))
    img.close()
    print('Decoded message from image : ', result)
    return result


def main():
    print("Select what you want to do: ")
    print('1 - Encode and decode image')
    print("2 - Just decode different image")
    
    text = input()

    if (text == '1'):
        message = '''noooo co ty nie powiesz'''
        encodeMessage(message, 'me.png', 'encoded-me.png')
        print('Message encoded')
        decodeMessage('encoded-me.png')
        
    if (text == '2'):
        print('Type file name if image exists in main folder or full path')
        path = input()
        pathdef = 'encoded-me.png'        
        decodeMessage(pathdef)
        
        
if __name__ == '__main__':
    main()

    
    