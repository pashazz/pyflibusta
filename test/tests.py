'''
Tests for flibusta
'''
import unittest, os
from flibusta import catalog

class FlibustaTest(unittest.TestCase):
    

    def test_findFile(self):
        '''check if findFile works'''
        id = '249564'
        directory = ('/home/pasha/media/books/Флибуста')
        t = catalog.findFile(id, directory)
        self.assertTrue(os.path.exists(t[0]))
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
