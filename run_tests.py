import unittest

import lexer.tests

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(lexer.tests)
    
    runner = unittest.TextTestRunner()
    runner.run(suite)