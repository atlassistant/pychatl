import unittest
from pychatl import parse

class ParserTests(unittest.TestCase):

  def test_parse_intents(self):
    result = parse("""
%[get_forecast](some=prop, something=else)
  will it rain in @[city]
  ~[greet] what's the weather like in @[city#variant]
""")

    self.assertEqual(1, len(result['intents']))
    self.assertTrue('get_forecast' in result['intents'])

    intent = result['intents']['get_forecast']

    self.assertEqual(2, len(intent['props']))
    self.assertTrue('some' in intent['props'])
    self.assertTrue('something' in intent['props'])
    self.assertEqual('prop', intent['props']['some'])
    self.assertEqual('else', intent['props']['something'])

    self.assertEqual(2, len(intent['data']))

    data = intent['data'][0]

    self.assertEqual(2, len(data))
    self.assertEqual('text', data[0]['type'])
    self.assertEqual('will it rain in ', data[0]['value'])

    self.assertEqual('entity', data[1]['type'])
    self.assertEqual('city', data[1]['value'])
    self.assertIsNone(data[1]['variant'])

    data = intent['data'][1]

    self.assertEqual(3, len(data))
    self.assertEqual('synonym', data[0]['type'])
    self.assertEqual('greet', data[0]['value'])

    self.assertEqual('text', data[1]['type'])
    self.assertEqual(" what's the weather like in ", data[1]['value'])   

    self.assertEqual('entity', data[2]['type'])
    self.assertEqual('city', data[2]['value'])
    self.assertEqual('variant', data[2]['variant'])

  def test_parse_entities(self):
    result = parse("""
@[city](some=prop, something=else)
  paris
  rouen
  ~[new york]
""")

    self.assertEqual(1, len(result['entities']))
    self.assertTrue('city' in result['entities'])

    entity = result['entities']['city']

    self.assertEqual(2, len(entity['props']))
    self.assertTrue('some' in entity['props'])
    self.assertTrue('something' in entity['props'])
    self.assertEqual('prop', entity['props']['some'])
    self.assertEqual('else', entity['props']['something'])

    data = entity['data']

    self.assertEqual(3, len(data))

    self.assertEqual('text', data[0]['type'])
    self.assertEqual('paris', data[0]['value'])

    self.assertEqual('text', data[1]['type'])
    self.assertEqual('rouen', data[1]['value'])

    self.assertEqual('synonym', data[2]['type'])
    self.assertEqual('new york', data[2]['value'])

  def test_parse_entities_variants(self):
    result = parse("""
@[city](some=prop, something=else)
  paris
  rouen
  ~[new york]

@[city#variant](var=prop)
  one variant
  another one
""")

    self.assertEqual(1, len(result['entities']))

    entity = result['entities']['city']

    self.assertEqual(1, len(entity['variants']))
    self.assertTrue('variant' in entity['variants'])
    self.assertEqual(3, len(entity['props']))
    self.assertTrue('some' in entity['props'])
    self.assertTrue('something' in entity['props'])
    self.assertTrue('var' in entity['props'])

    variant = entity['variants']['variant']

    self.assertEqual(2, len(variant))

    self.assertEqual('text', variant[0]['type'])
    self.assertEqual('one variant', variant[0]['value'])

    self.assertEqual('text', variant[1]['type'])
    self.assertEqual('another one', variant[1]['value'])

  def test_parse_synonyms(self):
    result = parse("""
~[new york](some=prop, something=else)
  nyc
  the big apple
""")

    self.assertEqual(1, len(result['synonyms']))
    self.assertTrue('new york' in result['synonyms'])

    synonym = result['synonyms']['new york']

    self.assertEqual(2, len(synonym['props']))
    self.assertTrue('some' in synonym['props'])
    self.assertTrue('something' in synonym['props'])
    self.assertEqual('prop', synonym['props']['some'])
    self.assertEqual('else', synonym['props']['something'])

    self.assertEqual(2, len(synonym['data']))

    data = synonym['data']

    self.assertEqual('text', data[0]['type'])
    self.assertEqual('nyc', data[0]['value'])

    self.assertEqual('text', data[1]['type'])
    self.assertEqual('the big apple', data[1]['value'])

  def test_parse_comments(self):
    result = parse("""
# chatl is really easy to understand.
#
# You can defines:
#   - Intents
#   - Entities (with or without variants)
#   - Synonyms
#   - Comments (only at the top level)

# Inside an intent, you got training data.
# Training data can refer to one or more entities and/or synonyms, they will be used
# by generators to generate all possible permutations and training samples.

%[my_intent]
  ~[greet] some training data @[date]
  another training data that uses an @[entity] at @[date#with_variant]

~[greet]
  hi
  hello

# Entities contains available samples and could refer to a synonym.

@[entity]
  some value
  other value
  ~[a synonym]

# Synonyms contains only raw values

~[a synonym]
  possible synonym
  another one

# Entities and intents can define arbitrary properties that will be made available
# to generators.
# For snips, `type` and `extensible` are used for example.

@[date](type=snips/datetime)
  tomorrow
  today

# Variants is used only to generate training sample with specific values that should
# maps to the same entity name, here `date`. Props will be merged with the root entity.

@[date#with_variant]
  the end of the day
  nine o clock
  twenty past five
""")

    self.assertEqual(1, len(result['intents']))
    self.assertEqual(2, len(result['entities']))
    self.assertEqual(2, len(result['synonyms']))