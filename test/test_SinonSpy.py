import sys
sys.path.insert(0, '../')

import unittest
import sinon.base as sinon
from sinon.spy import SinonSpy
from sinon.sandbox import sinontest
from sinon.matcher import SinonMatcher, Matcher

"""
======================================================
                 FOR TEST ONLY START
======================================================
"""
# build-in module
import os
# customized class
class A_object(object):
    # customized function
    def A_func(self):
        return "test_global_A_func"

# global function
def B_func(x=None):
    if x:
        return "test_local_B_func"+str(x)
    return "test_local_B_func"

def C_func(a="a", b="b", c="c"):
    return "test_local_C_func"

def D_func(err=False):
    if err:
        raise err
    else:
        return "test_local_D_func"

def E_func(*args, **kwargs):
    return str(args) + ' ' + str(kwargs)

"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonSpy(unittest.TestCase):

    def setUp(self):
        sinon.g = sinon.init(globals())

    @sinontest
    def test040_called_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        self.assertTrue(spy.called)

    @sinontest
    def test041_calledOnce_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test042_calledTwice_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(spy.calledTwice)

    @sinontest
    def test043_calledThrice_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(spy.calledThrice)

    @sinontest
    def test044_calledOnce_module_method(self):
        spy = SinonSpy(os, "system")
        os.system("cd")
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test045_calledTwice_module_method(self):
        spy = SinonSpy(os, "system")
        os.system("cd")
        os.system("cd")
        self.assertTrue(spy.calledTwice)

    @sinontest
    def test046_calledThrice_module_method(self):
        spy = SinonSpy(os, "system")
        os.system("cd")
        os.system("cd")
        os.system("cd")
        self.assertTrue(spy.calledThrice)

    @sinontest
    def test047_calledOnce_empty(self):
        spy = SinonSpy()
        spy()
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test048_calledTwice_empty(self):
        spy = SinonSpy()
        spy()
        spy()
        self.assertTrue(spy.calledTwice)

    @sinontest
    def test049_calledThrice_empty(self):
        spy = SinonSpy()
        spy()
        spy()
        spy()
        self.assertTrue(spy.calledThrice)

    @sinontest
    def test050_firstCall_callId(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        spy3 = SinonSpy(B_func)
        spy4 = SinonSpy()
        os.system("cd")
        spy2()
        sinon.g.B_func()
        spy4()
        self.assertEqual(spy1.firstCall.callId, 0)
        self.assertEqual(spy2.firstCall.callId, 1)
        self.assertEqual(spy3.firstCall.callId, 2)
        self.assertEqual(spy4.firstCall.callId, 3)

    @sinontest
    def test051_calledBefore_calledAfter_normal(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        spy3 = SinonSpy(B_func)
        os.system("cd")
        spy2()
        sinon.g.B_func()
        self.assertFalse(spy1.calledBefore(spy1))
        self.assertFalse(spy2.calledBefore(spy2))
        self.assertFalse(spy3.calledBefore(spy3))
        self.assertFalse(spy1.calledAfter(spy1))
        self.assertFalse(spy2.calledAfter(spy2))
        self.assertFalse(spy3.calledAfter(spy3))
        self.assertTrue(spy1.calledBefore(spy2))
        self.assertTrue(spy1.calledBefore(spy3))
        self.assertTrue(spy2.calledBefore(spy3))
        self.assertFalse(spy1.calledAfter(spy2))
        self.assertFalse(spy1.calledAfter(spy3))
        self.assertFalse(spy2.calledAfter(spy3))
        self.assertTrue(spy2.calledAfter(spy1))
        self.assertTrue(spy3.calledAfter(spy1))
        self.assertTrue(spy3.calledAfter(spy2))
        self.assertFalse(spy2.calledBefore(spy1))
        self.assertFalse(spy3.calledBefore(spy1))
        self.assertFalse(spy3.calledBefore(spy2))

    @sinontest
    def test052_calledBefore_nothing_called(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        self.assertFalse(spy1.calledBefore(spy2))
        self.assertFalse(spy2.calledBefore(spy1))
        self.assertFalse(spy2.calledAfter(spy1))
        self.assertFalse(spy1.calledAfter(spy2))

    @sinontest
    def test053_calledBefore_calledAfter_recalled_method(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        os.system("cd")
        self.assertTrue(spy1.calledBefore(spy2))
        self.assertFalse(spy1.calledAfter(spy2))
        self.assertFalse(spy2.calledBefore(spy1))
        self.assertFalse(spy2.calledAfter(spy1))
        spy2()
        self.assertTrue(spy1.calledBefore(spy2))
        self.assertFalse(spy1.calledAfter(spy2))
        self.assertFalse(spy2.calledBefore(spy1))
        self.assertTrue(spy2.calledAfter(spy1))
        os.system("cd")
        self.assertTrue(spy1.calledBefore(spy2))
        self.assertTrue(spy1.calledAfter(spy2))
        self.assertTrue(spy2.calledBefore(spy1))
        self.assertTrue(spy2.calledAfter(spy1))
        spy1.restore()

    @sinontest
    def test054_calledBefore_calledAfter_called_restore_recalled(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        os.system("cd")
        spy1.restore()
        spy1 = SinonSpy(os, "system")
        spy2()
        os.system("cd")
        self.assertTrue(spy1.calledAfter(spy2))
        self.assertFalse(spy2.calledAfter(spy1))
        self.assertTrue(spy2.calledBefore(spy1))
        self.assertFalse(spy1.calledBefore(spy2))

    @sinontest
    def test070_calledWith_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.calledWith(a="a", b="b", c="c"))
        self.assertFalse(spy.calledWith(a="wrong", b="b", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.calledWith("a", "b", "c"))
        self.assertFalse(spy.calledWith("a", "wrong", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.calledWith("a", b="b", c="c"))
        self.assertTrue(spy.calledWith("a", "b", c="c"))
        self.assertTrue(spy.calledWith("a", "b", "c"))
        self.assertFalse(spy.calledWith("a", "b", "d"))
        self.assertFalse(spy.calledWith("a", "b", c="d"))

    @sinontest
    def test071_calledWith_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(spy.calledWith(a="wrong"))
        self.assertTrue(spy.calledWith(a="a"))
        self.assertTrue(spy.calledWith(b="b"))
        self.assertTrue(spy.calledWith(c="c"))
        self.assertFalse(spy.calledWith(a="wrong", b="b"))
        self.assertTrue(spy.calledWith(a="a", b="b"))
        self.assertTrue(spy.calledWith(b="b", c="c"))
        self.assertTrue(spy.calledWith(a="a", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.calledWith("d"))
        self.assertTrue(spy.calledWith("a"))
        self.assertFalse(spy.calledWith("b"))
        self.assertFalse(spy.calledWith("c"))
        self.assertFalse(spy.calledWith("wrong", "b"))
        self.assertTrue(spy.calledWith("a", "b"))
        self.assertFalse(spy.calledWith("b", "c"))
        self.assertFalse(spy.calledWith("a", "c"))
        self.assertTrue(spy.calledWith("a", "b", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.calledWith("a", b="b"))
        self.assertTrue(spy.calledWith("a", c="c"))
        self.assertTrue(spy.calledWith(b="b", c="c"))
        self.assertTrue(spy.calledWith("a"))
        self.assertTrue(spy.calledWith(c="c"))
        self.assertFalse(spy.calledWith("wrong", b="b"))
        self.assertFalse(spy.calledWith("a", b="wrong"))
        self.assertFalse(spy.calledWith("a", c="wrong"))

    @sinontest
    def test072_alwaysCalledWith_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith(a="a", b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(spy.alwaysCalledWith(a="a", b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWith("a", "b", "c"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(spy.alwaysCalledWith("a", "b", "c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith("a", b="b", c="c"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWith("a", b="b", c="c"))
        spy.restore()

    @sinontest
    def test073_alwaysCalledWith_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="xxxx", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith(b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(spy.alwaysCalledWith(b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "xxxx")
        self.assertTrue(spy.alwaysCalledWith("a", "b"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(spy.alwaysCalledWith("a", "b"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b")
        self.assertTrue(spy.alwaysCalledWith("a", b="b"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWith("a", b="b"))
        spy.restore()

    @sinontest
    def test074_calledWithExactly_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.calledWithExactly(a="a", b="b", c="c"))
        self.assertFalse(spy.calledWithExactly(a="d", b="e", c="f"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.calledWithExactly("a", "b", "c"))
        self.assertFalse(spy.calledWithExactly("d", "e", "f"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.calledWithExactly("a", b="b", c="c"))
        self.assertFalse(spy.calledWithExactly("wrong", b="b", c="c"))
        #Exception
        with self.assertRaises(Exception) as context:
            spy.calledWithExactly()

    @sinontest
    def test075_calledWithExactly_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(spy.calledWithExactly(a="a", b="b"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.calledWithExactly("a", "b"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(spy.calledWithExactly("a", b="b"))

    @sinontest
    def test076_alwaysCalledWithExactly_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly(a="a", b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(spy.alwaysCalledWithExactly(a="a", b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", "b", "c"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(spy.alwaysCalledWithExactly("a", "b", "c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", b="b", c="c"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWithExactly("a", b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #Exception
        with self.assertRaises(Exception) as context:
            spy.alwaysCalledWithExactly()


    @sinontest
    def test077_alwaysCalledWithExactly_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly(a="a", b="b", c="c"))
        sinon.g.C_func(a="xxxx", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWithExactly(b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", "b", "c"))
        sinon.g.C_func("a", "b", "xxxx")
        self.assertFalse(spy.alwaysCalledWithExactly("a", "b"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", b="b", c="c"))
        sinon.g.C_func("a", b="b", c="xxx")
        self.assertFalse(spy.alwaysCalledWithExactly("a", b="b"))
        spy.restore()

    @sinontest
    def test078_neverCalledWith_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(spy.neverCalledWith(a="a", b="b", c="c"))
        self.assertTrue(spy.neverCalledWith(a="wrong", b="b", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.neverCalledWith("a", "b", "c"))
        self.assertTrue(spy.neverCalledWith("a", "wrong", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(spy.neverCalledWith("a", b="b", c="c"))
        self.assertFalse(spy.neverCalledWith("a", "b", c="c"))
        self.assertFalse(spy.neverCalledWith("a", "b", "c"))
        self.assertTrue(spy.neverCalledWith("a", "b", "d"))
        self.assertTrue(spy.neverCalledWith("a", "b", c="d"))

    @sinontest
    def test079_neverCalledWith_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.neverCalledWith(a="wrong"))
        self.assertFalse(spy.neverCalledWith(a="a"))
        self.assertFalse(spy.neverCalledWith(b="b"))
        self.assertFalse(spy.neverCalledWith(c="c"))
        self.assertTrue(spy.neverCalledWith(a="wrong", b="b"))
        self.assertFalse(spy.neverCalledWith(a="a", b="b"))
        self.assertFalse(spy.neverCalledWith(b="b", c="c"))
        self.assertFalse(spy.neverCalledWith(a="a", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.neverCalledWith("d"))
        self.assertFalse(spy.neverCalledWith("a"))
        self.assertTrue(spy.neverCalledWith("b"))
        self.assertTrue(spy.neverCalledWith("c"))
        self.assertTrue(spy.neverCalledWith("wrong", "b"))
        self.assertFalse(spy.neverCalledWith("a", "b"))
        self.assertTrue(spy.neverCalledWith("b", "c"))
        self.assertTrue(spy.neverCalledWith("a", "c"))
        self.assertFalse(spy.neverCalledWith("a", "b", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(spy.neverCalledWith("a", b="b"))
        self.assertFalse(spy.neverCalledWith("a", c="c"))
        self.assertFalse(spy.neverCalledWith(b="b", c="c"))
        self.assertFalse(spy.neverCalledWith("a"))
        self.assertFalse(spy.neverCalledWith(c="c"))
        self.assertTrue(spy.neverCalledWith("wrong", b="b"))
        self.assertTrue(spy.neverCalledWith("a", b="wrong"))
        self.assertTrue(spy.neverCalledWith("a", c="wrong"))

    @sinontest
    def test090_threw_without_err(self):
        spy = SinonSpy(D_func)
        sinon.g.D_func(err=False)
        self.assertFalse(spy.threw())

    @sinontest
    def test091_threw_with_err(self):
        class MyException(Exception):
            pass

        spy = SinonSpy(D_func)

        try:
            sinon.g.D_func(err=MyException)
        except:
            pass
        self.assertTrue(spy.threw())
        self.assertTrue(spy.threw(MyException))
        self.assertFalse(spy.threw(ValueError))

        try:
            sinon.g.D_func(err=ValueError)
        except:
            pass
        self.assertTrue(spy.threw(ValueError))

    @sinontest
    def test092_alwaysThrew_without_err(self):
        spy = SinonSpy(D_func)
        sinon.g.D_func(err=False)
        sinon.g.D_func(err=False)
        self.assertFalse(spy.alwaysThrew())

    @sinontest
    def test093_alwaysThrew_with_same_err(self):
        class MyException(Exception):
            pass

        spy = SinonSpy(D_func)

        try:
            sinon.g.D_func(err=MyException)
            sinon.g.D_func(err=MyException)
        except:
            pass
        self.assertTrue(spy.alwaysThrew())
        self.assertTrue(spy.alwaysThrew(MyException))

        try:
            sinon.g.D_func(err=ValueError)
        except:
            pass
        self.assertFalse(spy.alwaysThrew(MyException))

    @sinontest
    def test100_returned(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        self.assertTrue(spy.returned("test_local_B_func"))
        sinon.g.B_func(2)
        self.assertTrue(spy.returned("test_local_B_func2"))

    @sinontest
    def test101_returned_exception(self):
        # exception will return a empty function with no return
        spy = SinonSpy(D_func)

        try:
            sinon.g.D_func(err=ValueError)
        except:
            pass
        self.assertFalse(spy.returned("test_local_D_func"))
        sinon.g.D_func()
        self.assertTrue(spy.returned("test_local_D_func"))

    @sinontest
    def test102_alwaysReturned(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(spy.alwaysReturned("test_local_B_func"))
        sinon.g.B_func(123)
        self.assertFalse(spy.alwaysReturned("test_local_B_func"))

    @sinontest
    def test110_called(self):
        spy1 = SinonSpy(B_func)
        spy2 = SinonSpy(C_func)
        sinon.g.B_func()
        self.assertTrue(spy1.called)   #B_func is called
        self.assertFalse(spy2.called)  #C_func is never called

    @sinontest
    def test111_getCall_wrongIndex(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func()
        self.assertEqual(spy.getCall(-100), None)
        self.assertEqual(spy.getCall(0).callId, 0)
        self.assertEqual(spy.getCall(100), None)

    @sinontest
    def test120_kwargs(self):
        spy = SinonSpy(C_func)
        self.assertEqual(spy.kwargs, [])
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertEqual(spy.kwargs, [{"a":"a", "b":"b", "c":"c"}])
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertEqual(spy.kwargs, [{"a":"a", "b":"b", "c":"c"}, {"a":"a", "b":"b", "c":"c"}])
        sinon.g.C_func("a", b="b", c="c")
        self.assertEqual(spy.kwargs, [{"a":"a", "b":"b", "c":"c"}, {"a":"a", "b":"b", "c":"c"}, {"b": "b", "c": "c"}])

    @sinontest
    def test121_args(self):
        spy = SinonSpy(C_func)
        self.assertEqual(spy.args, [])
        sinon.g.C_func("a", "b", "c")
        self.assertEqual(spy.args, [("a", "b", "c")])
        sinon.g.C_func("a", "b", "c")
        self.assertEqual(spy.args, [("a", "b", "c"), ("a", "b", "c")])
        sinon.g.C_func("a", b="b", c="c")
        self.assertEqual(spy.args, [("a", "b", "c"), ("a", "b", "c"), ("a",)])

    @sinontest
    def test122_exceptions(self):
        spy = SinonSpy(D_func)
        self.assertEqual(spy.exceptions, [])

        try:
            sinon.g.D_func(ValueError)
        except:
            pass
        self.assertEqual(spy.exceptions, [ValueError])

        try:
            sinon.g.D_func(TypeError)
        except:
            pass
        self.assertEqual(spy.exceptions, [ValueError, TypeError])

    @sinontest
    def test123_returnValues(self):
        spy = SinonSpy(B_func)
        self.assertEqual(spy.returnValues, [])
        sinon.g.B_func()
        self.assertEqual(spy.returnValues, ["test_local_B_func"])
        sinon.g.B_func(2)
        self.assertEqual(spy.returnValues, ["test_local_B_func", "test_local_B_func2"])

    @sinontest
    def test124_args_module_function(self):
        spy = SinonSpy(os, "system")
        self.assertEqual(spy.args, [])
        os.system("cd")
        self.assertEqual(spy.args, [("cd", )])

    @sinontest
    def test125_kwargs_module_function(self):
        spy = SinonSpy(os, "walk")
        self.assertEqual(spy.kwargs, [])
        os.walk(".", topdown=False)
        self.assertEqual(spy.kwargs, [{"topdown": False}])

    @sinontest
    def test126_kwargs_pure(self):
        spy = SinonSpy()
        self.assertEqual(spy.kwargs, [])
        spy(a="a")
        self.assertEqual(spy.kwargs, [{"a": "a"}])

    @sinontest
    def test127_returnValues_module_function(self):
        spy = SinonSpy(os, "system")
        self.assertEqual(spy.returnValues, [])
        os.system("cd")
        self.assertEqual(spy.returnValues, [0])

    @sinontest
    def test130_reset(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func(2)
        self.assertTrue(spy.called)
        self.assertTrue(spy.args)
        spy.reset()
        self.assertFalse(spy.called)
        self.assertFalse(spy.args)

    @sinontest
    def test140_spy_as_callback(self):
        def func(f):
            f()
        spy = SinonSpy()
        func(spy)
        self.assertTrue(spy.called)
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test141_spy_as_callback_withargs(self):
        def func(f):
            f(1)
        spy = SinonSpy()
        func(spy)
        self.assertTrue(spy.calledWith(1))

    @sinontest
    def test200_calledWithMatch_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.calledWithMatch("a"))
        self.assertTrue(spy.calledWithMatch("a", "b"))
        self.assertTrue(spy.calledWithMatch("a", "b", "c"))
        self.assertFalse(spy.calledWithMatch("a", "b", "c", "d"))
        self.assertFalse(spy.calledWithMatch("a", "c"))
        self.assertTrue(spy.calledWithMatch(str))
        self.assertFalse(spy.calledWithMatch(str, int))
        self.assertTrue(spy.calledWithMatch(str, str))
        self.assertTrue(spy.calledWithMatch(str, str, str))
        sinon.g.C_func("d", "e")
        self.assertTrue(spy.calledWithMatch("a", "b"))
        self.assertTrue(spy.calledWithMatch("d", "e"))
        self.assertFalse(spy.calledWithMatch("a", "e"))
        self.assertFalse(spy.calledWithMatch("d", "e", "c")) #it's a combination

    @sinontest
    def test201_calledWith_matcher(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.calledWith(str))
        self.assertTrue(spy.calledWith(SinonMatcher(str)))

    @sinontest
    def test203_calledWithMatch_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.calledWithMatch(a="a"))
        self.assertTrue(spy.calledWithMatch(a="a", b="b"))
        self.assertFalse(spy.calledWithMatch(a="d", b="e"))
        self.assertTrue(spy.calledWithMatch(a="a", b="b", c="c"))
        self.assertTrue(spy.calledWithMatch(a="a", c="c")) # dict is not rely on order of arguments
        self.assertTrue(spy.calledWithMatch(a=str))
        self.assertFalse(spy.calledWithMatch(a=str, b=int))
        self.assertTrue(spy.calledWithMatch(a=str, b=str))
        self.assertTrue(spy.calledWithMatch(a=str, b=str, c=str))
        sinon.g.C_func(a="d", b="e")
        self.assertTrue(spy.calledWithMatch(a="a", b="b"))
        self.assertTrue(spy.calledWithMatch(a="d", b="e"))
        self.assertFalse(spy.calledWithMatch(a="a", b="e"))
        self.assertFalse(spy.calledWithMatch(a="d", b="e", c="c")) #it's a combination

    @sinontest
    def test206_calledWithMatch_combination(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", c="c")
        self.assertTrue(spy.calledWithMatch("a"))
        self.assertTrue(spy.calledWithMatch("a", "b"))
        self.assertFalse(spy.calledWithMatch("d", "e"))
        self.assertTrue(spy.calledWithMatch("a", "b", c="c"))
        self.assertTrue(spy.calledWithMatch("a", c="c")) # dict is not rely on order of arguments
        self.assertTrue(spy.calledWithMatch(str))
        self.assertFalse(spy.calledWithMatch(str, int))
        self.assertTrue(spy.calledWithMatch(str, str))
        self.assertTrue(spy.calledWithMatch(str, str, c=str))
        sinon.g.C_func("d", b="e")
        self.assertFalse(spy.calledWithMatch("a", b="b"))
        self.assertTrue(spy.calledWithMatch("d", b="e"))
        self.assertTrue(spy.calledWithMatch("a", b="e"))       #it's a combination
        self.assertFalse(spy.calledWithMatch("d", "e", c="c")) #it's a combination
        sinon.g.C_func(c="f")
        self.assertTrue(spy.calledWithMatch("a", "b", c="f")) #it's a combination but called

    @sinontest
    def test210_calledWith_Match_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.calledWith(SinonMatcher(str)))
        self.assertFalse(spy.calledWith(SinonMatcher(str), SinonMatcher(int)))
        self.assertTrue(spy.calledWith(SinonMatcher(str), SinonMatcher(str)))
        self.assertTrue(spy.calledWith(SinonMatcher(str), SinonMatcher(str), "c"))

    @sinontest
    def test213_calledWith_Match_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.calledWith(a=SinonMatcher(str)))
        self.assertFalse(spy.calledWith(a=SinonMatcher(str), b=SinonMatcher(int)))
        self.assertTrue(spy.calledWith(a=SinonMatcher(str), b=SinonMatcher(str)))
        self.assertTrue(spy.calledWith(a=SinonMatcher(str), b=SinonMatcher(str), c="c"))

    @sinontest
    def test216_calledWith_Match_combination(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", c="c")
        self.assertTrue(spy.calledWith(SinonMatcher(str)))
        self.assertFalse(spy.calledWith(SinonMatcher(str), SinonMatcher(int)))
        self.assertFalse(spy.calledWith(SinonMatcher(str), b=SinonMatcher(str)))
        self.assertTrue(spy.calledWith(SinonMatcher(str), SinonMatcher(str), c="c"))

    @sinontest
    def test219_calledWithMatch_exception(self):
        spy = SinonSpy(C_func)
        with self.assertRaises(Exception) as context:
            spy.calledWithMatch()

    @sinontest
    def test220_alwaysCalledWithMatch_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWithMatch("a"))
        self.assertTrue(spy.alwaysCalledWithMatch("a", "b"))
        self.assertTrue(spy.alwaysCalledWithMatch("a", "b", "c"))
        self.assertFalse(spy.alwaysCalledWithMatch("a", "b", "c", "d"))
        self.assertFalse(spy.alwaysCalledWithMatch("a", "c"))
        self.assertTrue(spy.alwaysCalledWithMatch(str))
        self.assertFalse(spy.alwaysCalledWithMatch(str, int))
        self.assertTrue(spy.alwaysCalledWithMatch(str, str))
        self.assertTrue(spy.alwaysCalledWithMatch(str, str, str))
        sinon.g.C_func("d", "e")
        self.assertFalse(spy.alwaysCalledWithMatch("a", "b"))
        self.assertFalse(spy.alwaysCalledWithMatch("d", "e"))
        self.assertFalse(spy.alwaysCalledWithMatch("a", "e"))
        self.assertFalse(spy.alwaysCalledWithMatch("d", "e", "c")) #it's a combination

    @sinontest
    def test221_alwaysCalledWith_matcher(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.alwaysCalledWith(str))
        self.assertTrue(spy.alwaysCalledWith(SinonMatcher(str)))

    @sinontest
    def test223_alwaysCalledWithMatch_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithMatch(a="a"))
        self.assertTrue(spy.alwaysCalledWithMatch(a="a", b="b"))
        self.assertFalse(spy.alwaysCalledWithMatch(a="d", b="e"))
        self.assertTrue(spy.alwaysCalledWithMatch(a="a", b="b", c="c"))
        self.assertTrue(spy.alwaysCalledWithMatch(a="a", c="c")) # dict is not rely on order of arguments
        self.assertTrue(spy.alwaysCalledWithMatch(a=str))
        self.assertFalse(spy.alwaysCalledWithMatch(a=str, b=int))
        self.assertTrue(spy.alwaysCalledWithMatch(a=str, b=str))
        self.assertTrue(spy.alwaysCalledWithMatch(a=str, b=str, c=str))
        sinon.g.C_func(a="d", b="e")
        self.assertFalse(spy.alwaysCalledWithMatch(a="a", b="b"))
        self.assertFalse(spy.alwaysCalledWithMatch(a="d", b="e"))
        self.assertFalse(spy.alwaysCalledWithMatch(a="a", b="e"))
        self.assertFalse(spy.alwaysCalledWithMatch(a="d", b="e", c="c")) #it's a combination

    @sinontest
    def test226_alwaysCalledWithMatch_combination(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", c="c")
        self.assertTrue(spy.alwaysCalledWithMatch("a"))
        self.assertTrue(spy.alwaysCalledWithMatch("a", "b"))
        self.assertFalse(spy.alwaysCalledWithMatch("d", "e"))
        self.assertTrue(spy.alwaysCalledWithMatch("a", "b", c="c"))
        self.assertTrue(spy.alwaysCalledWithMatch("a", c="c")) # dict is not rely on order of arguments
        self.assertTrue(spy.alwaysCalledWithMatch(str))
        self.assertFalse(spy.alwaysCalledWithMatch(str, int))
        self.assertTrue(spy.alwaysCalledWithMatch(str, str))
        self.assertTrue(spy.alwaysCalledWithMatch(str, str, c=str))
        sinon.g.C_func("d", b="e")
        self.assertFalse(spy.alwaysCalledWithMatch("a", b="b"))
        self.assertFalse(spy.alwaysCalledWithMatch("d", b="e"))
        self.assertFalse(spy.alwaysCalledWithMatch("a", b="e"))       #it's a combination
        self.assertFalse(spy.alwaysCalledWithMatch("d", "e", c="c")) #it's a combination
        sinon.g.C_func(c="f")
        self.assertFalse(spy.alwaysCalledWithMatch("a", "b", c="f")) #it's a combination but called

    @sinontest
    def test229_alwaysCalledWithMatch_exception(self):
        spy = SinonSpy(C_func)
        with self.assertRaises(Exception) as context:
            spy.alwaysCalledWithMatch()

    @sinontest
    def test230_alwaysCalledWith_Match_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWith(SinonMatcher(str)))
        self.assertFalse(spy.alwaysCalledWith(SinonMatcher(str), SinonMatcher(int)))
        self.assertTrue(spy.alwaysCalledWith(SinonMatcher(str), SinonMatcher(str)))
        self.assertTrue(spy.alwaysCalledWith(SinonMatcher(str), SinonMatcher(str), "c"))

    @sinontest
    def test233_alwaysCalledWith_Match_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith(a=SinonMatcher(str)))
        self.assertFalse(spy.alwaysCalledWith(a=SinonMatcher(str), b=SinonMatcher(int)))
        self.assertTrue(spy.alwaysCalledWith(a=SinonMatcher(str), b=SinonMatcher(str)))
        self.assertTrue(spy.alwaysCalledWith(a=SinonMatcher(str), b=SinonMatcher(str), c="c"))

    @sinontest
    def test236_alwaysCalledWith_Match_combination(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", c="c")
        self.assertTrue(spy.alwaysCalledWith(SinonMatcher(str)))
        self.assertFalse(spy.alwaysCalledWith(SinonMatcher(str), SinonMatcher(int)))
        self.assertFalse(spy.alwaysCalledWith(SinonMatcher(str), b=SinonMatcher(str)))
        self.assertTrue(spy.alwaysCalledWith(SinonMatcher(str), SinonMatcher(str), c="c"))

    @sinontest
    def test240_neverCalledWithMatch_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.neverCalledWithMatch("a"))
        self.assertFalse(spy.neverCalledWithMatch("a", "b"))
        self.assertFalse(spy.neverCalledWithMatch("a", "b", "c"))
        self.assertTrue(spy.neverCalledWithMatch("a", "b", "c", "d"))
        self.assertTrue(spy.neverCalledWithMatch("a", "c"))
        self.assertFalse(spy.neverCalledWithMatch(str))
        self.assertTrue(spy.neverCalledWithMatch(str, int))
        self.assertFalse(spy.neverCalledWithMatch(str, str))
        self.assertFalse(spy.neverCalledWithMatch(str, str, str))
        sinon.g.C_func("d", "e")
        self.assertFalse(spy.neverCalledWithMatch("a", "b"))
        self.assertFalse(spy.neverCalledWithMatch("d", "e"))
        self.assertTrue(spy.neverCalledWithMatch("a", "e"))
        self.assertTrue(spy.neverCalledWithMatch("d", "e", "c")) #it's a combination

    @sinontest
    def test250_firstCall_to_lastCall_with_call(self):
        spy = SinonSpy(E_func)
        sinon.g.E_func(1, 2)
        sinon.g.E_func(3, 4)
        sinon.g.E_func(5, 6)
        sinon.g.E_func(7, 8)
        self.assertEqual(type(spy.firstCall).__name__, "SpyCall")
        self.assertEqual(spy.firstCall.args, (1, 2))
        self.assertEqual(type(spy.secondCall).__name__, "SpyCall")
        self.assertEqual(spy.secondCall.args, (3, 4))
        self.assertEqual(type(spy.thirdCall).__name__, "SpyCall")
        self.assertEqual(spy.thirdCall.args, (5, 6))
        self.assertEqual(type(spy.lastCall).__name__, "SpyCall")
        self.assertEqual(spy.lastCall.args, (7, 8))

    @sinontest
    def test251_firstCall_to_lastCall_without_call(self):
        spy = SinonSpy(C_func)
        self.assertEqual(spy.firstCall, None)
        self.assertEqual(spy.secondCall, None)
        self.assertEqual(spy.thirdCall, None)
        self.assertEqual(spy.lastCall, None)

    @sinontest
    def test260_getCall(self):
        spy = SinonSpy(E_func)
        sinon.g.E_func(1, 2, a=1)
        sinon.g.E_func(3, 4, b=2)
        sinon.g.E_func(5, 6, c=3)

        call0 = spy.getCall(0)
        self.assertTupleEqual(call0.args, (1,2))
        self.assertDictEqual(call0.kwargs, {'a':1})
        self.assertEqual(call0.callId, 0)
        self.assertEqual(call0.exception, None)
        self.assertEqual(call0.proxy, spy)
        self.assertEqual(call0.returnValue, "(1, 2) {'a': 1}")
        self.assertEqual(type(call0.stack), type([]))

        call1 = spy.getCall(1)
        self.assertTupleEqual(call1.args, (3,4))
        self.assertDictEqual(call1.kwargs, {'b':2})
        self.assertEqual(call1.callId, 1)
        self.assertEqual(call1.exception, None)
        self.assertEqual(call1.proxy, spy)
        self.assertEqual(call1.returnValue, "(3, 4) {'b': 2}")
        self.assertEqual(type(call1.stack), type([]))

        call2 = spy.getCall(2)
        self.assertTupleEqual(call2.args, (5,6))
        self.assertDictEqual(call2.kwargs, {'c':3})
        self.assertEqual(call2.callId, 2)
        self.assertEqual(call2.exception, None)
        self.assertEqual(call2.proxy, spy)
        self.assertEqual(call2.returnValue, "(5, 6) {'c': 3}")
        self.assertEqual(type(call2.stack), type([]))

    @sinontest
    def test261_getCall_exception(self):
        spy = SinonSpy(D_func)
        exception = BaseException()
        try:
            sinon.g.D_func(exception)
        except BaseException as e:
            call = spy.getCall(0)
            self.assertTupleEqual(call.args, (exception,))
            self.assertDictEqual(call.kwargs, {})
            self.assertEqual(call.callId, 0)
            self.assertEqual(exception, e)
            self.assertEqual(call.exception, exception)
            self.assertEqual(call.proxy, spy)
            self.assertEqual(call.returnValue, None)
            self.assertEqual(type(call.stack), type([]))
        else:
            self.assertTrue(False, "Failed to catch exception")

    @sinontest
    def test261_getCall_multipleSpies(self):
        spy1 = SinonSpy(C_func)
        spy2 = SinonSpy(E_func)
        sinon.g.C_func(1, 2, 3)
        sinon.g.E_func(4, 5, 6)
        self.assertTupleEqual(spy1.getCall(0).args, (1, 2, 3))
        self.assertListEqual(spy1.args, [(1, 2, 3)])
        self.assertTupleEqual(spy2.getCall(0).args, (4, 5, 6))
        self.assertListEqual(spy2.args, [(4, 5, 6)])
        self.assertEqual(spy1.getCall(1), None)
        self.assertEqual(spy2.getCall(1), None)

    @sinontest
    def test270_args_and_kwargs(self):
        spy = SinonSpy(E_func)
        sinon.g.E_func()
        self.assertListEqual(spy.args, [()])
        self.assertListEqual(spy.kwargs, [{}])
        sinon.g.E_func(1, a=1)
        self.assertListEqual(spy.args, [(), (1,)])
        self.assertListEqual(spy.kwargs, [{}, {'a':1}])
        sinon.g.E_func(1, 2, a=1, b=2)
        self.assertListEqual(spy.args, [(), (1,), (1,2)])
        self.assertListEqual(spy.kwargs, [{}, {'a':1}, {'a':1,'b':2}])
