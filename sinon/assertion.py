"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
"""
from .util import ErrorHandler
from .spy import SinonSpy

class SinonAssertion(object):
    """
    assertion is an API for external to verify inspector(s)
    """

    failException = AssertionError
    message = ""

    @classmethod
    def __is_spy(cls, spy):
        """
        checking the argument is spy
        Args: SinonSpy
        Raised: is_not_spy_error (if argument is not spy/stub/expectation)
        """
        if not isinstance(spy, SinonSpy):
            ErrorHandler.is_not_spy_error(spy)

    @classmethod
    def fail(cls, message):
        """
        Defining fail message of assertion
        This function will change message until all tests finished
        Args: str
        """
        SinonAssertion.message = message

    @classmethod
    def notCalled(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is not called
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        if not (not spy.called):
            raise cls.failException(cls.message)

    @classmethod
    def called(cls, spy):
        """
        Checking the inspector is called
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        if not (spy.called):
            raise cls.failException(cls.message)

    @classmethod
    def calledOnce(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is called once
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        if not (spy.calledOnce):
            raise cls.failException(cls.message)

    @classmethod
    def calledTwice(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is called twice
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        if not (spy.calledTwice):
            raise cls.failException(cls.message)

    @classmethod
    def calledThrice(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is called thrice
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        if not (spy.calledThrice):
            raise cls.failException(cls.message)

    @classmethod
    def callCount(cls, spy, number): #pylint: disable=invalid-name
        """
        Checking the inspector is called number times
        Args: SinonSpy, number
        """
        cls.__is_spy(spy)
        if not (spy.callCount == number):
            raise cls.failException(cls.message)

    @classmethod
    def callOrder(cls, *args): #pylint: disable=invalid-name
        """
        Checking the inspector is called with given priority
        Args: SinonSpy, list of inspectors
        eg.
            [spy1, spy2, spy3] => spy1 is called before spy2, spy2 is called before spy3
            [spy1, spy2, spy1] => spy1 is called before and after spy2
        """
        for spy in args:
            cls.__is_spy(spy)
        for idx, val in enumerate(args):
            if val != args[0]:
                if not (val.calledAfter(args[idx-1])):
                    raise cls.failException(cls.message)
            if val != args[-1]:
                if not (val.calledBefore(args[idx+1])):
                    raise cls.failException(cls.message)

    @classmethod
    def calledWith(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is called with partial args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.calledWith(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def alwaysCalledWith(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is always called with partial args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.alwaysCalledWith(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def neverCalledWith(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is never called with partial args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.neverCalledWith(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def calledWithExactly(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is called with exactly args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.calledWithExactly(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def alwaysCalledWithExactly(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is always called with exactly args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.alwaysCalledWithExactly(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def calledWithMatch(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is called with partial SinonMatcher(args/kwargs)
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.calledWithMatch(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def alwaysCalledWithMatch(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is always called with partial SinonMatcher(args/kwargs)
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.alwaysCalledWithMatch(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def neverCalledWithMatch(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is never called with partial SinonMatcher(args/kwargs)
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        if not (spy.neverCalledWithMatch(*args, **kwargs)):
            raise cls.failException(cls.message)

    @classmethod
    def threw(cls, spy, error_type=None):
        """
        Checking the inspector is raised error_type
        Args: SinonSpy, Exception (defaut: None)
        """
        cls.__is_spy(spy)
        if not (spy.threw(error_type)):
            raise cls.failException(cls.message)

    @classmethod
    def alwaysThrew(cls, spy, error_type=None): #pylint: disable=invalid-name
        """
        Checking the inspector is always raised error_type
        Args: SinonSpy, Exception (defaut: None)
        """
        cls.__is_spy(spy)
        if not (spy.alwaysThrew(error_type)):
            raise cls.failException(cls.message)
