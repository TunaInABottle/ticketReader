import unittest
import id_generator

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_id_generator(self):
        self.assertEqual(id_generator.next_id("cr0001"), "cr0002")
        self.assertEqual(id_generator.next_id("parar0301"), "parar0302")
        
        with self.assertRaises(ValueError):
            id_generator.next_id("0parar0301")

if __name__ == '__main__':
    unittest.main()