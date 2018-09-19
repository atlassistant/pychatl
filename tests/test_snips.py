import unittest
from pychatl import parse
from pychatl.postprocess.snips import snips, is_builtin_entity

class SnipsTests(unittest.TestCase):

  def test_is_builtin_entity(self):
    self.assertTrue(is_builtin_entity('snips/datetime'))
    self.assertFalse(is_builtin_entity('some_entity'))
    self.assertFalse(is_builtin_entity(None))

  def test_process_intents(self):
    result = parse("""
%[get_forecast]
  will it rain in @[city] on @[date]
  ~[greet] what's the weather like in @[city#variant]

@[city]
  paris
  rouen

@[city#variant]
  new york
  los angeles

@[date](snips:type=snips/datetime)
  tomorrow

~[greet]
  hi
  hello

""")

    snips_data = snips(result)

    self.assertEqual(1, len(snips_data['intents']))
    self.assertTrue('get_forecast' in snips_data['intents'])

    intent = snips_data['intents']['get_forecast']

    self.assertTrue('utterances' in intent)

    utterances = intent['utterances']

    self.assertEqual(3, len(utterances))

    data = utterances[0].get('data')

    self.assertEqual(4, len(data))
    self.assertEqual('will it rain in ', data[0].get('text'))
    self.assertEqual('paris', data[1].get('text'))
    self.assertEqual('city', data[1].get('slot_name'))
    self.assertEqual('city', data[1].get('entity'))
    self.assertEqual(' on ', data[2].get('text'))
    self.assertEqual('tomorrow', data[3].get('text'))
    self.assertEqual('date', data[3].get('slot_name'))
    self.assertEqual('snips/datetime', data[3].get('entity'))

    data = utterances[1].get('data')

    self.assertEqual(3, len(data))
    self.assertEqual('hi', data[0].get('text'))
    self.assertEqual(" what's the weather like in ", data[1].get('text'))
    self.assertEqual('new york', data[2].get('text'))

    data = utterances[2].get('data')

    self.assertEqual(3, len(data))
    self.assertEqual('hello', data[0].get('text'))
    self.assertEqual(" what's the weather like in ", data[1].get('text'))
    self.assertEqual('los angeles', data[2].get('text'))

  def test_process_entities(self):
    result = parse("""
@[city]
  paris
  rouen
  ~[new york]

@[room](extensible=false)
  kitchen
  bedroom

@[date](snips:type=snips/datetime)
  tomorrow
  on tuesday

~[new york]
  nyc
  the big apple
""")

    snips_data = snips(result)

    self.assertEqual(3, len(snips_data['entities']))
    self.assertTrue('city' in snips_data['entities'])

    entity = snips_data['entities']['city']

    self.assertTrue(entity['use_synonyms'])
    self.assertTrue(entity['automatically_extensible'])
    self.assertEqual(3, len(entity['data']))
    self.assertEqual('new york', entity['data'][2]['value'])
    self.assertEqual(2, len(entity['data'][2]['synonyms']))
    self.assertEqual(['nyc', 'the big apple'], entity['data'][2]['synonyms'])

    self.assertTrue('room' in snips_data['entities'])
    entity = snips_data['entities']['room']
    self.assertFalse(entity['use_synonyms'])
    self.assertFalse(entity['automatically_extensible'])
    self.assertEqual(2, len(entity['data']))

    self.assertFalse('date' in snips_data['entities'])
    self.assertTrue('snips/datetime' in snips_data['entities'])
    self.assertEqual({}, snips_data['entities']['snips/datetime'])

  def test_process_entities_with_variants(self):
    result = parse("""
@[city]
  paris
  rouen
  ~[new york]

@[city#variant]
  one variant
  another one

~[new york]
  nyc
  the big apple
""")

    snips_data = snips(result)

    self.assertEqual(1, len(snips_data['entities']))
    self.assertTrue('city' in snips_data['entities'])

    entity = snips_data['entities']['city']

    self.assertEqual(5, len(entity['data']))

    data = [ d.get('value') for d in entity['data'] ]

    self.assertEqual(['paris', 'rouen', 'new york', 'one variant', 'another one'], data)

  def test_process_options(self):
    result = parse("""
@[city]
  paris
  rouen
""")

    snips_data = snips(result)

    self.assertEqual('en', snips_data.get('language'))

    snips_data = snips(result, language='fr')

    self.assertEqual('fr', snips_data.get('language'))
