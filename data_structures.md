# Power Grid Server Data Structures

This document contains the core data structures that define the Power Grid game mechanics, including the actual data used.

## 1. Power Plant Cards (powerplants.json)
Each power plant defines its capabilities and cost:
```json
{
    "generators": 1,        // How many cities it can power
    "market_cost": 3,       // Cost to buy (also serves as plant ID)
    "resource_cost": 2,     // Resources needed to operate
    "resource_type": 2,     // OIL=1, COAL=0, GAS=2, URANIUM=3, HYBRID=4, CLEAN=5
    "type": "dark"         // Card type (affects game phases)
}
```

## 2. Game Map (map.edgelist)
Defines city connections and their costs:
```
# Format: city1 city2 connection_cost
Sofia Bucuresti 9
Zurich Milano 11
Minsk Kharkiv 16
// ... many more connections
```
This creates a graph where:
- Cities are nodes
- Connections are edges
- Numbers are the connection costs
- Players must build along these connections

## 3. City Regions (city_colors.json)
Groups cities into regions for game setup:
```json
{
    "green": ["Warszawa", "Minsk", "Moskwa", "Kharkiv", "Kyjiv", "Odessa", "Bucuresti"],
    "orange": ["Riga", "Tallinn", "Sankt-Peterburg", "Helsinki", "Stockholm", "Oslo", "Kobenhavn"],
    "brown": ["Bremen", "Berlin", "Praha", "Katowice", "Munchen", "Rhein-Main", "Stuttgart"],
    // ... more regions
}
```
Game uses different numbers of regions based on player count:
- 3 players: 3 regions
- 4 players: 4 regions
- 5 players: 5 regions
- 6 players: 5 regions (remove one random region)

## 4. Resource Market Setup (resource_slots.json)
Defines how resources are organized in the market:
```json
[
    {
        "0": 3,  // COAL amount
        "1": 2,  // OIL amount
        "2": 4,  // GAS amount
        "3": 1   // URANIUM amount
    },
    // ... more price slots
]
```
Key features:
- Each entry represents a price level
- First entry is most expensive
- Players must buy highest priced resources first
- Market replenishes from highest price down

## 5. Resource Replenishment (replenish_rates.json)
Controls how resources are added each turn:
```json
{
  "europe": {
    "2": {  // 2 players
      "2": {  // GAS
        "1": 2,  // Phase 1: add 2
        "2": 6,  // Phase 2: add 6
        "3": 2   // Phase 3: add 2
      },
      // ... other resources
    },
    // ... other player counts
  }
}
```
- Different rates for player count
- Different rates per game phase
- Separate rates for Europe/USA maps

## 6. Power Plant Payoff Table (payoff.json)
How much money players get for powering cities:
```json
{
  "money": [10,22,33,44,54,64,73,82,90,98,105,112,118,124,129,134,138,142,145,148,150]
}
```
- Index = number of cities powered
- Value = money earned

## Important Game Rules

1. Turn Structure:
   - Auction power plants
   - Buy resources
   - Build generators
   - Power cities/earn money

2. Building Rules:
   - Must build connected to existing network
   - First city can be anywhere
   - Cities get more expensive as more players build

3. Resource Rules:
   - Must buy highest priced resources first
   - Hybrid plants can use either oil or gas
   - Resources stored on specific plants
   - Must use exact resource amounts

4. Game Progression:
   - Step 2 starts when someone builds 7th city (6 players: 6th city)
   - Step 3 shuffled in when deck depleted
   - Game ends after step 3 when someone builds:
     - 3-4 players: 17 cities
     - 5 players: 15 cities
     - 6 players: 14 cities