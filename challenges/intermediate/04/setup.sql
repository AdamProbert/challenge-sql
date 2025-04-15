-- Setup for intermediate challenge #4 on HAVING clause
-- Create pokemon table with varied types and CP values
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- Insert pokemon data with various types and CP values
INSERT INTO
    pokemon (name, type, cp, region)
VALUES
    -- Water type (8 Pokemon)
    ('Squirtle', 'Water', 900, 'Kanto'),
    ('Wartortle', 'Water', 1350, 'Kanto'),
    ('Blastoise', 'Water', 2100, 'Kanto'),
    ('Psyduck', 'Water', 850, 'Kanto'),
    ('Golduck', 'Water', 1600, 'Kanto'),
    ('Poliwag', 'Water', 650, 'Kanto'),
    ('Poliwhirl', 'Water', 1200, 'Kanto'),
    ('Poliwrath', 'Water', 1950, 'Kanto'),
    -- Fire type (7 Pokemon)
    ('Charmander', 'Fire', 950, 'Kanto'),
    ('Charmeleon', 'Fire', 1400, 'Kanto'),
    ('Charizard', 'Fire', 2150, 'Kanto'),
    ('Vulpix', 'Fire', 800, 'Kanto'),
    ('Ninetales', 'Fire', 1650, 'Kanto'),
    ('Growlithe', 'Fire', 850, 'Kanto'),
    ('Arcanine', 'Fire', 1950, 'Kanto'),
    -- Electric type (6 Pokemon)
    ('Pikachu', 'Electric', 950, 'Kanto'),
    ('Raichu', 'Electric', 1800, 'Kanto'),
    ('Magnemite', 'Electric', 750, 'Kanto'),
    ('Magneton', 'Electric', 1450, 'Kanto'),
    ('Voltorb', 'Electric', 850, 'Kanto'),
    ('Electrode', 'Electric', 1500, 'Kanto'),
    -- Grass type (5 Pokemon)
    ('Bulbasaur', 'Grass', 850, 'Kanto'),
    ('Ivysaur', 'Grass', 1300, 'Kanto'),
    ('Venusaur', 'Grass', 2000, 'Kanto'),
    ('Oddish', 'Grass', 700, 'Kanto'),
    ('Gloom', 'Grass', 1250, 'Kanto'),
    -- Psychic type (5 Pokemon)
    ('Abra', 'Psychic', 600, 'Kanto'),
    ('Kadabra', 'Psychic', 1100, 'Kanto'),
    ('Alakazam', 'Psychic', 1950, 'Kanto'),
    ('Mewtwo', 'Psychic', 3000, 'Kanto'),
    ('Mew', 'Psychic', 2600, 'Kanto'),
    -- Fighting type (4 Pokemon)
    ('Mankey', 'Fighting', 750, 'Kanto'),
    ('Primeape', 'Fighting', 1550, 'Kanto'),
    ('Machop', 'Fighting', 900, 'Kanto'),
    ('Machamp', 'Fighting', 2050, 'Kanto'),
    -- Rock type (4 Pokemon)
    ('Geodude', 'Rock', 700, 'Kanto'),
    ('Graveler', 'Rock', 1200, 'Kanto'),
    ('Golem', 'Rock', 1800, 'Kanto'),
    ('Onix', 'Rock', 1600, 'Kanto'),
    -- Normal type (3 Pokemon)
    ('Jigglypuff', 'Normal', 750, 'Kanto'),
    ('Wigglytuff', 'Normal', 1400, 'Kanto'),
    ('Snorlax', 'Normal', 2200, 'Kanto'),
    -- Poison type (3 Pokemon)
    ('Ekans', 'Poison', 600, 'Kanto'),
    ('Arbok', 'Poison', 1300, 'Kanto'),
    ('Muk', 'Poison', 1700, 'Kanto'),
    -- Ground type (3 Pokemon)
    ('Sandshrew', 'Ground', 700, 'Kanto'),
    ('Sandslash', 'Ground', 1450, 'Kanto'),
    ('Diglett', 'Ground', 500, 'Kanto'),
    -- Dragon type (3 Pokemon, high average CP)
    ('Dratini', 'Dragon', 900, 'Kanto'),
    ('Dragonair', 'Dragon', 1600, 'Kanto'),
    ('Dragonite', 'Dragon', 2800, 'Kanto'),
    -- Flying type (2 Pokemon)
    ('Pidgey', 'Flying', 400, 'Kanto'),
    ('Pidgeot', 'Flying', 1500, 'Kanto'),
    -- Bug type (2 Pokemon)
    ('Caterpie', 'Bug', 300, 'Kanto'),
    ('Butterfree', 'Bug', 1200, 'Kanto'),
    -- Ghost type (2 Pokemon, high average but only 2)
    ('Gastly', 'Ghost', 750, 'Kanto'),
    ('Gengar', 'Ghost', 1850, 'Kanto'),
    -- Ice type (1 Pokemon)
    ('Articuno', 'Ice', 2700, 'Kanto'),
    -- Fairy type (1 Pokemon)
    ('Clefairy', 'Fairy', 800, 'Kanto');
