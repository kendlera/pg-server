# Power Grid Core Data Files

# powerplants.json - Defines all power plant cards in the game
```json
[{"generators": 6, "market_cost": 44, "resource_cost": 0, "resource_type": 5, "type": "light"}, ...]
```

# map.edgelist - Defines city connections and costs
```
Sofia Bucuresti 9
Zurich Milano 11
Minsk Kharkiv 16
...
```

# city_colors.json - Defines regions
```json
{
    "green": ["Warszawa", "Minsk", "Moskwa", "Kharkiv", "Kyjiv", "Odessa", "Bucuresti"],
    "orange": ["Riga", "Tallinn", "Sankt-Peterburg", "Helsinki", "Stockholm", "Oslo", "Kobenhavn"],
    ...
}
```

# resource_slots.json - Market setup
```json
[{"0": 3, "1": 2, "2": 4, "3": 1}, ...]
```

# replenish_rates.json - Resource replenishment rules
```json
{"europe": {"2": {"2": {"1": 2, "2": 6, "3": 2}, ...}}}
```

# payoff.json - Money earned for powering cities
```json
{"money": [10,22,33,44,54,64,73,82,90,98,105,112,118,124,129,134,138,142,145,148,150]}
```