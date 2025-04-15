-- Setup for intermediate challenge #6 on subqueries
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
    ('Lance', 'Blackthorn City', 8),
    ('Cynthia', 'Celestic Town', 8),
    ('Steven Stone', 'Mossdeep City', 8),
    ('Red', 'Pallet Town', 8),
    ('Blue', 'Pallet Town', 7),
    ('Lorelei', 'Four Island', 8),
    ('Bruno', 'Unknown', 8),
    ('Agatha', 'Unknown', 8),
    ('Sabrina', 'Saffron City', 6),
    ('Lt. Surge', 'Vermilion City', 6),
    ('Erika', 'Celadon City', 6);

-- Insert pokemon data with varied CP values
INSERT INTO
    pokemon (name, type, cp, trainer_id)
VALUES
    -- Ash's Pokemon (mix of strong and average)
    ('Pikachu', 'Electric', 1500, 1),
    ('Charizard', 'Fire', 2200, 1),
    ('Squirtle', 'Water', 1100, 1),
    ('Bulbasaur', 'Grass', 1150, 1),
    ('Pidgeot', 'Flying', 1450, 1),
    ('Greninja', 'Water', 1900, 1),
    -- Misty's Pokemon (mostly water, some strong)
    ('Starmie', 'Water', 1750, 2),
    ('Goldeen', 'Water', 950, 2),
    ('Psyduck', 'Water', 1050, 2),
    ('Gyarados', 'Water', 2100, 2),
    -- Brock's Pokemon (mostly rock/ground, average CP)
    ('Onix', 'Rock', 1400, 3),
    ('Geodude', 'Rock', 1000, 3),
    ('Vulpix', 'Fire', 1100, 3),
    ('Zubat', 'Poison', 900, 3),
    -- Gary's Pokemon (strong competitors)
    ('Blastoise', 'Water', 2100, 4),
    ('Umbreon', 'Dark', 1850, 4),
    ('Electivire', 'Electric', 1950, 4),
    ('Arcanine', 'Fire', 2050, 4),
    ('Nidoking', 'Poison', 1900, 4),
    -- Lance's Pokemon (dragon master, very strong)
    ('Dragonite', 'Dragon', 2400, 5),
    ('Gyarados', 'Water', 2150, 5),
    ('Aerodactyl', 'Rock', 1950, 5),
    ('Charizard', 'Fire', 2250, 5),
    ('Dragonair', 'Dragon', 1850, 5),
    -- Cynthia's Pokemon (champion, extremely strong)
    ('Garchomp', 'Dragon', 2600, 6),
    ('Spiritomb', 'Ghost', 2000, 6),
    ('Lucario', 'Fighting', 2200, 6),
    ('Milotic', 'Water', 2100, 6),
    ('Roserade', 'Grass', 1900, 6),
    -- Steven's Pokemon (champion, steel focus, very strong)
    ('Metagross', 'Steel', 2550, 7),
    ('Skarmory', 'Steel', 1950, 7),
    ('Aggron', 'Steel', 2150, 7),
    ('Claydol', 'Ground', 1900, 7),
    ('Cradily', 'Rock', 1850, 7),
    -- Red's Pokemon (legend, extremely strong)
    ('Pikachu', 'Electric', 2300, 8),
    ('Snorlax', 'Normal', 2500, 8),
    ('Venusaur', 'Grass', 2300, 8),
    ('Charizard', 'Fire', 2450, 8),
    ('Blastoise', 'Water', 2350, 8),
    ('Lapras', 'Water', 2200, 8),
    -- Blue's Pokemon (rival, very strong)
    ('Pidgeot', 'Flying', 1950, 9),
    ('Alakazam', 'Psychic', 2050, 9),
    ('Rhydon', 'Ground', 2100, 9),
    ('Gyarados', 'Water', 2150, 9),
    ('Arcanine', 'Fire', 2100, 9),
    -- Elite Four - Lorelei (ice specialist)
    ('Lapras', 'Water', 2150, 10),
    ('Jynx', 'Ice', 1850, 10),
    ('Slowbro', 'Water', 1950, 10),
    ('Cloyster', 'Water', 1900, 10),
    -- Elite Four - Bruno (fighting specialist)
    ('Onix', 'Rock', 1650, 11),
    ('Hitmonchan', 'Fighting', 1900, 11),
    ('Hitmonlee', 'Fighting', 1950, 11),
    ('Machamp', 'Fighting', 2100, 11),
    -- Elite Four - Agatha (ghost specialist)
    ('Gengar', 'Ghost', 2050, 12),
    ('Golbat', 'Poison', 1750, 12),
    ('Haunter', 'Ghost', 1850, 12),
    ('Arbok', 'Poison', 1800, 12),
    -- Gym Leader - Sabrina (psychic)
    ('Kadabra', 'Psychic', 1650, 13),
    ('Alakazam', 'Psychic', 1950, 13),
    ('Mr. Mime', 'Psychic', 1700, 13),
    -- Gym Leader - Lt. Surge (electric)
    ('Raichu', 'Electric', 1750, 14),
    ('Voltorb', 'Electric', 1300, 14),
    ('Electabuzz', 'Electric', 1650, 14),
    -- Gym Leader - Erika (grass)
    ('Vileplume', 'Grass', 1750, 15),
    ('Victreebel', 'Grass', 1700, 15),
    ('Tangela', 'Grass', 1600, 15),
    -- Wild Pokemon (no trainer)
    ('Mewtwo', 'Psychic', 3000, NULL),
    ('Zapdos', 'Electric', 2750, NULL),
    ('Moltres', 'Fire', 2800, NULL),
    ('Articuno', 'Ice', 2700, NULL),
    ('Mew', 'Psychic', 2900, NULL);
