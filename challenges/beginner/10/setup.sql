-- Setup for beginner challenge #10 on column aliases
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    hp INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    speed INTEGER NOT NULL
);

-- Insert Pokemon with varied stats
INSERT INTO
    pokemon (name, type, hp, attack, defense, speed)
VALUES
    ('Mewtwo', 'Psychic', 106, 110, 90, 130),
    ('Dragonite', 'Dragon', 91, 134, 95, 80),
    ('Snorlax', 'Normal', 160, 110, 65, 30),
    ('Gyarados', 'Water', 95, 125, 79, 81),
    ('Alakazam', 'Psychic', 55, 50, 45, 120),
    ('Arcanine', 'Fire', 90, 110, 80, 95),
    ('Lapras', 'Water', 130, 85, 80, 60),
    ('Exeggutor', 'Grass', 95, 95, 85, 55),
    ('Vaporeon', 'Water', 130, 65, 60, 65),
    ('Jolteon', 'Electric', 65, 65, 60, 130),
    ('Flareon', 'Fire', 65, 130, 60, 65),
    ('Mew', 'Psychic', 100, 100, 100, 100),
    ('Charizard', 'Fire', 78, 84, 78, 100),
    ('Blastoise', 'Water', 79, 83, 100, 78),
    ('Venusaur', 'Grass', 80, 82, 83, 80),
    ('Machamp', 'Fighting', 90, 130, 80, 55),
    ('Golem', 'Rock', 80, 120, 130, 45),
    ('Gengar', 'Ghost', 60, 65, 60, 110),
    ('Rhydon', 'Ground', 105, 130, 120, 40),
    ('Clefable', 'Fairy', 95, 70, 73, 60),
    ('Pikachu', 'Electric', 35, 55, 40, 90),
    ('Raichu', 'Electric', 60, 90, 55, 110),
    ('Slowbro', 'Water', 95, 75, 110, 30),
    ('Magneton', 'Electric', 50, 60, 95, 70),
    ('Muk', 'Poison', 105, 105, 75, 50);
