-- Setup for first beginner challenge
-- Create pokemon table with sample data
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cp DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50)
);

-- Insert sample data
INSERT INTO
    pokemon (name, cp, type)
VALUES
    ('Pikachu', 950.50, 'Electric'),
    ('Charizard', 1599.99, 'Fire'),
    ('Squirtle', 850.75, 'Water'),
    ('Bulbasaur', 905.25, 'Grass'),
    ('Jigglypuff', 680.50, 'Fairy'),
    ('Gyarados', 1750.99, 'Water'),
    ('Mewtwo', 2299.99, 'Psychic'),
    ('Gengar', 1205.50, 'Ghost'),
    ('Dragonite', 1850.75, 'Dragon'),
    ('Snorlax', 1680.25, 'Normal');
