import screeninfo
import keyboard
import ctypes
import sys
import os

# Setting the command to clear the page based on the type of platform
clear_screen = 'clear'

if sys.platform == 'win32':
    clear_screen = 'cls'



class ScreenSplitter:

    def __init__(self, text):
        self.text = text
    
    def get_string_width_size(self):
        """Find the largest string width"""

        width = ''
        split = [part for part in self.text.split('\n')]

        for section in split:
            if len(section) > len(width):
                width = section
        
        return width
    
    def get_monitor_width_size(self):
        """Find monitor width"""
        return screeninfo.get_monitors()[0].width - 440 # The number 440 is by default to reduce the number of pixels related to the scroll bar in cmd
    
    def get_text_pixel(self, text, font_size = 16, font=''):
        """Calculate the number of pixels that a string needs to be displayed"""

        class SIZE(ctypes.Structure):
            _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

        hdc = ctypes.windll.user32.GetDC(0)
        hfont = ctypes.windll.gdi32.CreateFontA(font_size, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
        hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

        size = SIZE(0, 0)
        ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

        ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
        ctypes.windll.gdi32.DeleteObject(hfont)

        return size.cx
    
    def string_maker(self, lst_of_str):
        """Creating a string based on a list of strings"""

        result = ""

        for item in lst_of_str:
            result += ''.join(item) + '\n'
        
        return result
    
    def show(self, data, start=0):
        """Displaying the result with the ability to move between pages with the right and left keys"""

        lenght = len(data) - 1

        while True:

            os.system(clear_screen)
            print(data[start])

            try:

                press = keyboard.read_hotkey(suppress=False)

            except KeyboardInterrupt:
                return
                
            if press == 'right':
                start += 1

            if press == 'left':
                start -= 1
                
            if start > lenght:
                start = 0
                
            if start < 0:
                start = lenght

            if press == 'q':
                return
            
    def screen_splitter(self):
        """Converting a large string of screens into several smaller screens and displaying them"""

        width_monitor_pixel = ScreenSplitter.get_monitor_width_size(self)
        width_text = ScreenSplitter.get_string_width_size(self)
        width_text_pixel = ScreenSplitter.get_text_pixel(self, width_text)

        if width_text_pixel <= width_monitor_pixel:
            print(self.text)
            return
        
        number_of_page = (width_text_pixel // width_monitor_pixel) 

        k = len(width_text) // number_of_page
        start = 0
        end = k


        parts = []

        for page_num in range(number_of_page):
            temp = []
            for item in self.text.split('\n'):
                if page_num == number_of_page - 1:
                    temp.append(item[start:])
                else:
                    temp.append(item[start:end])
            
            start = end
            end = k
            end *= (page_num + 2)
            parts.append(ScreenSplitter.string_maker(self, temp))       

        ScreenSplitter.show(self, parts)


class LoadFromFile(ScreenSplitter):

    def __init__(self):
        pass
    
    def get_path(self):
        """Get file path [.txt]"""

        while True:
            path = input('Enter your path:').strip()    
            if os.path.exists(path):
                self.path = path
                return
            print('Please enter a right path')
    
    def read(self):
        """Read and show file"""
        with open(self.path, 'r') as file:
            self.text = file.read()
        
        super().screen_splitter()
    



if __name__ == '__main__':

    splitter = ScreenSplitter('this is a test')
    splitter.screen_splitter()