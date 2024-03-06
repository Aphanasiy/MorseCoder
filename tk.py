import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb
import time
import locale

import player
import settings

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

class GridManager:
    _grid: dict
    def __init__(self):
        self._grid = dict()
    
    def add(self, module, col, row):
        if ((col, row) in self._grid):
            raise Exception(f"Field ({col}, {row}) is already occupied")
        self._grid[(col, row)] = module 

    def render(self):
        for (col, row), module in self._grid.items():
            module.grid(column=col, row=row, ipadx=6, ipady=4, padx=5, pady=5, sticky="NSWE")
    
    def __del__(self):
        del self._grid



class LetterGameFrame:
    _gameFrame: tk.Frame
    _centralLabel: tk.Label
    _toMenuButton: tk.Button
    _mainWindow = None
    _player = player.LetterGame

    def _l10n(self):
        return self._mainWindow._l10n

    def bind(self, event, callback):
        self._mainWindow._window.bind(event, callback)
    
    def unbind(self, event):
        self._mainWindow._window.unbind(event)

    def display(self, message):
        self._centralLabel.config(text=message)

    def press(self, event):
        self._player.press(event.char)

    def bind_keyboard(self):
        for i in range(ord('a'), ord('z') + 1):
            self.bind(chr(i), self.press)
        
    def unbind_keyboard(self):
        for i in range(ord('a'), ord('z') + 1):
            self.unbind(chr(i))


    def background(self, color):
        self._gameFrame.config(background=color)
        self._centralLabel.config(background=color)

    def _onMenuButtonClick(self):
        self._mainWindow._closeLetterGame()
        self._mainWindow._openMenu()

    def __init__(self, placeIn, mainWindow):
        self._mainWindow = mainWindow

        self._gameFrame = tk.Frame(placeIn, background="gray")
        self._gameFrame.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

        self._centralLabel = tk.Label(
                    self._gameFrame, 
                    text=self._l10n().LetterGameWelcome, 
                    font=("Ubuntu Mono", 25),
                    background="gray")
        self._centralLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._toMenuButton = tk.Button(
                    self._gameFrame,
                    text=self._l10n().Menu,
                    font=("Ubuntu Mono", 18),
                    command=self._onMenuButtonClick
        )
        self._toMenuButton.place(
                    anchor=tk.S + tk.E, 
                    relx=0.98, rely=0.99)
        
        self._player = player.TKinterLetterGame(self, rounds=15)

        self.bind("<Return>", self.start)


    def start(self, event):
        self.unbind("<Return>")
        self.bind_keyboard()
        self._player.start_round(force=True)


    def destroy(self):
        # print("Destroy LetterGameFrame")
        self._gameFrame.destroy()


class MenuFrame:
    _menuFrame: tk.Frame
    _menuGridManager: GridManager
    _mainWindow = None

    def _l10n(self):
        return self._mainWindow._l10n
    
    def _onLetterButtonClick(self):
        self._mainWindow._closeMenu()
        self._mainWindow._openLetterGame()

    
    def _onWordButtonClick(self):
        tkmb.showerror("Words", self.l10n().NotImplemented)


    def __init__(self, placeIn, mainWindow):
        self._mainWindow = mainWindow

        self._menuFrame = tk.Frame(width=200, height=200, background="#FFE4B1")
        self._menuFrame.place(in_=placeIn, anchor=tk.CENTER, relx=.5, rely=.5)
        self._menuGridManager = GridManager()
        self._menuGridManager.add(tk.Button(
                    self._menuFrame, 
                    text=self._l10n().Menu1Letters,
                    command=self._onLetterButtonClick
                ), 0, 0)
        self._menuGridManager.add(tk.Button(
                    self._menuFrame, 
                    text=self._l10n().Menu2Words,
                    command=self._onWordButtonClick
                ), 0, 1)
        self._menuGridManager.add(tk.Button(
                    self._menuFrame,
                    text=self._l10n().MenuExit,
                    command=self._mainWindow._window.destroy,
                    background="#FF5C5C"
                ), 0, 2)

        self._menuGridManager.render()

    
    def destroy(self):
        self._menuFrame.destroy()
        del self._menuGridManager
        # print("DESTROY MENU")


class Window:
    _window: tk.Tk
    _mainFrame: tk.Frame
    _l10n: settings.L10N

    def __init__(self, locale="en"):
        self._window = tk.Tk()
        self._window.style = ttk.Style()
        self._window.style.theme_use("alt")
        self._window.minsize(width=500, height=500)
        self._window.title("MorseCoder")
        self._window.geometry("1000x1000")
        self._l10n = settings.L10N(locale)

        self._mainFrame = tk.Frame(borderwidth=5, relief=tk.RIDGE, background="white")
        self._mainFrame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._openMenu()

        self._window.bind("<Escape>", self._destroy)

    def _openMenu(self):
        self._menuFrame = MenuFrame(self._mainFrame, self)
    
    def _closeMenu(self):
        self._menuFrame.destroy()
    
    def _openLetterGame(self):
        self._letterGame = LetterGameFrame(self._mainFrame, self)
    
    def _closeLetterGame(self):
        self._letterGame.destroy()
        self._letterGame = None
        del self._letterGame
    
    def _destroy(self, *args):
        # print(args)
        self._window.destroy()

    def __repr__(self):
        self._window.mainloop()
        return ""
