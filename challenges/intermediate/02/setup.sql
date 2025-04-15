-- Setup for intermediate challenge #2 on LEFT JOIN
-- Create trainers table
CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hometown VARCHAR(100) NOT NULL,
    badges INTEGER NOT NULL DEFAULT 0
);

-- Create pokemon table with foreign key to trainers
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL,
    trainer_id INTEGER REFERENCES trainers (trainer_id)
);

-- Insert trainer data
INSERT INTO
    trainers (name, hometown, badges)
VALUES
    ('Ash Ketchum', 'Pallet Town', 8),
    ('Misty', 'Cerulean City', 5),
    ('Brock', 'Pewter City', 7),
    ('Gary Oak', 'Pallet Town', 10),
    ('May', 'Petalburg City', 4),
    ('Dawn', 'Twinleaf Town', 5),
    ('Serena', 'Vaniville Town', 3),
    ('Clemont', 'Lumiose City', 6);

-- Insert pokemon data - mix of captured and wild Pokemon
INSERT INTO
    pokemon (name, type, cp, trainer_id)
VALUES
    -- Ash's Pokemon
    ('Pikachu', 'Electric', 1500, 1),
    ('Charizard', 'Fire', 2100, 1),
    ('Squirtle', 'Water', 1200, 1),
    ('Bulbasaur', 'Grass', 1250, 1),
    ('Pidgeotto', 'Flying', 1100, 1),
    -- Misty's Pokemon
    ('Starmie', 'Water', 1650, 2),
    ('Goldeen', 'Water', 950, 2),
    ('Psyduck', 'Water', 1050, 2),
    ('Gyarados', 'Water', 1900, 2),
    -- Brock's Pokemon
    ('Onix', 'Rock', 1800, 3),
    ('Geodude', 'Rock', 1100, 3),
    ('Vulpix', 'Fire', 1200, 3),
    ('Zubat', 'Poison', 900, 3),
    -- Gary's Pokemon
    ('Blastoise', 'Water', 2000, 4),
    ('Umbreon', 'Dark', 1750, 4),
    ('Electivire', 'Electric', 1850, 4),
    ('Arcanine', 'Fire', 1950, 4),
    ('Nidoking', 'Poison', 1800, 4),
    -- Wild Pokemon (no trainer)
    ('Mewtwo', 'Psychic', 3000, NULL),
    ('Articuno', 'Ice', 2700, NULL),
    ('Zapdos', 'Electric', 2750, NULL),
    ('Moltres', 'Fire', 2800, NULL),
    ('Dragonite', 'Dragon', 2650, NULL),
    ('Snorlax', 'Normal', 2500, NULL),
    ('Lapras', 'Water', 2300, NULL),
    ('Venusaur', 'Grass', 2200, NULL),
    ('Machamp', 'Fighting', 2150, NULL),
    ('Gengar', 'Ghost', 2250, NULL),
    ('Alakazam', 'Psychic', 2100, NULL),
    ('Tauros', 'Normal', 1950, NULL),
    ('Ditto', 'Normal', 1000, NULL),
    ('Abra', 'Psychic', 1200, NULL),
    ('Eevee', 'Normal', 1100, NULL);
