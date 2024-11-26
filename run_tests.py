import unittest

import lexer.tests

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    
    testes_lexer = unittest.defaultTestLoader.loadTestsFromModule(lexer.tests)
    
    runner.run(testes_lexer)