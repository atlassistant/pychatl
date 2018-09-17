pychatl |travis| |pypi| |license|
=================================

.. |travis| image:: https://travis-ci.org/atlassistant/pychatl.svg?branch=master
    :target: https://travis-ci.org/atlassistant/pychatl

.. |pypi| image:: https://badge.fury.io/py/pychatl.svg
    :target: https://badge.fury.io/py/pychatl

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0

Tiny DSL to generate training dataset for NLU engines. Based on the javascript implementation of `chatl <https://github.com/atlassistant/chatl>`_.

Installation
------------

pip
~~~

.. code-block:: bash

  $ pip install pychatl

source
~~~~~~

.. code-block:: bash

  $ git clone https://github.com/atlassistant/pychatl.git
  $ cd pychatl
  $ python setup.py install

or

.. code-block:: bash

  $ pip install -e .

Usage
-----

From the terminal
~~~~~~~~~~~~~~~~~

.. code-block:: bash

  $ pychatl .\example\forecast.dsl .\example\lights.dsl -a snips -o '{ \"language\": \"en\" }'

From the code
~~~~~~~~~~~~~

.. code-block:: python

  from pychatl import parse

  result = parse("""
  # pychatl is really easy to understand.
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

Testing
-------

.. code-block:: bash

  $ cd tests/
  $ python -m unittest -v
