-- Setup for beginner challenge #8 on NULL values
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    evolution_level INTEGER,
    evolution_stone VARCHAR(50)
);

-- Insert Pokemon with some NULL values for evolution data
INSERT INTO
    pokemon (
        name,
        type,
        region,
        evolution_level,
        evolution_stone
    )
VALUES
    -- Pokemon with NULL evolution_level
    ('Eevee', 'Normal', 'Kanto', NULL, 'Water Stone'),
    ('Gloom', 'Grass', 'Kanto', NULL, 'Leaf Stone'),
    (
        'Poliwhirl',
        'Water',
        'Kanto',
        NULL,
        'Water Stone'
    ),
    ('Vulpix', 'Fire', 'Kanto', NULL, 'Fire Stone'),
    ('Shellder', 'Water', 'Kanto', NULL, 'Water Stone'),
    ('Exeggcute', 'Grass', 'Kanto', NULL, 'Leaf Stone'),
    -- Pokemon with NULL evolution_stone
    ('Pikachu', 'Electric', 'Kanto', 25, NULL),
    ('Pidgey', 'Flying', 'Kanto', 18, NULL),
    ('Rattata', 'Normal', 'Kanto', 20, NULL),
    ('Spearow', 'Flying', 'Kanto', 20, NULL),
    ('Sandshrew', 'Ground', 'Kanto', 22, NULL),
    ('Nidoran♀', 'Poison', 'Kanto', 16, NULL),
    ('Nidorina', 'Poison', 'Kanto', 32, NULL),
    ('Nidoran♂', 'Poison', 'Kanto', 16, NULL),
    ('Nidorino', 'Poison', 'Kanto', 32, NULL),
    ('Zubat', 'Poison', 'Kanto', 22, NULL),
    ('Golbat', 'Poison', 'Kanto', 25, NULL),
    -- Pokemon with both values known
    ('Bulbasaur', 'Grass', 'Kanto', 16, NULL),
    ('Ivysaur', 'Grass', 'Kanto', 32, NULL),
    ('Charmander', 'Fire', 'Kanto', 16, NULL),
    ('Charmeleon', 'Fire', 'Kanto', 36, NULL),
    ('Squirtle', 'Water', 'Kanto', 16, NULL),
    ('Wartortle', 'Water', 'Kanto', 36, NULL),
    ('Caterpie', 'Bug', 'Kanto', 7, NULL),
    ('Metapod', 'Bug', 'Kanto', 10, NULL),
    ('Weedle', 'Bug', 'Kanto', 7, NULL),
    ('Kakuna', 'Bug', 'Kanto', 10, NULL),
    ('Jigglypuff', 'Fairy', 'Kanto', 30, NULL),
    -- Pokemon with neither value (non-evolving)
    ('Farfetch''d', 'Flying', 'Kanto', NULL, NULL),
    ('Kangaskhan', 'Normal', 'Kanto', NULL, NULL),
    ('Pinsir', 'Bug', 'Kanto', NULL, NULL),
    ('Tauros', 'Normal', 'Kanto', NULL, NULL),
    ('Ditto', 'Normal', 'Kanto', NULL, NULL),
    ('Aerodactyl', 'Rock', 'Kanto', NULL, NULL),
    ('Articuno', 'Ice', 'Kanto', NULL, NULL),
    ('Zapdos', 'Electric', 'Kanto', NULL, NULL),
    ('Moltres', 'Fire', 'Kanto', NULL, NULL),
    ('Mewtwo', 'Psychic', 'Kanto', NULL, NULL),
    ('Mew', 'Psychic', 'Kanto', NULL, NULL);
