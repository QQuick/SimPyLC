# ====== Legal notices
#
# Copyright (C) 2013 - 2018 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicense for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your license.
#

from datetime import *
from time import *
from threading import *
from traceback import *
import math
import builtins

from .base import *
from .gui import *
from .graphics import *
from .scene import *
from .chart import *
from .coder import *
            
class _Functor:
    def __init__  (self, state):
        self._state = evaluate (state)
        
    def __call__ (self):
        return self._state
        
    def __lt__ (self, other):
        return self () < evaluate (other)
    
    def __le__ (self, other):
        return self () <= evaluate (other)
    
    def __gt__ (self, other):
        return self () > evaluate (other)
    
    def __ge__ (self, other):
        return self () >= evaluate (other)
    
    def __eq__ (self, other):
        return self () == evaluate (other)
    
    def __ne__ (self, other):
        return self () != evaluate (other)
        
    def __neg__ (self):
        return -self ()
        
    def __add__ (self, other):
        return self () + evaluate (other)
    
    def __radd__ (self, other):
        return evaluate (other) + self ()
    
    def __sub__ (self, other):
        return self () - evaluate (other)
    
    def __rsub__ (self, other):
        return evaluate (other) - self ()
    
    def __mul__ (self, other):
        return self () * evaluate (other)
    
    def __rmul__ (self, other):
        return evaluate (other) * self ()
    
    def __truediv__ (self, other):
        return self () / evaluate (other)
        
    def __rtruediv__ (self, other):
        return float (evaluate (other)) / self ()
        
    def __mod__ (self, other):
        return self () % evaluate (other)
        
    def __rmod__ (self, other):
        return evaluate (other) % self ()
        
    def __bool__ (self):
        return not not self ()
        
class _Element:
    def __init__ (self):
        self.color = None
        if not Module._current is None:
            self._setPosition ()
            Module._current._pages [self._pageIndex] ._elements.append (self)

    def _setPosition (self):
        self._pageIndex, self._rowIndex, self._columnIndex = Module._pageIndex, Module._rowIndex, Module._columnIndex 
        Module._current._maxNrOfRows = max (Module._current._maxNrOfRows, self._rowIndex + 2)  # Leave room for page caption
        Module._current._maxNrOfColumns = max (Module._current._maxNrOfColumns, self._columnIndex + 1)
            
    def _isA (self, *classNames):
        for className in classNames:
            if isinstance (self, eval (className)):
                return True
        return False
        
class _Caption (_Element):
    def __init__ (self, text):
        self._text = text
        _Element.__init__ (self)
        
class _GroupCaption (_Caption):
    def __init__ (self, text, top = False):
        self._top = top
        _Caption.__init__ (self, text)

    def _setPosition (self):
        if self._top:
            Module._columnIndex += 1
            Module._rowIndex = 0
        elif self._text:
            Module._rowIndex += 1
        _Caption._setPosition (self)
        
    def __call__ (self):
        return '{0}'.format (self._text) if self._text and self._text [0] != ' ' else ''
        
class _PageCaption (_Caption):
    def __init__ (self, text):
        _Caption.__init__ (self, text)
        
    def _setPosition (self):
        Module._pageIndex += 1
        Module._current._pages.append (_Page ())
        Module._columnIndex = -1
        Module._rowIndex = -1
        _Caption._setPosition (self)
        
    def __call__ (self):
        return 'Page {0}: {1}'.format (self._pageIndex + 1, self._text)
        
class _Circuit (_Element, _Functor):
    def __init__ (self, state):
        _Element.__init__ (self)
        _Functor .__init__ (self, state)
        self._forced = False
        
    def _write (self, value):
        self._state = value
        
    def _force (self):
        self._forced = True
        
    def _release (self):
        self._forced = False
        
    def _setPosition (self):
        if Module._pageIndex == -1:  # No _Captions, so just one long list of _Circuits
            Module._current._defaultFormat = True
            Module._pageIndex = 0
            Module._current._pages.append (_Page ())
            Module._columnIndex = 0
            Module._rowIndex = -1  # Use position of missing _PageCaption for first _Circuit
            
        Module._rowIndex += 1
        _Element._setPosition (self)
    
class _Follower (_Circuit):
    def __init__ (self, value):
        _Circuit.__init__ (self, value)
        
    def _follow (self, trueValue, condition = True, falseValue = None):
        if self._forced:
            return
        if evaluate (condition):
            self._state = evaluate (trueValue)
        else:
            if not falseValue is None:
                self._state = evaluate (falseValue)     
                
class Marker (_Follower):
    def __init__ (self, value = False):
        _Follower.__init__ (self, value)
        
    def mark (self, trueValue = True, condition = True, falseValue = None):
        _Follower._follow (self, trueValue, condition, falseValue)
        
class Runner (Marker):
    def __init__ (self, value = True):
        Marker.__init__ (self, value)
        World.runner = self
        
class Oneshot (_Circuit):
    def __init__ (self, value = False):
        _Circuit.__init__ (self, value)
        self._oldCondition = False
                
    def trigger (self, condition = True):
        if self._forced:
            return
            
        self._state =  evaluate (condition) and not self._oldCondition
        self._oldCondition = evaluate (condition)

class Latch (_Circuit):
    def __init__ (self, value = False):
        _Circuit.__init__ (self, value)

    def latch (self, condition = True):
        if self._forced:
            return
        if evaluate (condition):
            self._state = True

    def unlatch (self, condition = True):
        if self._forced:
            return
        if evaluate (condition):
            self._state = False
                    
class Register (_Follower):
    def __init__ (self, value = 0):
        _Follower.__init__ (self, value)

    def set (self, trueValue = 1, condition = True, falseValue = None):
            _Follower._follow (self, trueValue, condition, falseValue)

class Timer (_Circuit):
    def __init__ (self):
        _Circuit.__init__ (self, self._stateFromValue (0.))
        self._value = 0.  # Seconds as float
            
    def _stateFromValue (self, value):  # State is time when timer semantic value was 0
        return World.time () - value
    
    def _valueFromState (self, state):  # Value is timer semantic value for a certain state (stored time)
        return World.time () - state

    def reset (self, condition = True):
        if self._forced:
            return
        if evaluate (condition):
            self._state = self._stateFromValue (0)
        
    def _force (self):
        self._forced = True
        self._value = self._valueFromState (self._state)
        
    def _release (self):
        self._forced = False
        self._state = self._stateFromValue (self._value)
        
    def __call__ (self):
        return self._value if self._forced else self._valueFromState (self._state)
            
    def _write (self, value):
        if self._forced:
            self._value = value
        else:
            self._state = self._stateFromValue (value)
    
class _Page:
    def __init__ (self):
        self._elements = []
    
class Module:
    _current = None  # Place elements outside any module
    _id = -1
    
    def _getId (self):
        Module._id += 1
        return str (Module._id) 

    def __init__ (self, name = None):
        Module._current = self  # Place elements in this module
        self._name = name if name else decapitalize (self.__class__.__name__)
        Module._pageIndex = -1
        self._pages = []
        self._maxNrOfRows = 0
        self._maxNrOfColumns = 0
        self._defaultFormat = False
        
    def input (self):
        pass
        
    def sweep (self):
        pass
        
    def output (self):
        pass
        
    def group (self, text = '', top = False):
        setattr (self, Module._getId (self), _GroupCaption (' ', top))  # Note the blank, so it won't be compressed
        setattr (self, Module._getId (self), _GroupCaption (text))
            
    def page (self, text = ''):
        setattr (self, Module._getId (self), _PageCaption (text))

    def part (self, text = ''):
        pass
                        
    def _setPublicElementNames (self):
        for var in vars (self):
            if not var.startswith ('_'):
                getattr (self, var) ._name = var
                                
import inspect
    
class World (Thread):
    time = Register (0)  # Early because needed in Timer constructors
    startDateTime = datetime.now ()
    runner = True   # May be replaced by a Runner
    
    def __init__ (self, *parameters):
        Thread.__init__ (self)
        
        Module._current = None  # Place further elements outside any module
        World._modules = []
        World._scenes = []
        World._charts = []
        
        for parameter in parameters:
            if isinstance (parameter, Module):
                World._modules.append (parameter)
            elif isinstance (parameter, Scene):
                World._scenes.append (parameter)
            elif isinstance (parameter, Chart):
                World._charts.append (parameter)
                
        if generateCode (self):
            exit (0)
                
        World.period = Timer ()
        World.period._name = 'period'
        World._instance = self
        
        for module in World._modules:
            setattr (World, module._name, module)
            module._setPublicElementNames ()
            
        for scene in World._scenes:
            scene._registerWithCamera ()
            scene._registerWithThings ()
            
        for chart in World._charts:
            chart.define ()
                
        World.first = Marker (True)
        World.sleep = Register (0.02)
        World.refresh = Register (0.013)
        World.period.reset (True)
        
        World.elapsed = Register (0)
        World.offset = Register (0)
                        
        self.daemon = True
        self.start ()

        Graphics (World)
        Gui (World) # Main thread, so this thread, so last
    
    def run (self): # Module constructors called here, placing elements inside modules
        self._cycle ()      
        
    def _cycle (self):
        while True:
            World.elapsed.set ((datetime.now () - World.startDateTime) .total_seconds ())
                        
            if World.runner:
                World.time.set (World.elapsed () - World.offset ())
                
                for module in World._modules:
                    module.input ()
                    module.sweep ()
                    module.output ()
                    
                for scene in World._scenes:
                    scene.update ()
                 
                for chart in World._charts:
                    chart.update ()
                 
                World.first.mark (False)
            else:
                World.offset.set (World.elapsed () - World.time ())

            World.period.reset (True)
            sleep (World.sleep ())
            
world = World   # Pretend this class is a singleton object  
                 
pi = math.pi
radiansPerDegree = math.pi / 180
degreesPerRadian = 180 / math.pi
     
def abs (anObject):
    return builtins.abs (evaluate (anObject))
    
def max (object0, object1):
    return builtins.max (evaluate (object0), evaluate (object1))

def min (object0, object1):
    return builtins.min (evaluate (object0), evaluate (object1))

def pow (object0, object1):
    return math.pow (evaluate (object0), evaluate (object1))

def sqrt (anObject):
    return math.sqrt (evaluate (anObject))

def exp (anObject):
    return math.exp (evaluate (anObject))
    
def log (anObject):
    return math.log (evaluate (anObject))
    
def log10 (anObject):
    return math.log10 (evaluate (anObject))
    
def sin (anObject):
    return math.sin (evaluate (anObject) * radiansPerDegree)
    
def cos (anObject):
    return math.cos (evaluate (anObject) * radiansPerDegree)
    
def tan (anObject):
    return math.tan (evaluate (anObject) * radiansPerDegree)
    
def asin (anObject):
    return math.asin (evaluate (anObject)) * degreesPerRadian

def acos (anObject):
    return math.acos (evaluate (anObject)) * degreesPerRadian

def atan2 (object0, object1):
    return math.atan2 (evaluate (object0), evaluate (object1)) * degreesPerRadian
    
def limit (anObject, limit0, limit1 = None):
    if limit1 is None:
        limit1 = limit0
        limit0 = -limit0
    return min (max (anObject, limit0), limit1)
    
def snap (anObject, target, margin):
    return target if abs (anObject - target) < margin else anObject
    
def digit (anObject, index):
    return int (('000000000000' + str (int (evaluate (anObject)))) [-evaluate (index + 1)])
    