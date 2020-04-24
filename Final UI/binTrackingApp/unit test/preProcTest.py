import unittest
from preProc import PreProc


class PreProcTest(unittest.TestCase):

    def test(self):
        self.assertRaises(TypeError, PreProc)

if __name__ == '__main__':
    unittest.main(verbosity=2)
