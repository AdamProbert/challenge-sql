-- Setup for advanced subquery & aggregation challenge
-- Create a more detailed Pokemon database
CREATE TABLE pokemon_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL,
    effective_against VARCHAR(100)
);

CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    pokedex_number INTEGER NOT NULL UNIQUE,
    type_id INTEGER REFERENCES pokemon_types (type_id),
    secondary_type_id INTEGER REFERENCES pokemon_types (type_id),
    cp DECIMAL(10, 2) NOT NULL,
    caught_date DATE NOT NULL
);

-- Insert type data
INSERT INTO
    pokemon_types (type_name, effective_against)
VALUES
    ('Fire', 'Grass, Ice, Bug, Steel'),
    ('Water', 'Fire, Ground, Rock'),
    ('Grass', 'Water, Ground, Rock'),
    ('Electric', 'Water, Flying'),
    ('Psychic', 'Fighting, Poison'),
    ('Ice', 'Grass, Ground, Flying, Dragon'),
    ('Dragon', 'Dragon'),
    ('Fairy', 'Fighting, Dragon, Dark'),
    ('Fighting', 'Normal, Ice, Rock, Dark, Steel'),
    ('Flying', 'Grass, Fighting, Bug');

-- Insert pokemon data with varied CP
INSERT INTO
    pokemon (
        name,
        pokedex_number,
        type_id,
        secondary_type_id,
        cp,
        caught_date
    )
VALUES
    -- Fire types
    ('Charmander', 4, 1, NULL, 615.00, '2021-06-15'),
    ('Charizard', 6, 1, 10, 1515.00, '2020-04-20'),
    ('Vulpix', 37, 1, NULL, 420.00, '2022-01-10'),
    ('Arcanine', 59, 1, NULL, 1781.00, '2019-10-05'),
    ('Rapidash', 78, 1, NULL, 1245.00, '2020-03-22'),
    ('Flareon', 136, 1, NULL, 1230.00, '2021-02-15'),
    -- Water types
    ('Squirtle', 7, 2, NULL, 602.00, '2021-07-12'),
    ('Blastoise', 9, 2, NULL, 1392.00, '2020-05-03'),
    ('Psyduck', 54, 2, NULL, 487.00, '2022-01-20'),
    ('Poliwrath', 62, 2, 9, 1340.00, '2021-06-10'),
    -- Grass types
    ('Bulbasaur', 1, 3, NULL, 627.00, '2021-08-10'),
    ('Venusaur', 3, 3, NULL, 1467.00, '2020-11-05'),
    ('Exeggutor', 103, 3, 5, 1429.00, '2019-09-15'),
    ('Tangela', 114, 3, NULL, 972.00, '2020-07-22'),
    ('Vileplume', 45, 3, NULL, 1402.00, '2020-10-18'),
    -- Electric types
    ('Pikachu', 25, 4, NULL, 827.00, '2019-03-01'),
    ('Raichu', 26, 4, NULL, 1439.00, '2020-06-08'),
    ('Electabuzz', 125, 4, NULL, 1395.00, '2021-05-15'),
    -- Psychic types
    ('Abra', 63, 5, NULL, 417.00, '2022-05-20'),
    ('Alakazam', 65, 5, NULL, 1813.00, '2019-09-12'),
    ('Mewtwo', 150, 5, NULL, 2784.00, '2019-02-28'),
    ('Mew', 151, 5, NULL, 1754.00, '2020-08-03'),
    ('Hypno', 97, 5, NULL, 1109.00, '2020-08-15'),
    ('Mr. Mime', 122, 5, 8, 1163.00, '2020-10-05'),
    -- Dragon types
    ('Dratini', 147, 7, NULL, 528.00, '2021-04-15'),
    ('Dragonair', 148, 7, NULL, 1024.00, '2020-09-10'),
    ('Dragonite', 149, 7, 10, 2107.00, '2019-01-25'),
    ('Gyarados', 130, 2, 10, 2046.00, '2020-03-18');
