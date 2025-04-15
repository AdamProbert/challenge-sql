-- Setup for beginner challenge #3 on AND, OR, NOT
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL,
    first_caught DATE NOT NULL
);

-- Insert diverse Pokemon sample data
INSERT INTO
    pokemon (name, type, region, cp, first_caught)
VALUES
    ('Pikachu', 'Electric', 'Kanto', 950, '2016-07-09'),
    ('Raichu', 'Electric', 'Kanto', 1450, '2016-08-10'),
    ('Squirtle', 'Water', 'Kanto', 820, '2016-07-10'),
    ('Blastoise', 'Water', 'Kanto', 1680, '2016-09-15'),
    ('Bulbasaur', 'Grass', 'Kanto', 780, '2016-07-10'),
    ('Venusaur', 'Grass', 'Kanto', 1320, '2016-10-05'),
    ('Charmander', 'Fire', 'Kanto', 850, '2016-07-10'),
    ('Charizard', 'Fire', 'Kanto', 1550, '2016-09-25'),
    ('Jigglypuff', 'Fairy', 'Kanto', 670, '2016-08-05'),
    ('Gengar', 'Ghost', 'Kanto', 1210, '2016-10-31'),
    ('Gyarados', 'Water', 'Kanto', 1780, '2016-12-25'),
    ('Lapras', 'Water', 'Kanto', 1320, '2017-01-20'),
    ('Vaporeon', 'Water', 'Kanto', 1620, '2017-01-05'),
    (
        'Jolteon',
        'Electric',
        'Kanto',
        1570,
        '2017-01-12'
    ),
    ('Mewtwo', 'Psychic', 'Kanto', 2540, '2017-07-22');
