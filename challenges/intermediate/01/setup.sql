-- Setup for intermediate JOIN challenge
-- Create shops and item_purchases tables with Pokemon-themed sample data
CREATE TABLE shops (
    shop_id SERIAL PRIMARY KEY,
    shop_name VARCHAR(50) NOT NULL,
    shopkeeper VARCHAR(50) NOT NULL,
    location VARCHAR(100) UNIQUE NOT NULL,
    pokecoin_exchange_rate DECIMAL(10, 2),
    established_date DATE NOT NULL
);

CREATE TABLE item_purchases (
    purchase_id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops (shop_id),
    purchase_date DATE NOT NULL,
    pokecoin_amount DECIMAL(10, 2) NOT NULL,
    item_name VARCHAR(50) NOT NULL
);

-- Insert sample shops
INSERT INTO
    shops (
        shop_name,
        shopkeeper,
        location,
        pokecoin_exchange_rate,
        established_date
    )
VALUES
    (
        'Poke Mart',
        'Shop Clerk',
        'Viridian City',
        1.25,
        '2016-02-27'
    ),
    (
        'Berry Shop',
        'Berry Master',
        'Cerulean City',
        1.0,
        '2016-02-27'
    ),
    (
        'Evolution Store',
        'Mr. Stone',
        'Pewter City',
        1.5,
        '2016-02-27'
    ),
    (
        'Battle Items',
        'Fighting Dojo Master',
        'Saffron City',
        0.8,
        '2016-02-27'
    ),
    (
        'Silph Co. Shop',
        'Silph President',
        'Saffron City HQ',
        2.0,
        '2016-02-27'
    );

-- Insert sample item purchases
INSERT INTO
    item_purchases (
        shop_id,
        purchase_date,
        pokecoin_amount,
        item_name
    )
VALUES
    (1, '2023-03-10', 120.00, 'Ultra Ball'),
    (2, '2023-03-12', 80.00, 'Sitrus Berry'),
    (3, '2023-03-15', 40.00, 'Water Stone'),
    (1, '2023-03-20', 200.00, 'Max Revive'),
    (2, '2023-03-25', 50.00, 'Lum Berry'),
    (4, '2023-03-28', 300.00, 'Focus Sash'),
    (5, '2023-04-01', 20.00, 'Poke Ball'),
    (1, '2023-04-05', 85.00, 'Great Ball');
