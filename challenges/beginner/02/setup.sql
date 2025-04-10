-- Create pokemon table with sample data
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    cp INTEGER NOT NULL,
    first_caught DATE NOT NULL
);

-- Insert sample data
INSERT INTO
    pokemon (name, type, region, cp, first_caught)
VALUES
    ('Pikachu', 'Electric', 'Kanto', 950, '2016-07-09'),
    ('Bulbasaur', 'Grass', 'Kanto', 905, '2016-07-14'),
    ('Squirtle', 'Water', 'Kanto', 851, '2016-08-13'),
    ('Charizard', 'Fire', 'Kanto', 1600, '2016-08-13'),
    ('Jigglypuff', 'Fairy', 'Kanto', 681, '2016-09-13'),
    ('Gengar', 'Ghost', 'Kanto', 1206, '2016-10-21'),
    (
        'Machamp',
        'Fighting',
        'Kanto',
        1480,
        '2017-01-21'
    ),
    ('Gyarados', 'Water', 'Kanto', 1751, '2017-02-09'),
    ('Mewtwo', 'Psychic', 'Kanto', 2300, '2017-07-21'),
    (
        'Dragonite',
        'Dragon',
        'Kanto',
        1851,
        '2017-04-21'
    );
