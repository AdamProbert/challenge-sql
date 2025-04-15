-- Setup for beginner challenge #6 on LIKE pattern matching
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL
);

-- Insert Pokemon with specific name patterns
INSERT INTO
    pokemon (name, type, region, cp)
VALUES
    -- Names ending with "chu"
    ('Pikachu', 'Electric', 'Kanto', 950),
    ('Raichu', 'Electric', 'Kanto', 1450),
    ('Pichu', 'Electric', 'Johto', 350),
    -- Names containing "saur"
    ('Bulbasaur', 'Grass', 'Kanto', 780),
    ('Ivysaur', 'Grass', 'Kanto', 1050),
    ('Venusaur', 'Grass', 'Kanto', 1320),
    -- Other common Pokemon
    ('Charmander', 'Fire', 'Kanto', 850),
    ('Charmeleon', 'Fire', 'Kanto', 1100),
    ('Charizard', 'Fire', 'Kanto', 1550),
    ('Squirtle', 'Water', 'Kanto', 820),
    ('Wartortle', 'Water', 'Kanto', 1050),
    ('Blastoise', 'Water', 'Kanto', 1680),
    ('Caterpie', 'Bug', 'Kanto', 310),
    ('Metapod', 'Bug', 'Kanto', 340),
    ('Butterfree', 'Bug', 'Kanto', 900),
    ('Weedle', 'Bug', 'Kanto', 320),
    ('Kakuna', 'Bug', 'Kanto', 350),
    ('Beedrill', 'Bug', 'Kanto', 910),
    ('Pidgey', 'Flying', 'Kanto', 380),
    ('Rattata', 'Normal', 'Kanto', 320);
