-- Setup for first beginner challenge
-- Create pokemon table with sample data
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cp DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- Insert sample data
INSERT INTO
    pokemon (name, cp, type, region)
VALUES
    ('Pikachu', 950.50, 'Electric', 'Kanto'),
    ('Charizard', 1599.99, 'Fire', 'Kanto'),
    ('Squirtle', 850.75, 'Water', 'Kanto'),
    ('Bulbasaur', 905.25, 'Grass', 'Kanto'),
    ('Jigglypuff', 680.50, 'Fairy', 'Kanto'),
    ('Gyarados', 1750.99, 'Water', 'Kanto'),
    ('Mewtwo', 2299.99, 'Psychic', 'Kanto'),
    ('Gengar', 1205.50, 'Ghost', 'Kanto'),
    ('Dragonite', 1850.75, 'Dragon', 'Kanto'),
    ('Snorlax', 1680.25, 'Normal', 'Kanto');
