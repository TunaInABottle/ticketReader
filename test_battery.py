import unittest
import id_generator
import Entry

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_id_generator(self):
        self.assertEqual(id_generator.next_id("cr0001"), "cr0002")
        self.assertEqual(id_generator.next_id("parar0301"), "parar0302")
        
        with self.assertRaises(ValueError):
            id_generator.next_id("0parar0301")

    def test_entry_extract_price(self):
        self.assertEqual(Entry.Entry('ACETO B. DI ALCOOL xVI 0,69').price, 0.69)
        self.assertEqual(Entry.Entry('CAROTE VASSOIO *VI 0.99').price, 0.99)
        self.assertEqual(Entry.Entry('Scanto % Bollone -2,50').price, -2.50)
        self.assertEqual(Entry.Entry('CECI V/VERDE BIO xVI 099').price, 0.99)
        self.assertEqual(Entry.Entry('Sconto Articolo 0 99').price, 0.99)
        self.assertEqual(Entry.Entry('Sconto Articolo -0 24').price, -0.24)
        print(Entry.Entry('Sconto Articolo -0 24').product)


if __name__ == '__main__':
    unittest.main()

