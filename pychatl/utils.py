from collections import Mapping

def deep_update(d, u):
  """Deeply updates a dictionary. List values are not concatenated!

  Args:
    d (dict): First dictionary
    u (dict): Second dictionary

  Returns:
    dict: The merge dictionary

  """

  for k, v in u.items():
    if isinstance(v, Mapping):
      d[k] = deep_update(d.get(k, {}), v)
    else:
      d[k] = v

  return d