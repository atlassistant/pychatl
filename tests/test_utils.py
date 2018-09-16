import unittest
from pychatl.utils import deep_update

class UtilsTests(unittest.TestCase):

  def test_deep_update(self):
    a = {
      'language': 'en',
      'entities': {
        'room': {
          'data': [
            {
              'value': 'kitchen',
            },
            {
              'value': 'bedroom',
            },
          ],
          'automatically_extensible': True,
        }
      }
    }

    b = {
      'language': 'fr',
      'entities': {
        'room': {
          'data': [
            {
              'value': 'living room',
            },
          ],
          'automatically_extensible': False,
        }
      }
    }

    result = deep_update(a, b)

    self.assertEqual('fr', result['language'])
    self.assertFalse(result['entities']['room']['automatically_extensible'])
    self.assertEqual(1, len(result['entities']['room']['data']))