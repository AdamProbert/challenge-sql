-- Setup for intermediate challenge #5 on joining multiple tables for evolution chains
-- Evolution methods table
CREATE TABLE evolution_methods (
    method_id SERIAL PRIMARY KEY,
    method_name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Insert evolution methods
INSERT INTO
    evolution_methods (method_name, description)
VALUES
    ('Level', 'Evolves when reaching a specific level'),
    (
        'Stone',
        'Evolves when exposed to an evolutionary stone'
    ),
    ('Trade', 'Evolves when traded to another trainer'),
    (
        'Happiness',
        'Evolves when happiness reaches a high level'
    ),
    (
        'Item Held',
        'Evolves when leveling up while holding a specific item'
    ),
    (
        'Move Known',
        'Evolves when leveling up while knowing a specific move'
    ),
    (
        'Location',
        'Evolves when leveling up in a specific location'
    );

-- Evolution chains table
CREATE TABLE evolution_chains (
    evolution_chain_id SERIAL PRIMARY KEY,
    basic_form_id INTEGER NOT NULL,
    middle_form_id INTEGER,
    final_form_id INTEGER,
    basic_to_middle_method INTEGER REFERENCES evolution_methods (method_id),
    middle_to_final_method INTEGER REFERENCES evolution_methods (method_id),
    evolution_requirement VARCHAR(100),
    evolution_requirement2 VARCHAR(100)
);

-- Pokemon species table
CREATE TABLE pokemon_species (
    species_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    evolution_stage INTEGER NOT NULL, -- 1=basic, 2=middle, 3=final
    evolution_chain_id INTEGER REFERENCES evolution_chains (evolution_chain_id)
);

-- Insert Pokemon species data
INSERT INTO
    pokemon_species (name, type, evolution_stage, evolution_chain_id)
VALUES
    -- Bulbasaur family
    ('Bulbasaur', 'Grass', 1, 1),
    ('Ivysaur', 'Grass', 2, 1),
    ('Venusaur', 'Grass', 3, 1),
    -- Charmander family
    ('Charmander', 'Fire', 1, 2),
    ('Charmeleon', 'Fire', 2, 2),
    ('Charizard', 'Fire', 3, 2),
    -- Squirtle family
    ('Squirtle', 'Water', 1, 3),
    ('Wartortle', 'Water', 2, 3),
    ('Blastoise', 'Water', 3, 3),
    -- Caterpie family
    ('Caterpie', 'Bug', 1, 4),
    ('Metapod', 'Bug', 2, 4),
    ('Butterfree', 'Bug', 3, 4),
    -- Weedle family
    ('Weedle', 'Bug', 1, 5),
    ('Kakuna', 'Bug', 2, 5),
    ('Beedrill', 'Bug', 3, 5),
    -- Pidgey family
    ('Pidgey', 'Flying', 1, 6),
    ('Pidgeotto', 'Flying', 2, 6),
    ('Pidgeot', 'Flying', 3, 6),
    -- Rattata family (2-stage)
    ('Rattata', 'Normal', 1, 7),
    ('Raticate', 'Normal', 3, 7),
    -- Pikachu family (modified to show 3-stage)
    ('Pichu', 'Electric', 1, 8),
    ('Pikachu', 'Electric', 2, 8),
    ('Raichu', 'Electric', 3, 8),
    -- Abra family
    ('Abra', 'Psychic', 1, 9),
    ('Kadabra', 'Psychic', 2, 9),
    ('Alakazam', 'Psychic', 3, 9),
    -- Machop family
    ('Machop', 'Fighting', 1, 10),
    ('Machoke', 'Fighting', 2, 10),
    ('Machamp', 'Fighting', 3, 10),
    -- Geodude family
    ('Geodude', 'Rock', 1, 11),
    ('Graveler', 'Rock', 2, 11),
    ('Golem', 'Rock', 3, 11),
    -- Gastly family
    ('Gastly', 'Ghost', 1, 12),
    ('Haunter', 'Ghost', 2, 12),
    ('Gengar', 'Ghost', 3, 12),
    -- Dratini family
    ('Dratini', 'Dragon', 1, 13),
    ('Dragonair', 'Dragon', 2, 13),
    ('Dragonite', 'Dragon', 3, 13);

-- Insert evolution chain data
INSERT INTO
    evolution_chains (
        evolution_chain_id,
        basic_form_id,
        middle_form_id,
        final_form_id,
        basic_to_middle_method,
        middle_to_final_method,
        evolution_requirement,
        evolution_requirement2
    )
VALUES
    (1, 1, 2, 3, 1, 1, 'Level 16', 'Level 32'),
    (2, 4, 5, 6, 1, 1, 'Level 16', 'Level 36'),
    (3, 7, 8, 9, 1, 1, 'Level 16', 'Level 36'),
    (4, 10, 11, 12, 1, 1, 'Level 7', 'Level 10'),
    (5, 13, 14, 15, 1, 1, 'Level 7', 'Level 10'),
    (6, 16, 17, 18, 1, 1, 'Level 18', 'Level 36'),
    (7, 19, NULL, 20, 1, NULL, 'Level 20', NULL),
    (
        8,
        22,
        23,
        24,
        4,
        2,
        'High Happiness',
        'Thunder Stone'
    ),
    (9, 25, 26, 27, 1, 3, 'Level 16', 'Trade'),
    (10, 28, 29, 30, 1, 3, 'Level 28', 'Trade'),
    (11, 31, 32, 33, 1, 3, 'Level 25', 'Trade'),
    (12, 34, 35, 36, 1, 3, 'Level 25', 'Trade'),
    (13, 37, 38, 39, 1, 1, 'Level 30', 'Level 55');

-- Update the pokemon_species table with foreign keys to match evolution_chains
UPDATE pokemon_species
SET
    species_id = name_id
FROM
    (
        VALUES
            ('Bulbasaur', 1),
            ('Ivysaur', 2),
            ('Venusaur', 3),
            ('Charmander', 4),
            ('Charmeleon', 5),
            ('Charizard', 6),
            ('Squirtle', 7),
            ('Wartortle', 8),
            ('Blastoise', 9),
            ('Caterpie', 10),
            ('Metapod', 11),
            ('Butterfree', 12),
            ('Weedle', 13),
            ('Kakuna', 14),
            ('Beedrill', 15),
            ('Pidgey', 16),
            ('Pidgeotto', 17),
            ('Pidgeot', 18),
            ('Rattata', 19),
            ('Raticate', 20),
            ('Pichu', 22),
            ('Pikachu', 23),
            ('Raichu', 24),
            ('Abra', 25),
            ('Kadabra', 26),
            ('Alakazam', 27),
            ('Machop', 28),
            ('Machoke', 29),
            ('Machamp', 30),
            ('Geodude', 31),
            ('Graveler', 32),
            ('Golem', 33),
            ('Gastly', 34),
            ('Haunter', 35),
            ('Gengar', 36),
            ('Dratini', 37),
            ('Dragonair', 38),
            ('Dragonite', 39)
    ) AS name_map (name, name_id)
WHERE
    pokemon_species.name = name_map.name;
