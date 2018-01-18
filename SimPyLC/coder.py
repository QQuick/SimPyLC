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

from sys import *
from ast import *
from _ast import *
from datetime import *
import os
from os.path import *
from re import *

from .base import programDir, decapitalize, programNameAndVersion

def generateCode (world):
    return coder.code (world)   
    
class Coder:
    def __init__ (self):
        self.symbolTable = {}

    def code (self, world):
        modules = world._modules
        
        try:
            self.nativeCode = sub (r'/\*\*.*?\*\*/', '', open ('native.cpp') .read (), flags = DOTALL)
        except:
            return
    
        if len (argv) < 2:
            return False

        print ('Code generation started')
        tailArgs = argv [1:]
        self.moduleNameList = [module._name for module in modules] if '*' in tailArgs else [arg for arg in tailArgs if not '=' in arg]

        argDict = dict ([arg.split ('=') for arg in tailArgs if '=' in arg])        
        self.plcPrefix = '{0}_'.format (argDict ['prefix']) if 'prefix' in argDict else ''
        self.device = argDict ['device'] if 'device' in argDict else 'arduino'
        self.addModulePrefix = len (self.moduleNameList) > 1
        
        self.cSymbols = {
            UnaryOp: {Not: '!', UAdd: '+', USub: '-'},
            BinOp: {Add: '+', Sub: '-', Mult: '*', Div: '/', Mod: '%'},
            BoolOp: {And: '&&', Or: '||'},
            Compare: {Eq: '==', NotEq: '!=', Lt: '<', LtE: '<=', Gt: '>', GtE: '>='}
        }
        
        self.parse ()
        # self.dump ()  # Leave in for debugging purposes
        self.generate ()
        
        print ('Code generation ready')
        return True

    def parse (self):
        def getContent (fileName):
            with open (fileName) as file:
                return file.read ()
    
        self.moduleFileNames = ['{0}.py'.format (moduleName) for moduleName in self.moduleNameList]
        self.sourceCodes = [getContent (moduleFileName) for moduleFileName in self.moduleFileNames]
        self.parseTrees = [parse (sourceCode) for sourceCode in self.sourceCodes]
                    
    def dump (self):
        def walk (name, value, tabLevel, fragments):
            fragments .append ('\n{0}{1}: {2} '.format (tabLevel * '\t', name, type (value).__name__ ))
            if isinstance (value, AST):
                for field in iter_fields (value):
                    walk (field [0], field [1], tabLevel + 1, fragments)
            elif isinstance (value, list):
                for element in value:
                    walk ('element', element, tabLevel + 1, fragments)
            else:
                fragments.append ('= {0}'.format (value))
                
        fragments = []
        for parseTree in self.parseTrees:
            walk ('file', parseTree, 0, fragments)
            
        self.targetFile = open ('{0}.{1}'.format (programDir, 'tree'), 'w')
        self.targetFile.write (''.join (fragments) [1:])
        self.targetFile.close ()    
                
    def generate (self):
        initCode = '\n'.join ([GeneratingVisitor (parseTree, True) .code for parseTree in self.parseTrees])
        sweepCode = '\n'.join ([GeneratingVisitor (parseTree, False) .code for parseTree in self.parseTrees])
                
        generatedCode = (
            self.getPrologue () + (
'''


// ____________ PLC variables ____________

'''
            ) + 
            initCode +  (
'''


// ____________ PLC cycle ____________

void {0}cycle () {{

'''
            ).format (self.plcPrefix) + 
            sweepCode +
            (
'''
    // ______ System ______

    {0}update ();
}}
'''
            ).format (self.plcPrefix) +
            self.getEpilogue ()
        )
        
        generationRoot = 'generated'
        generationDir = '{0}/{1}'.format (generationRoot, programDir)
        
        if not exists (generationDir):
            os.makedirs (generationDir)
                
        self.targetFile = open ('{0}/{1}.{2}'.format (generationDir, programDir, 'ino'), 'w')       
        self.targetFile.write (generatedCode + self.nativeCode)
        self.targetFile.close ()
        
    def getPrologue (self):
        return (
'''// ======================== BEGIN OF GENERATED CODE ========================



// ====== BEGIN OF License COMMENT BLOCK, INCLUDE IN ANY COPY OF THIS GENERATED CODE AND DO NOT REMOVE ======
//
// I M P O R T A N T   S A F E T Y   N O T I C E
//
// THIS CODE IS INTENDED SOLELY FOR EDUCATIONAL PURPOSES AND IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS.
// IT IS STRICKTLY PROHIBITED TO USE THIS GENERATED CODE IN ANY SITUATION THAT ENTAILS RISK OF DAMAGE OR INJURIES.
//
// USE OF THIS CODE IS GOVERNED BY THE QQUICK LICENSE (WWW.QQUICK.ORG/LICENSE).
// YOUR LICENSE TO USE THIS GENERATED CODE AUTOMATICALLY ENDS IF YOU REMOVE OR LEAVE OUT THIS LICENSE COMMENT BLOCK OR THE CODE THAT GENERATED IT. 
//
// ====== END OF License COMMENT BLOCK, INCLUDE IN COPY OF THIS GENERATED CODE AND DO NOT REMOVE ======



// Generator: {1}
// Generated: {2}
// Target platform: {3}



// ____________ General includes ____________

#include <math.h>



// ____________ {3} macros ____________
{4}


// ____________ General macros ____________

// Circuit operations

#define {0}mark4(marker, trueValue, condition, falseValue) marker = (condition) ? (trueValue) : (falseValue)
#define {0}mark3(marker, trueValue, condition) if (condition) marker = (trueValue)
#define {0}mark2(marker, trueValue) marker = (trueValue)
#define {0}mark1(marker) marker = {0}True

#define {0}trigger2(oneshot, condition) oneshot.value = oneshot.memo; oneshot.memo = (condition); oneshot.value = !oneshot.value and oneshot.memo
#define {0}trigger1(oneshot) oneshot.value = !oneshot.memo; oneshot.memo = {0}True
#define {0}spiked1(oneshot) (oneshot.value)

#define {0}latch2(latch, condition) if (condition) latch = {0}True
#define {0}latch1 (latch) latch = {0}True

#define {0}unlatch2(latch, condition) if (condition) latch = {0}False
#define {0}unlatch1 (latch) latch = {0}False

#define {0}set4(register, trueValue, condition, falseValue) register = (condition) ? (trueValue) : (falseValue)
#define {0}set3(register, trueValue, condition) if (condition) register = (trueValue)
#define {0}set2(register, trueValue) register = (trueValue)
#define {0}set1(register) register = 1

#define {0}reset2(timer, condition) if (condition) {{timer.exact = {0}nowExact; timer.inexact = {0}nowInexact;}}
#define {0}reset1(timer) timer.exact = {0}nowExact; timer.inexact = {0}nowInexact
#define {0}elapsed1(timer) (({0}nowInexact - timer.inexact) < 3.6e6 ? 1e-6 * ({0}nowExact - timer.exact) : 1e-3 * ({0}nowInexact - timer.inexact))

// Support operations

#define {0}update()\\
    {0}thenExact = {0}nowExact; {0}nowExact = {0}getNowExact(); {0}period = 1e-6 * ({0}nowExact - {0}thenExact);\\
    {0}nowInexact = {0}getNowInexact();\\
    {0}first = {0}False;

// Types

#define {0}False 0
#define {0}True 1
#define {0}Bool bool
#define {0}UInt unsigned long
#define {0}Int long
#define {0}Float double
#define {0}Marker int
#define {0}Oneshot struct {{int value; int memo;}}
#define {0}Latch int
#define {0}Register double
#define {0}Timer struct {{unsigned long exact; unsigned long inexact;}}

// Math operations

#define {0}abs1(value) fabs (value)
#define {0}max2(value0, value1) fmax (value0, value1)
#define {0}min2(value0, value1) fmin (value0, value1)
#define {0}limit3(value, aLimit0, aLimit1) min (max (value, aLimit0), aLimit1)  
#define {0}limit2(value, aLimit) {0}limit3 (value, -aLimit, aLimit)
#define {0}digit2(value, index) getDigit (int (value), index)

// ____________ General functions ____________

int {0}getDigit (int value, int index) {{
    return (index == 0) ? value % 10 : {0}getDigit (value / 10, --index);
}}

// ____________ General variables ____________

{0}UInt {0}nowExact = 0;
{0}UInt {0}thenExact = 0;
{0}UInt {0}nowInexact = 0;
{0}Float {0}period = 1;
{0}Bool {0}first = {0}True;
'''
    ).format (self.plcPrefix, programNameAndVersion, datetime.now (), self.device.capitalize (), self.getPlatformMacros ())
        
    def getEpilogue (self):
        return (
'''


// ======================== END OF GENERATED CODE ========================

'''
    )
        
    def getPlatformMacros (self):
        return (
'''
#define {0}getNowExact() micros ()
#define {0}getNowInexact() millis ()
'''         
    ).format (self.plcPrefix)

        
coder = Coder ()

class GeneratingVisitor (NodeVisitor):
    def __init__ (self, tree, init):
        self.fragments = []
        
        self.indentLevel = 0
        self.init = init
        self.visit (tree)

    def emit (self, fragment):
        self.fragments.append (fragment)
        
    def indent (self):
        self.indentLevel += 1
        
    def unIndent (self):
        self.indentLevel -= 1
    
    def getIndent (self):
        return self.indentLevel * '\t'
        
    def getModulePrefix (self, moduleName):
        return (
                ''
            if not coder.addModulePrefix or moduleName == 'world' else
                '{0}_'.format (self.moduleName)
            if moduleName == 'self' else
                '{0}_'.format (moduleName)
        )   
        
    def getError (self, node, text):
        return 'Error in module \'{0}\', line {1}: {2}'.format (self.moduleName, node.lineno, text) 

    def visit_ClassDef (self, node):
        self.moduleName = decapitalize (node.name)
        for statement in node.body:
            self.visit (statement)
        if self.init:
            self.code = ''.join (['// ______ Module: {0} ______'.format (self.moduleName)] + self.fragments)
        else:
            self.code = ''.join (['\t// ______ Module: {0} ______\n'.format (self.moduleName)] + self.fragments)
        
    def visit_FunctionDef (self, node):
        def visitBody ():
            for element in node.body:
                self.surpressSemicolon = False
                self.surpressNewline = False
                self.visit (element)
                if not self.surpressSemicolon:
                    self.emit (';')
                if not self.surpressNewline:
                    self.emit ('\n')

        if self.init:
            if node.name == '__init__':
                visitBody ()
        else:
            if node.name != '__init__':
                self.indent ()
                self.emit ('\n{0}// ___ {1} ___\n'.format (self.getIndent (), node.name.capitalize ()))
                visitBody ()
                self.unIndent ()
            
    def visit_Expr (self, node):
        if self.init:
            if len (node.value.args):
                if node.value.func.attr == 'page':
                    self.emit ('\n{0}// Page: {1}'.format (self.getIndent (), node.value.args [0] .s))
                elif node.value.func.attr == 'group':
                    self.emit ('\n{0}// Group: {1}\n'.format (self.getIndent (), node.value.args [0] .s))
                self.surpressSemicolon = True
        else:
            self.generic_visit (node)
            
    def visit_Assign (self, node):
        if self.init:
            if node.value.func.id == 'Runner':
                self.surpressSemicolon = True
                self.surpressNewline = True
            else:
                coder.symbolTable ['{0}{1}{2}'.format (coder.plcPrefix, self.getModulePrefix (node.targets[0] .value.id), node.targets [0] .attr)] = node.value.func.id
                self.emit ('{0}{1}{2} {1}{3}{4}'.format (
                    self.getIndent (),
                    coder.plcPrefix,
                    node.value.func.id,
                    self.getModulePrefix (node.targets [0] .value.id),
                    node.targets [0] .attr
                ))
                self.emit (' = ')           
                
                if node.value.func.id in ('Marker', 'Latch'):
                    if node.value.args:
                        self.emit ('{0}{1}'.format (coder.plcPrefix, node.value.args [0] .value))
                    else:
                        self.emit ('{0}False'.format (coder.plcPrefix))
                elif node.value.func.id == 'Oneshot':
                    if node.value.args:
                        self.emit ('{{0}{1}, {0}{False}}'.format (coder.plcPrefix, node.value.args [0] .id))
                    else:
                        self.emit ('{{{0}False, {0}False}}'.format (coder.plcPrefix))
                elif node.value.func.id == 'Register':
                    if node.value.args:
                        self.emit ('{0}'.format (node.value.args [0] .n))
                    else:
                        self.emit ('0')
                elif node.value.func.id == 'Timer':
                    self.emit ('{{{0}nowExact, {0}nowInexact}}'.format (coder.plcPrefix))
                else:
                    raise Exception (self.getError (node, 'Element {0} not allowed here'.format (node.value.func.id)))
        else:
            raise Exception (self.getError (node, 'Operator = not allowed here'))

    def visit_Call (self, node):
        if node.func.__class__ == Attribute:    # Member function
            if node.func.attr == 'part':
                self.emit ('\n{0}// Part: {1}\n'.format (self.getIndent (), node.args [0] .s))
                self.surpressSemicolon = True
            else:
                if (
                    type (node.func.value) == Attribute and node.func.value.value.id in coder.moduleNameList + ['self']
                    and (
                        not node.args
                        or 
                        type (node.args [0]) != Attribute
                        or
                        type (node.args [0].value) != Attribute
                        or
                        node.args [0].value.attr in coder.moduleNameList + ['self']
                    )
                ):
                    self.emit ('{0}'.format (self.getIndent ()))
                    self.emit ('{0}{1}{2} ('.format (coder.plcPrefix, node.func.attr, len (node.args) + 1))
                    self.emit ('{0}{1}{2}'.format (
                        coder.plcPrefix,
                        self.getModulePrefix (node.func.value.value.id),
                        node.func.value.attr
                    ))
                    for arg in node.args:
                        self.emit (', ')
                        self.visit (arg)
                    self.emit (')')
                else:
                    self.surpressSemicolon = True
                    self.surpressNewline = True
                
        else:   # Free function
            self.emit ('{0}{1}{2} ('.format (coder.plcPrefix, node.func.id, len (node.args)))
            for index, arg in enumerate (node.args):
                if index:
                    self.emit (', ')
                self.visit (arg)            
            self.emit (')')

    def visit_Attribute (self, node):
        objectName = (
                node.value.attr
            if type (node.value) == Attribute else
                node.value.id
        )
        
        qualifiedName = '{0}{1}{2}'.format (coder.plcPrefix, self.getModulePrefix (objectName), node.attr)
        
        if qualifiedName == '{0}period'.format (coder.plcPrefix):
            self.emit (qualifiedName)
        elif coder.symbolTable [qualifiedName] == 'Timer':
            self.emit ('{0}elapsed1 ({1})'.format (coder.plcPrefix, qualifiedName))
        elif coder.symbolTable [qualifiedName] == 'Oneshot':
            self.emit ('{0}spiked1 ({1})'.format (coder.plcPrefix, qualifiedName))
        else:
            self.emit (qualifiedName)
            
    def visit_Pass (self, node):
        self.emit ('{0}'.format (self.getIndent ()))

    def visit_Num (self, node):
        self.emit (repr (node.n))

    def visit_Name (self, node):
        self.emit (node.id if not node.id in (True, False) else '{0}{1}'.format (coder.plcPrefix, node.id))

    def visit_NameConstant (self, node):
        self.emit ('{0}'.format (node.value))
        
    def visit_UnaryOp (self, node):
        self.emit('(')
        self.emit ('{0}'.format (coder.cSymbols [UnaryOp][type (node.op)]))
        self.visit (node.operand)
        self.emit (')')
                
    def visit_BinOp (self, node):
        self.emit ('(')
        if type (node.op) == Mod:
            self.emit ('({0}Int) '.format (coder.plcPrefix))
        self.visit (node.left)
        self.emit (' {0} '.format (coder.cSymbols [BinOp][type (node.op)]))
        if type (node.op) == Mod:
            self.emit ('({0}Int) '.format (coder.plcPrefix))
        self.visit (node.right)
        self.emit (')')

    def visit_BoolOp (self, node):
        self.emit ('(')
        for index, value in enumerate (node.values):
            if index:
                self.emit (' {0} '.format (coder.cSymbols [BoolOp][type (node.op)]))
            self.visit (value)
        self.emit (')')

    def visit_Compare (self, node):
        self.emit ('(')
        left = node.left
        for index, (operand, right) in enumerate (zip (node.ops, node.comparators)):
            if index:
                self.emit (' && ')
            self.visit (left)
            self.emit (' {0} '.format (coder.cSymbols [Compare][type (operand)]))
            self.visit (right)
            left = right
        self.emit(')')
        