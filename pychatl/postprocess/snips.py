from itertools import product
from ..utils import deep_update

def is_builtin_entity(name):
  """Checks if the given entity name is a builtin one.

  Args:
    name (str): Name of the entity
  
  Returns:
    bool: True if it's one, false otherwise

  """

  if name:
    return name.startswith('snips/')
  
  return False

def snips(dataset, **options):

  entities_idx = {}

  entities = dataset.get('entities', {})
  intents = dataset.get('intents', {})
  synonyms = dataset.get('synonyms', {})

  def get_entity_or_variant_value(entity, variant):
    key = entity + (variant or '')

    d = entities.get(entity, {}).get('data', [])

    if variant:
      d = entities.get(entity, {}).get('variants', {}).get(variant, [])

    if key not in entities_idx or entities_idx[key] >= (len(d) - 1):
      entities_idx[key] = 0
    else:
      entities_idx[key] += 1
    
    return d[entities_idx[key]].get('value')

  def get_sentence_value(raw_data):
    t = raw_data.get('type', 'text')
    v = raw_data.get('value')

    if t == 'text':
      return { 
        'text': v,
      }
    elif t == 'entity':
      return {
        'text': get_entity_or_variant_value(v, raw_data.get('variant')),
        'slot_name': v,
        'entity': entities.get(v, {}).get('props', {}).get('snips:type', v),
      }

    return {}

  training_dataset = {
    'language': 'en',
    'intents': {},
    'entities': {},
  }

  # Process entities first
  
  for (name, entity) in entities.items():
    # Here we flatten the variants data
    variants_value = list(entity.get('variants', {}).values())
    variants_data = [item for sublist in variants_value for item in sublist]

    entity_data = entity.get('data', []) + variants_data
    props = entity.get('props', {})
    prop_type = props.get('snips:type')

    if is_builtin_entity(prop_type):
      training_dataset['entities'][prop_type] = {}
    else:
      data = []
      use_synonyms = False

      for d in entity_data:
        t = d.get('type', 'text')
        v = d.get('value')

        if t == 'text':
          data.append({
            'value': v,
            'synonyms': [],
          })
        elif t == 'synonym':
          synonyms = dataset.get('synonyms', {}).get(v, {}).get('data', [])
          use_synonyms = True

          data.append({
            'value': v,
            'synonyms': [s.get('value') for s in synonyms],
          })

      training_dataset['entities'][name] = {
        'data': data,
        'use_synonyms': use_synonyms,
        'automatically_extensible': (props.get('extensible', 'true') == 'true'),
      }

  # And then intents
  # For intents, we need to generate all permutations for synonyms

  for (name, intent) in intents.items():
    intent_data = intent.get('data', [])
    utterances = []

    for sentence in intent_data:
      synonyms_in_sentence = list(filter(lambda d: d.get('type') == 'synonym', sentence))

      if len(synonyms_in_sentence) > 0:
        synonym_values = [[d.get('value') for d in synonyms.get(s.get('value'), {}).get('data', [])] for s in synonyms_in_sentence]
        
        permutations = product(*synonym_values)

        for permutation in permutations:
          cur_sentence = []
          permut_idx = 0

          for data in sentence:
            if data.get('type') == 'synonym':
              data = {
                'type' : 'text',
                'value': permutation[permut_idx],
              }

              permut_idx += 1
            
            cur_sentence.append(get_sentence_value(data))
          
          utterances.append({
            'data': cur_sentence,
          })
            
      else:
        utterances.append({
          'data': [ get_sentence_value(d) for d in sentence ],
        })
    
    training_dataset['intents'][name] = {
      'utterances': utterances,
    }

  return deep_update(training_dataset, options)