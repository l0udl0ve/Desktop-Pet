from PIL import Image, ImageTk
import pyautogui as pt
import tkinter as tk
from bisect import *
import send2trash
import threading
import importlib
import pystray
import windnd
import src
import sys
import os

WIDTH, HEIGHT = pt.size()
taskbarHeight = 40
imgWidth, imgHeight = 200, 200
posX, posY = WIDTH - imgWidth, HEIGHT - imgHeight
centerX, centerY = posX + imgWidth // 2, posY + imgHeight // 2

root = tk.Tk()
root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
root.overrideredirect(True)
root.configure(bg='pink')
root.attributes('-transparentcolor', 'pink')
root.wm_attributes('-topmost', 1)

tan = [
    -5.02733949212585,
    -1.49660576266549,
    -0.6681786379192988,
    -0.19891236737965837,
    0.198912367379658,
    0.6681786379192989,
    1.496605762665489,
    5.027339492125846
]


def load_images(folder_path):
    image_list = []
    for x in os.listdir(folder_path):
        y = tk.PhotoImage(file=folder_path + '/' + x)
        image_list.append(y)
    return image_list


class Pet:
    def __init__(self, player):
        self.shellPath = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.eyes = load_images(self.shellPath + '\\src\\eyes')
        self.tails = load_images(self.shellPath + '\\src\\tails')
        self.eat = load_images(self.shellPath + '\\src\\eat')
        self.click = load_images(self.shellPath + '\\src\\click')

        self.len_eyes = len(self.eyes)
        self.len_tails = len(self.tails)
        self.player = player
        self.eyes_times = 0
        self.memu = None
        self.topWindow = None
        self._systray()
        self.isOpen = False
        self.iconDir = {}

    def _eyes_play(self, element) -> None:
        x, y = pt.position()
        if posX < x < posX + imgWidth and posY < y < posY + imgHeight:
            img_num = 0
        else:
            if x == posX:
                img_num = 5
            else:
                tan_theta = -(y - posY) / (x - posX)
                if tan_theta >= tan[7] or tan_theta < tan[0]:
                    img_num = 5
                else:
                    img_num = (bisect_left(tan, tan_theta) + 4) % 8 + 1

            if img_num == 1:
                if x < posX:
                    img_num += 8
            else:
                if y < posY:
                    img_num += 8
        img = self.eyes[img_num]
        element.config(image=img)
        self.eyes_times += 1
        root.after(50, lambda: self._eyes_play(element))

    def _tails_play(self, element, index: int = 0) -> None:
        if index == self.len_tails:
            index = 0
        img = self.tails[index]
        element.config(image=img)
        if index == 0:
            root.after(1000, lambda: self._tails_play(element, index + 1))
        else:
            root.after(200, lambda: self._tails_play(element, index + 1))

    def _play_once(self, window, images, index: int = 0):
        if index == len(images):
            window.destroy()
            return
        img = images[index]
        window.config(image=img)
        root.after(100, lambda: self._play_once(window, images, index + 1))

    def _memu_destroy(self) -> None:
        self.memu.destroy()
        self.memu = None
        self.isOpen = False

    def _onclick(self, event) -> None:
        if self.isOpen:
            self._memu_destroy()
            self.isOpen = False
        else:
            self.topWindow = tk.Label(self.player, bg='pink', bd=0)
            self.topWindow.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._play_once(self.topWindow, self.click)
            if self.memu:
                return
            width, height = 50, 200
            self.memu = tk.Toplevel(self.player)
            self.memu.overrideredirect(True)
            self.memu.configure(bg='pink')
            self.memu.geometry(f"{width}x{height}+{posX - width}+{posY}")
            self.memu.attributes('-transparentcolor', 'pink')
            self.memu.wm_attributes('-topmost', 1)

            self.scrollbar = tk.Scrollbar(self.memu, borderwidth=0)
            self.scrollbar.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.75)
            self.canvas = tk.Canvas(self.memu, yscrollcommand=self.scrollbar.set, borderwidth=0)
            self.canvas.place(relx=0, rely=0, relwidth=0.8, relheight=0.75)

            self.frame = tk.Frame(self.canvas, bg='pink')
            self.frame.pack(fill="x")
            self.canvas.create_window((0, 0), window=self.frame, width=40)
            self._make_menu(self.frame)
            self.frame.update()
            self.canvas.configure(yscrollcommand=self.scrollbar.set, scrollregion=self.canvas.bbox("all"))
            self.scrollbar.config(command=self.canvas.yview)

            self.close_img = tk.PhotoImage(self.shellPath + '\\src\\misc\\close.png')
            close = tk.Button(self.memu, image=self.close_img, bg='pink', relief='flat', cursor='hand2',
                              command=self._hide_window)
            close.place(relx=0, rely=0.775, relwidth=0.9, relheight=0.225)

            self.isOpen = True

    def _make_menu(self, window) -> None:
        for path in os.listdir(self.shellPath + '\\plugin'):
            spec = importlib.util.spec_from_file_location("plugin", self.shellPath + f"\\plugin\\{path}\\main.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugin_class = getattr(module, "Plugin")

            plugin = plugin_class()
            if os.path.exists(self.shellPath + f"\\plugin\\{path}\\icon.png"):
                image = Image.open(self.shellPath + f"\\plugin\\{path}\\icon.png")
                self.iconDir[path] = ImageTk.PhotoImage(image)
                tk.Button(window, image=self.iconDir[path], relief='flat', overrelief='raised', cursor='hand2',
                          command=plugin.run).pack(fill="x")
            else:
                tk.Button(window, text=path[0].upper(), relief='flat', overrelief='raised', cursor='hand2',
                          command=plugin.run).pack(fill="x")

    def _ondrop(self, paths_raw) -> None:
        self.topWindow = tk.Label(self.player, bg='pink', bd=0)
        self.topWindow.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._play_once(self.topWindow, self.eat)
        threading.Thread(target=self._move2trash, args=(paths_raw,)).start()

    def _move2trash(self, paths_raw) -> None:
        paths = [x.decode('gbk') for x in paths_raw]
        for path in paths:
            send2trash.send2trash(path)
        sys.exit()

    def _getPoint(self, event):
        self.x, self.y = event.x, event.y

    def _move(self, event):
        global posX, posY
        new_x = (event.x - self.x) + self.player.winfo_x()
        new_y = (event.y - self.y) + self.player.winfo_y()
        s = f"{imgWidth}x{imgHeight}+{new_x}+{new_y}"
        posX = new_x
        posY = new_y

        if self.memu:
            self.memu.geometry(f"{50}x{200}+{posX - 50}+{posY}")
        self.player.geometry(s)

    def _systray(self):
        self.systray_menu = (
            pystray.MenuItem('显示', self._show_window, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('退出', self._quit)
        )
        image = Image.open(self.shellPath + '\\src\\misc\\icon.png')
        self.icon = pystray.Icon("icon", image, "桌宠", self.systray_menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def _hide_window(self):
        if self.memu:
            self._memu_destroy()
        self.player.withdraw()

    def _show_window(self):
        self.icon.visible = True
        self.player.deiconify()

    def _quit(self, icon):
        icon.stop()
        self.player.quit()
        self.player.destroy()

    def play(self):
        eye = tk.Label(self.player, bg='pink', bd=0)
        eye.place(relx=0.145, rely=0.105, relwidth=0.71, relheight=0.5)
        tail = tk.Label(self.player, bg='pink', bd=0)
        tail.place(relx=0.145, rely=0.605, relwidth=0.71, relheight=0.29)
        self._tails_play(tail)
        self._eyes_play(eye)
        self.player.bind("<Button-1>", self._getPoint)
        self.player.bind("<B1-Motion>", self._move)
        self.player.bind("<Double-Button-1>", self._onclick)
        windnd.hook_dropfiles(self.player, func=self._ondrop)


body = Pet(root)
body.play()
root.mainloop()
