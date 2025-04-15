-- Setup for beginner challenge #4 on ORDER BY
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL
);

-- Insert diverse Pokemon sample data with varied CP within types
INSERT INTO
    pokemon (name, type, region, cp)
VALUES
    -- Electric types
    ('Pikachu', 'Electric', 'Kanto', 950),
    ('Raichu', 'Electric', 'Kanto', 1450),
    ('Electabuzz', 'Electric', 'Kanto', 1250),
    ('Jolteon', 'Electric', 'Kanto', 1570),
    -- Water types
    ('Squirtle', 'Water', 'Kanto', 820),
    ('Blastoise', 'Water', 'Kanto', 1680),
    ('Gyarados', 'Water', 'Kanto', 1780),
    ('Vaporeon', 'Water', 'Kanto', 1620),
    ('Lapras', 'Water', 'Kanto', 1320),
    -- Fire types
    ('Charmander', 'Fire', 'Kanto', 850),
    ('Charizard', 'Fire', 'Kanto', 1550),
    ('Arcanine', 'Fire', 'Kanto', 1650),
    ('Flareon', 'Fire', 'Kanto', 1510),
    -- Grass types
    ('Bulbasaur', 'Grass', 'Kanto', 780),
    ('Venusaur', 'Grass', 'Kanto', 1320),
    ('Vileplume', 'Grass', 'Kanto', 1220),
    ('Victreebel', 'Grass', 'Kanto', 1230),
    -- Psychic types
    ('Abra', 'Psychic', 'Kanto', 850),
    ('Alakazam', 'Psychic', 'Kanto', 1650),
    ('Mewtwo', 'Psychic', 'Kanto', 2540),
    ('Mew', 'Psychic', 'Kanto', 2100);
