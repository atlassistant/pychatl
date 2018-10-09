from sure import expect
from pychatl.utils import deep_update

class TestUtils:

  def test_it_should_be_able_to_deep_update_a_dict(self):
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

    expect(result['language']).to.equal('fr')
    expect(result['entities']['room']['automatically_extensible']).to.be.false
    expect(result['entities']['room']['data']).to.have.length_of(1)