%[get_forecast]
  will it be sunny in @[location] at @[date#at]
  what's the weather like in @[location] on @[date#on]
  will it rain in @[location] @[date]
  what kind of weather should I expect at @[date#at] in @[location]
  what will be the weather on @[date#on] in @[location]
  tell me if it is going to rain @[date] in @[location]
  will it rain in @[location] and @[location] @[date]

~[los angeles]
  la

@[date](snips:type=snips/datetime)
  tomorrow
  today
  this evening

@[date#at]
  the end of the day
  nine o'clock

@[date#on]
  tuesday
  monday

@[location]
  ~[los angeles]
  paris
  rio de janeiro
  tokyo
  london
  tel aviv
  paris