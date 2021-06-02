'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import sys
import traceback

from time import *
from tkinter import *

from .base import *

class Cell:
    pageCaption, groupCaption, circuit, filler = range (4)

    def __init__ (self, moduleWindow, module, element):
        self.moduleWindow = moduleWindow
        self.module = module
        self.element = element

        if self.element._isA ('_PageCaption'):
            self.kind = Cell.pageCaption
            self.label =  Label (self.moduleWindow, text = self.element (), justify = CENTER, width = Gui.windowWidth)
            self.label.grid (row = 0, column = 0, columnspan = 2 * self.module._maxNrOfColumns)
            self.label.configure (foreground = pageCaptionForegroundColorHex, background = pageCaptionBackgroundColorHex)
            self.label.bind ('<ButtonPress-1>', lambda event: self.moduleWindow.goPage (self.moduleWindows.pageIndex - 1))
            self.label.bind ('<ButtonPress-2>', lambda event: self.moduleWindow.goPage (self.moduleWindows.pageIndex + 1))
        
        elif self.element._isA ('_GroupCaption'):
            self.kind = Cell.groupCaption
            self.label = Label (self.moduleWindow, text = self.element (), justify = CENTER, width = Gui.labelWidth + Gui.entryWidth)
            self.label.grid (row = self.element._rowIndex + 1, column = 2 * self.element._columnIndex, columnspan = 2)
            self.label.configure (foreground = groupCaptionForegroundColorHex, background = groupCaptionBackgroundColorHex)
        
        elif self.element._isA ('_Circuit'):        
            self.kind = Cell.circuit
            self.label =  Label (self.moduleWindow, text = self.element._name, anchor = 'e', justify = RIGHT, width = Gui.labelWidth)
            
            self.entry = Entry (self.moduleWindow, font = Gui.entryFont, width = Gui.entryWidth)

            self.entry.bind ('<ButtonPress-1>', self.force)
            self.entry.bind ('<ButtonRelease-1>', self.select)  # Selecting (highlighting) text at ButtonPress-1 has no effect, since it's too early
            self.entry.bind ('<Return>', self.forceAndSelect)   # Select so it will be ready to be overwritten
            
            self.entry.bind ('<Key>', self.edit)
            
            self.entry.bind ('<ButtonRelease-3>', self.release)
            self.entry.bind ('<Escape>', self.release)
            
            self.entry.bind ('<ButtonPress-2>', self.set1)
            self.entry.bind ('<ButtonRelease-2>', self.set0)
            
            if sys.platform in {'win32', 'darwin'}:
                self.entry.bind ('<MouseWheel>', lambda event: self.adapt (1 if event.delta > 0 else -1))       # Windows, OsX
            elif sys.platform in {'linux'}:
                self.entry.bind ('<Button-4>', self.adapt (1))                                                  # Linux
                self.entry.bind( '<Button-5>', self.adapt (-1))                                                 # Linux
            else:
                print ('Error: Unknown platform')
                sys.exit (1)
            
            self.label.grid (row = self.element._rowIndex + 1, column = 2 * self.element._columnIndex, ipadx= 0.5, sticky = 'NEW')
            self.entry.grid (row = self.element._rowIndex + 1, column = 2 * self.element._columnIndex + 1, sticky = 'NEW')
            
            self.entry.configure (foreground = entryReleasedForegroundColorHex, background = entryReleasedBackgroundColorHex)
            self.label.configure (foreground = hexFromRgb (self.element.color) if self.element.color else labelForegroundColorHex, background = labelBackgroundColorHex)
            
        elif self.element._isA ('_Filler'):
            self.kind = Cell.filler
            self.label0 = Label (self.moduleWindow, text = '', width = Gui.labelWidth)
            self.label1 = Label (self.moduleWindow, text = '', width = Gui.entryWidth)
            self.label0.grid (row = self.element._rowIndex + 1, column = 2 * self.element._columnIndex, sticky = 'NEW')
            self.label1.grid (row = self.element._rowIndex + 1, column = 2 * self.element._columnIndex + 1, sticky = 'NEW')
            self.label0.configure (foreground = panelBackgroundColorHex, background = panelBackgroundColorHex)
            self.label1.configure (foreground = panelBackgroundColorHex, background = panelBackgroundColorHex)
        
    def force (self, event):
        self.entry.configure (foreground = entryForcedForegroundColorHex, background = entryForcedBackgroundColorHex)
        if self.element._forced:
            self.element._write (eval (self.entry.get ()))
        else:
            self.element._force ()
            
    def select (self, event):
        if self.element._forced:
            self.entry.selection_range (0, END)
            
    def forceAndSelect (self, event):
        self.force (event)
        self.select (event)
        
    def edit (self, event):
        if self.element._forced and event.char.isalnum ():
            self.entry.configure (foreground = entryEditForegroundColorHex, background = entryEditBackgroundColorHex)
        
    def release (self, event):
        self.element._write (eval (self.entry.get ()))
        self.element._release ()
        self.entry.configure (foreground = entryReleasedForegroundColorHex, background = entryReleasedBackgroundColorHex)
    
    def set1 (self, event):
        if self.element._isA ('Marker', 'Runner', 'Oneshot', 'Latch'):
            self.element._write (1)

    def set0 (self, event):
        if self.element._isA ('Marker', 'Runner', 'Oneshot', 'Latch'):
            self.element._write (0)
    
    def adapt (self, delta):
        if self.element._isA ('Register', 'Timer'):
            try:
                self.element._write (round (eval (self.entry.get ())) + delta)
            except:     # Why is this needed under Linux?
                pass
                # print (traceback.format_exc ())

class _Filler:
    def __init__ (self, columnIndex):
        self._columnIndex = columnIndex
        self._rowIndex = 2
        
    def _isA (self, *ClassNames):
        return '_Filler' in ClassNames
        
class ModuleWindow (Toplevel):
    def __init__ (self, module):
        Toplevel.__init__ (self)
        self.module = module
        self.title (getTitle (self.module._name))
        
        self.pageIndex = 0
        self.bind ('<Prior>', lambda event: self.goPage (self.pageIndex - 1))
        self.bind ('<Next>', lambda event: self.goPage (self.pageIndex + 1))
        
        self.configure (background = panelBackgroundColorHex)

        for columnIndex in range (2 * self.module._maxNrOfColumns):
            self.columnconfigure (columnIndex, weight = 1)
        
        if self.module._defaultFormat:
            self.geometry("%dx%d%+d%+d" % (Gui.windowWidth / 4, 800, 0, 0))
        else:
            self.geometry("%dx%d%+d%+d" % (Gui.windowWidth, self.module._maxNrOfRows * Gui.rowHeight, 0, 0))
            
        self.pageIndex = None
        self.goPage (0)

    def goPage (self, pageIndex):
        for child in self.winfo_children ():
            child.destroy ()
    
        self.pageIndex = min (max (pageIndex, 0), len (self.module._pages) - 1)
        
        self.cells = []
        firstEmptyColumnIndex = 0
        for element in self.module._pages [self.pageIndex] ._elements:
            self.cells.append (Cell (self, self.module, element))
            firstEmptyColumnIndex = 2 * element._columnIndex + 1
            
        for fillerColumnIndex in range (firstEmptyColumnIndex, self.module._maxNrOfColumns):
            self.cells.append (Cell (self, self.module, _Filler (fillerColumnIndex)))
            
    def readFromEngine (self):
        for cell in self.cells:
            if cell.kind == Cell.circuit and not cell.element._forced and cell.entry.get () != cell.element ():
                cell.entry.delete (0, END)
                cell.entry.insert (0, cell.element ())
                
class Gui:
    entryFont = ('Quartz MS', 10)
    
    windowWidth = 800
    labelWidth = 20
    entryWidth = 10
    
    rowHeight = 23

    def __init__ (self, world):
        self.world = world      
        self.root = Tk ()
        self.root.withdraw ()
        self.moduleWindows = [ModuleWindow (module) for module in self.world._modules]
        
        while True:
            for moduleWindow in self.moduleWindows:
                moduleWindow.readFromEngine ()
                
            self.root.update ()
            
            for  moduleWindow in self.moduleWindows:
                moduleWindow.update ()
                
            sleep (0.1)
            
