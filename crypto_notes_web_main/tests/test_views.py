import unittest
from pyramid import testing
from webtest import TestApp
from crypto_notes_app import main


class TestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        app = TestApp(main({}, **{'__file__': 'development.ini'}))
        response = app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello World!', response.body)


if __name__ == '__main__':
    unittest.main()
