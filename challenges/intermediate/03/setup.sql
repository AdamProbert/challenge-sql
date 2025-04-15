-- Setup for intermediate challenge #3 on aggregation
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
    ('Clemont', 'Lumiose City', 6),
    ('Iris', 'Opelucid City', 4),
    ('Cilan', 'Striaton City', 3),
    ('Bonnie', 'Lumiose City', 1),
    ('Max', 'Petalburg City', 0),
    ('Tracey Sketchit', 'Orange Islands', 2),
    ('Nurse Joy', 'Various Cities', 0),
    ('Officer Jenny', 'Various Cities', 0);

-- Insert pokemon data with trainer relationships
INSERT INTO
    pokemon (name, type, cp, trainer_id)
VALUES
    -- Ash's Pokemon (6)
    ('Pikachu', 'Electric', 1500, 1),
    ('Charizard', 'Fire', 2100, 1),
    ('Squirtle', 'Water', 1200, 1),
    ('Bulbasaur', 'Grass', 1250, 1),
    ('Pidgeotto', 'Flying', 1100, 1),
    ('Greninja', 'Water', 1900, 1),
    -- Misty's Pokemon (4)
    ('Starmie', 'Water', 1650, 2),
    ('Goldeen', 'Water', 950, 2),
    ('Psyduck', 'Water', 1050, 2),
    ('Gyarados', 'Water', 1900, 2),
    -- Brock's Pokemon (4)
    ('Onix', 'Rock', 1800, 3),
    ('Geodude', 'Rock', 1100, 3),
    ('Vulpix', 'Fire', 1200, 3),
    ('Zubat', 'Poison', 900, 3),
    -- Gary's Pokemon (5)
    ('Blastoise', 'Water', 2000, 4),
    ('Umbreon', 'Dark', 1750, 4),
    ('Electivire', 'Electric', 1850, 4),
    ('Arcanine', 'Fire', 1950, 4),
    ('Nidoking', 'Poison', 1800, 4),
    -- May's Pokemon (3)
    ('Blaziken', 'Fire', 1850, 5),
    ('Beautifly', 'Bug', 1100, 5),
    ('Skitty', 'Normal', 950, 5),
    -- Dawn's Pokemon (3)
    ('Piplup', 'Water', 1200, 6),
    ('Buneary', 'Normal', 1050, 6),
    ('Pachirisu', 'Electric', 1150, 6),
    -- Serena's Pokemon (3)
    ('Braixen', 'Fire', 1350, 7),
    ('Pancham', 'Fighting', 1200, 7),
    ('Sylveon', 'Fairy', 1450, 7),
    -- Clemont's Pokemon (3)
    ('Luxray', 'Electric', 1550, 8),
    ('Chespin', 'Grass', 1200, 8),
    ('Bunnelby', 'Normal', 950, 8),
    -- Iris's Pokemon (2)
    ('Axew', 'Dragon', 1100, 9),
    ('Excadrill', 'Ground', 1800, 9),
    -- Cilan's Pokemon (2)
    ('Pansage', 'Grass', 1250, 10),
    ('Stunfisk', 'Ground', 1300, 10),
    -- Bonnie's Pokemon (1)
    ('Dedenne', 'Electric', 850, 11),
    -- Max has no Pokemon (0)
    -- Tracey's Pokemon (2)
    ('Scyther', 'Bug', 1700, 13),
    ('Marill', 'Water', 950, 13),
    -- Nurse Joy's Pokemon (2)
    ('Chansey', 'Normal', 1400, 14),
    ('Blissey', 'Normal', 1600, 14),
    -- Officer Jenny's Pokemon (2)
    ('Growlithe', 'Fire', 1100, 15),
    ('Arcanine', 'Fire', 1950, 15),
    -- Wild Pokemon (no trainer)
    ('Mewtwo', 'Psychic', 3000, NULL),
    ('Articuno', 'Ice', 2700, NULL),
    ('Zapdos', 'Electric', 2750, NULL);
