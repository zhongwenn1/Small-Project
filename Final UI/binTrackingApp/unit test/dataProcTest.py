import unittest
from dataProc import DataProc
import pandas as pd

class DataProcTest(unittest.TestCase):

    def test_open_file(self):
        self.assertRaises(TypeError,DataProc)

    def test_get_df(self):
        df = pd.DataFrame([10,20,30],columns=['Beam Diff'])
        dp = DataProc(None)
        output = dp.get_df(df,10,20)
        new_df = pd.DataFrame([10,20],columns=['Beam Diff'])
        self.assertTrue(new_df.equals(output))

if __name__ == '__main__':
    unittest.main(verbosity=2)