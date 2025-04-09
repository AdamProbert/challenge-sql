-- Setup for second beginner challenge (WHERE clause)
-- Create mario_characters table with sample data
CREATE TABLE mario_characters (
    character_id SERIAL PRIMARY KEY,
    character_name VARCHAR(50) NOT NULL,
    species VARCHAR(50) NOT NULL,
    kingdom VARCHAR(50) NOT NULL,
    power_level INTEGER NOT NULL,
    first_appearance DATE NOT NULL
);

-- Insert sample data
INSERT INTO
    mario_characters (
        character_name,
        species,
        kingdom,
        power_level,
        first_appearance
    )
VALUES
    (
        'Mario',
        'Human',
        'Mushroom Kingdom',
        95,
        '1981-07-09'
    ),
    (
        'Luigi',
        'Human',
        'Mushroom Kingdom',
        90,
        '1983-06-14'
    ),
    (
        'Princess Peach',
        'Human',
        'Mushroom Kingdom',
        75,
        '1985-09-13'
    ),
    ('Bowser', 'Koopa', 'Dark Land', 100, '1985-09-13'),
    (
        'Toad',
        'Mushroom',
        'Mushroom Kingdom',
        60,
        '1985-09-13'
    ),
    (
        'Yoshi',
        'Dinosaur',
        'Mushroom Kingdom',
        85,
        '1990-04-21'
    ),
    (
        'Wario',
        'Human',
        'Diamond City',
        88,
        '1992-01-21'
    ),
    (
        'Donkey Kong',
        'Gorilla',
        'DK Island',
        92,
        '1981-07-09'
    ),
    (
        'Waluigi',
        'Human',
        'Mushroom Kingdom',
        70,
        '2000-07-21'
    ),
    (
        'Princess Daisy',
        'Human',
        'Sarasaland',
        75,
        '1989-04-21'
    );
