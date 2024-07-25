import sys
sys.path.insert(0, '../')

import unittest
import sinon.base as sinon
from sinon.spy import SinonSpy
from sinon.stub import SinonStub
from sinon.sandbox import sinontest

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

from test.test_Class import ForTestOnly

"""
======================================================
FOR TEST ONLY END
======================================================
"""



class TestSinonSandbox(unittest.TestCase):

    def setUp(self):
        sinon.init(globals())

    @classmethod
    @sinontest
    def _spy_in_sinontest(self):
        base1 = SinonSpy(ForTestOnly)
        base2 = SinonSpy(D_func)
        base3 = SinonSpy(A_object)

    @classmethod
    @sinontest
    def _stub_in_sinontest(self):
        base1 = SinonStub(ForTestOnly)
        base2 = SinonStub(D_func)
        base3 = SinonStub(A_object)

    def test001_test_spy_in_sinontest(self):
        base = SinonSpy()
        self.assertEqual(len(base._queue), 1)
        TestSinonSandbox._spy_in_sinontest()
        self.assertEqual(len(base._queue), 1)
        base.restore()

    def test002_test_stub_in_sinontest(self):
        base = SinonStub()
        self.assertEqual(len(base._queue), 1)
        TestSinonSandbox._stub_in_sinontest()
        self.assertEqual(len(base._queue), 1)
        base.restore()
