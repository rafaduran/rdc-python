#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`src.decorators` --- Very short description
===================================================
Long description

.. module:: src.decorators 
    :synopsis: Short description
    
.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""
from __future__ import print_function
import functools



class memoized(object):
    """
    :py:class:`memoized` decorator caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and not re-evaluated.
    
    This decorator recipe has been taking from 
    `Python decorators libray <http://wiki.python.org/moin/PythonDecoratorLibrary>`_
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
        def __repr__(self):
            """Return the function's docstring."""
            return self.func.__doc__
        def __get__(self, obj, objtype):
            """Support instance methods."""
            return functools.partial(self.__call__, obj)


def dummy_decorator(func):
    """
    :py:func:`dummy_decorator` description
    """
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


def optional_arguments_decorator(real_decorator):
    """
    :py:func:`optional_arguments_decorator` is a decorates others decorators, so 
    they can be called with or without arguments. This receipt has been taken from 
    chapter 2 of Martyn Alchin's "Pro Django" book.
    
    .. note::
        Decorators using this receipt must used extra arguments as keywords 
        arguments
        
    Usage example::
       
        @optional_arguments_decorator
        def decorate(func, args, kwargs, prefix='Decorated'):
            return '{0}: {1}'.format(prefix, func(*args, **kwargs))
            
        @decorate
        def test(a, b):
            return a + b     

        print(test(13,4))

        test = decorate(test, prefix='Decorated again')

        print(test(13,4))
    """
    def decorator(func=None, **kwargs):
        # This is the decorator that will be
        # exposed to the rest of your program
        def decorated(func):
            # This returns the final, decorated
            # function, regardless of how it was called
            def wrapper(*a, **kw):
                return real_decorator(func, a, kw, **kwargs)
            return wrapper
        if func is None:
            # The decorator was called with arguments
            def decorator(func):
                return decorated(func)
            return decorator
        # The decorator was called without arguments
        return decorated(func)
    return decorator


def enter_exit(func, args, kwargs, writer=print):
    """
    :py:func:`enter_exit` decorator prints messages when entering and exiting 
    given function, useful while debugging
    
    :params writer: takes end and start string and does something
    :type writer: callable
    
    :Author: Rafael Durán Castañeda <rafadurancastaneda@gmail.com>
    
    .. warning::
        :py:func:`enter_exit` needs :py:func:`optional_arguments_decorator` and
        importing print function::
        
            from __future__ import print_function
        
    Simple usage::
    
        @enter_exit
        def log_test():
            pass
            
    so you can do:

    >>> log_test()
    Entering log_test
    Exiting log_test
    
        
    Using logging::
    
        import logging
        logging.basicConfig(level='INFO')
        @enter_exit(writer=logging.info)
        def log_test():
            pass
        
    Now you can do:
        
    >>> log_test()
    INFO:root:Entering log_test
    INFO:root:Exiting log_test
        
    
    Once more::
     
        lista = []
        @enter_exit(writer=lista.append)
        def log_test():
            pass

    So:
    
    >>> log_test()
    >>> print(' '.join([cad for cad in lista]))
    Entering log_test Exiting log_test
    
    """
    writer("Entering {0}".format(func.__name__))
    func(*args, **kwargs)
    writer("Exiting {0}".format(func.__name__))
    
    
def error_wrapper(func, args, kwargs, errors=Exception):
    """
    :py:func:`error_wrapper` wrappes any given number of exceptions, if no
    agrument then wrappes :py:class:`Exception`.
    
    :params func: function to be decorated
    :params args: needed by :py:func:`optional_arguments_decorator`
    :params kwargs: needed by :py:func:`optional_arguments_decorator`
    :params errors: errors to be wrapped, default :py:class:`Exception`
    :type errors: tuple or Exception
    :Author: Rafael Durán Castañeda <rafadurancastaneda@gmail.com>
    
    .. warning::
        
        :py:func:`exception_wrapper` uses 
        :py:func:`~decorator.optional_arguments_decorator`, so it must be used together or 
        imported
        
    Usage::
    
        @exception_wrapper(errors=(TypeError, ValueError, ZeroDivisionError))
        def test(a, b):
            return a / b
        
    And then you'll get:
        
    >>> test(9, 0)
    integer division or modulo by zero
    >>> test(5, "string")
    unsupported operand type(s) for /: 'int' and 'str'
    
    This works nice with partial::
    
        import functools
        
        os_io_error_wrapper = functools.partial(error_wrapper, errors=(IOError, OSError))
        
        @os_io_error_wrapper
        def test():
            file = open("Doesn't exist", "rb")
            
    so:
    
    >>> test()
    [Errno 2] No such file or directory: "Doesn't exist"

    """
    try:
        func(*args, **kwargs)
    except errors as e:
        # do something
        # raise it
        print(e) # or just print exception
    return

wrapper = optional_arguments_decorator(error_wrapper)


def dict_from_class(cls, filter=('__module__',  '__name__',  '__weakref__', 
     '__dict__', '__doc__')):
    """
    Returns all attributes for a given class, filtering unwanted attributes
    """
    return dict(
        (key, value)
        for (key, value) in cls.__dict__.items()
        if key not in filter )
    
def property_from_class(cls):
    """
    Class decorator used to build a property attribute from a class
    
    .. warning:::py:func:`exception_wrapper` uses 
        :py:func:`dict_from_class`, so it must be used together or imported
        
    Usage::
        
        class A(object):
            @property_from_class 
            class value(object):
                '''Value must be an integer'''
                def fget(self):
                    return self.__value
                def fset(self, value):
                    # Ensure that value to be stored is an int.
                    assert isinstance(value, int), repr(value)
                self.__value = value

    Now you can do::
    
            >>> a = A()
            >>> a.value = 4
            >>>print(a.value)
            4
            >>>print(A.value.__doc__)
            Value must be an integer
            >>>a.value = 'hola'
            Traceback (most recent call last):
            File "/home/rdc/workspace/decorator/decorator.py", line 161, in <module>
            a.value = 'hola'
            File "/home/rdc/workspace/decorator/decorator.py", line 150, in fset
            assert isinstance(value, int), repr(value)
            AssertionError: 'hola'

    """
    return property(doc=cls.__doc__, **dict_from_class(cls))