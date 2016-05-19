#! /usr/bin/env python
# $Header$
'''Typecodes for numbers.
'''

from pysphere.ZSI import _inttypes, _floattypes, _seqtypes, \
        EvaluateException
from pysphere.ZSI.TC import TypeCode, Integer, Decimal
from pysphere.ZSI.wstools.Namespaces import SCHEMA

class IunsignedByte(Integer):
    '''Unsigned 8bit value.
    '''
    type = (SCHEMA.XSD3, "unsignedByte")
    parselist = [ (None, "unsignedByte") ]
    seriallist = [ ]

class IunsignedShort(Integer):
    '''Unsigned 16bit value.
    '''
    type = (SCHEMA.XSD3, "unsignedShort")
    parselist = [ (None, "unsignedShort") ]
    seriallist = [ ]

class IunsignedInt(Integer):
    '''Unsigned 32bit value.
    '''
    type = (SCHEMA.XSD3, "unsignedInt")
    parselist = [ (None, "unsignedInt") ]
    seriallist = [ ]

class IunsignedLong(Integer):
    '''Unsigned 64bit value.
    '''
    type = (SCHEMA.XSD3, "unsignedLong")
    parselist = [ (None, "unsignedLong") ]
    seriallist = [ ]

class Ibyte(Integer):
    '''Signed 8bit value.
    '''
    type = (SCHEMA.XSD3, "byte")
    parselist = [ (None, "byte") ]
    seriallist = [ ]

class Ishort(Integer):
    '''Signed 16bit value.
    '''
    type = (SCHEMA.XSD3, "short")
    parselist = [ (None, "short") ]
    seriallist = [ ]

class Iint(Integer):
    '''Signed 32bit value.
    '''
    type = (SCHEMA.XSD3, "int")
    parselist = [ (None, "int") ]
    seriallist = [ int ]

class Ilong(Integer):
    '''Signed 64bit value.
    '''
    type = (SCHEMA.XSD3, "long")
    parselist = [(None, "long")]
    seriallist = [ long ]

class InegativeInteger(Integer):
    '''Value less than zero.
    '''
    type = (SCHEMA.XSD3, "negativeInteger")
    parselist = [ (None, "negativeInteger") ]
    seriallist = [ ]

class InonPositiveInteger(Integer):
    '''Value less than or equal to zero.
    '''
    type = (SCHEMA.XSD3, "nonPositiveInteger")
    parselist = [ (None, "nonPositiveInteger") ]
    seriallist = [ ]

class InonNegativeInteger(Integer):
    '''Value greater than or equal to zero.
    '''
    type = (SCHEMA.XSD3, "nonNegativeInteger")
    parselist = [ (None, "nonNegativeInteger") ]
    seriallist = [ ]

class IpositiveInteger(Integer):
    '''Value greater than zero.
    '''
    type = (SCHEMA.XSD3, "positiveInteger")
    parselist = [ (None, "positiveInteger") ]
    seriallist = [ ]

class Iinteger(Integer):
    '''Integer value.
    '''
    type = (SCHEMA.XSD3, "integer")
    parselist = [ (None, "integer") ]
    seriallist = [ ]

class IEnumeration(Integer):
    '''Integer value, limited to a specified set of values.
    '''

    def __init__(self, choices, pname=None, **kw):
        Integer.__init__(self, pname, **kw)
        self.choices = choices
        t = type(choices)
        if isinstance(choices, _seqtypes):
            self.choices = tuple(choices)
        elif TypeCode.typechecks:
            raise TypeError(
                'Enumeration choices must be list or sequence, not ' + str(t))
        if TypeCode.typechecks:
            for c in self.choices:
                if not isinstance(c, _inttypes):
                    raise TypeError('Enumeration choice "' +
                            str(c) + '" is not an integer')

    def parse(self, elt, ps):
        val = Integer.parse(self, elt, ps)
        if val not in self.choices:
            raise EvaluateException('Value "' + str(val) + \
                        '" not in enumeration list',
                    ps.Backtrace(elt))
        return val

    def serialize(self, elt, sw, pyobj, name=None, orig=None, **kw):
        if pyobj not in self.choices:
            raise EvaluateException('Value not in int enumeration list')
        Integer.serialize(self, elt, sw, pyobj, name=name, orig=orig, **kw)


class FPfloat(Decimal):
    '''IEEE 32bit floating point value.
    '''
    type = (SCHEMA.XSD3, "float")
    parselist = [ (None, "float") ]
    seriallist = [ float ]

class FPdouble(Decimal):
    '''IEEE 64bit floating point value.
    '''
    type = (SCHEMA.XSD3, "double")
    parselist = [ (None, "double") ]
    seriallist = [ ]

class FPEnumeration(FPfloat):
    '''Floating point value, limited to a specified set of values.
    '''

    def __init__(self, choices, pname=None, **kw):
        FPfloat.__init__(self, pname, **kw)
        self.choices = choices
        t = type(choices)
        if isinstance(choices, _seqtypes):
            self.choices = tuple(choices)
        elif TypeCode.typechecks:
            raise TypeError(
                'Enumeration choices must be list or sequence, not ' + str(t))
        if TypeCode.typechecks:
            for c in self.choices:
                if not isinstance(c, _floattypes):
                    raise TypeError('Enumeration choice "' +
                            str(c) + '" is not floating point number')

    def parse(self, elt, ps):
        val = Decimal.parse(self, elt, ps)
        if val not in self.choices:
            raise EvaluateException('Value "' + str(val) + \
                        '" not in enumeration list',
                    ps.Backtrace(elt))
        return val

    def serialize(self, elt, sw, pyobj, name=None, orig=None, **kw):
        if pyobj not in self.choices:
            raise EvaluateException('Value not in int enumeration list')
        Decimal.serialize(self, elt, sw, pyobj, name=name, orig=orig, **kw)

