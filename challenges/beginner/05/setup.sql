-- Setup for beginner challenge #5 on LIMIT and OFFSET
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL,
    level INTEGER NOT NULL
);

-- Insert Pokemon sample data with varied CP values
INSERT INTO
    pokemon (name, type, region, cp, level)
VALUES
    ('Mewtwo', 'Psychic', 'Kanto', 2540, 40),
    ('Dragonite', 'Dragon', 'Kanto', 2420, 38),
    ('Mew', 'Psychic', 'Kanto', 2350, 39),
    ('Snorlax', 'Normal', 'Kanto', 2250, 36),
    ('Tyranitar', 'Rock', 'Johto', 2190, 35),
    ('Gyarados', 'Water', 'Kanto', 1780, 32),
    ('Blastoise', 'Water', 'Kanto', 1680, 31),
    ('Arcanine', 'Fire', 'Kanto', 1650, 30),
    ('Alakazam', 'Psychic', 'Kanto', 1650, 30),
    ('Lapras', 'Water', 'Kanto', 1320, 25),
    ('Venusaur', 'Grass', 'Kanto', 1320, 25),
    ('Charizard', 'Fire', 'Kanto', 1550, 29),
    ('Machamp', 'Fighting', 'Kanto', 1470, 28),
    ('Raichu', 'Electric', 'Kanto', 1450, 27),
    ('Vaporeon', 'Water', 'Kanto', 1620, 30),
    ('Jolteon', 'Electric', 'Kanto', 1570, 29),
    ('Flareon', 'Fire', 'Kanto', 1510, 28),
    ('Gengar', 'Ghost', 'Kanto', 1210, 23),
    ('Exeggutor', 'Grass', 'Kanto', 1420, 26),
    ('Rhydon', 'Ground', 'Kanto', 1350, 25);
