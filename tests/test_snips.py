from sure import expect
from pychatl import parse
from pychatl.postprocess.snips import snips, is_builtin_entity

class TestSnips:

  def test_it_should_be_able_to_check_builtin_entity(self):
    expect(is_builtin_entity('snips/datetime')).to.be.true
    expect(is_builtin_entity('some_entity')).to.be.false
    expect(is_builtin_entity(None)).to.be.false

  def test_it_should_process_intents(self):
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

    expect(snips_data['intents']).to.have.length_of(1)
    expect(snips_data['intents']).to.have.key('get_forecast')

    intent = snips_data['intents']['get_forecast']

    expect(intent).to.have.key('utterances')

    utterances = intent['utterances']

    expect(utterances).to.have.length_of(3)

    data = utterances[0].get('data')

    expect(data).to.have.length_of(4)
    expect(data[0].get('text')).to.equal('will it rain in ')
    expect(data[1].get('text')).to.equal('paris')
    expect(data[1].get('slot_name')).to.equal('city')
    expect(data[1].get('entity')).to.equal('city')
    expect(data[2].get('text')).to.equal(' on ')
    expect(data[3].get('text')).to.equal('tomorrow')
    expect(data[3].get('slot_name')).to.equal('date')
    expect(data[3].get('entity')).to.equal('snips/datetime')

    data = utterances[1].get('data')

    expect(data).to.have.length_of(3)
    expect(data[0].get('text')).to.equal('hi')
    expect(data[1].get('text')).to.equal(" what's the weather like in ")
    expect(data[2].get('text')).to.equal('new york')
    expect(data[2].get('slot_name')).to.equal('city')
    expect(data[2].get('entity')).to.equal('city')

    data = utterances[2].get('data')

    expect(data).to.have.length_of(3)
    expect(data[0].get('text')).to.equal('hello')
    expect(data[1].get('text')).to.equal(" what's the weather like in ")
    expect(data[2].get('text')).to.equal('los angeles')
    expect(data[2].get('slot_name')).to.equal('city')
    expect(data[2].get('entity')).to.equal('city')
  
  def test_it_should_process_entities(self):
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

    expect(snips_data['entities']).to.have.length_of(3)
    expect(snips_data['entities']).to.have.key('city')

    entity = snips_data['entities']['city']

    expect(entity['use_synonyms']).to.be.true
    expect(entity['automatically_extensible']).to.be.true
    
    expect(entity['data']).to.have.length_of(3)
    expect(entity['data'][0]['value']).to.equal('paris')
    expect(entity['data'][1]['value']).to.equal('rouen')
    expect(entity['data'][2]['value']).to.equal('new york')
    expect(entity['data'][2]['synonyms']).to.have.length_of(2)
    expect(entity['data'][2]['synonyms']).to.equal(['nyc', 'the big apple'])

    expect(snips_data['entities']).to.have.key('room')

    entity = snips_data['entities']['room']

    expect(entity['use_synonyms']).to.be.false
    expect(entity['automatically_extensible']).to.be.false
    
    expect(entity['data']).to.have.length_of(2)
    expect(snips_data['entities']).to_not.have.key('date')
    expect(snips_data['entities']).to.have.key('snips/datetime')

    expect(snips_data['entities']['snips/datetime']).to.be.empty
  
  def test_it_should_process_entities_with_variants(self):
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

    expect(snips_data['entities']).to.have.length_of(1)
    expect(snips_data['entities']).to.have.key('city')

    entity = snips_data['entities']['city']

    expect(entity['data']).to.have.length_of(5)
    expect(entity['use_synonyms']).to.be.true
    expect(entity['automatically_extensible']).to.be.true
    expect(entity['data'][2]['synonyms']).to.have.length_of(2)
    expect(entity['data'][2]['synonyms']).to.equal(['nyc', 'the big apple'])

    data = [ d.get('value') for d in entity['data'] ]

    expect(data).to.equal(['paris', 'rouen', 'new york', 'one variant', 'another one'])

  def test_process_options(self):
    result = parse("""
@[city]
  paris
  rouen
""")

    snips_data = snips(result)

    expect(snips_data.get('language')).to.equal('en')

    snips_data = snips(result, language='fr')

    expect(snips_data.get('language')).to.equal('fr')
