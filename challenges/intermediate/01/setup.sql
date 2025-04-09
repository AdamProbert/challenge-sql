-- Setup for intermediate JOIN challenge
-- Create shops and item_purchases tables with Zelda-themed sample data
CREATE TABLE shops (
    shop_id SERIAL PRIMARY KEY,
    shop_name VARCHAR(50) NOT NULL,
    shopkeeper VARCHAR(50) NOT NULL,
    location VARCHAR(100) UNIQUE NOT NULL,
    rupee_exchange_rate DECIMAL(10, 2),
    established_date DATE NOT NULL
);

CREATE TABLE item_purchases (
    purchase_id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops (shop_id),
    purchase_date DATE NOT NULL,
    rupee_amount DECIMAL(10, 2) NOT NULL,
    item_name VARCHAR(50) NOT NULL
);

-- Insert sample shops
INSERT INTO
    shops (
        shop_name,
        shopkeeper,
        location,
        rupee_exchange_rate,
        established_date
    )
VALUES
    (
        'Beedle''s Airshop',
        'Beedle',
        'Sky Islands',
        1.25,
        '2011-11-18'
    ),
    (
        'Malo Mart',
        'Malo',
        'Castle Town',
        1.0,
        '2006-11-19'
    ),
    (
        'Bomb Shop',
        'Barnes',
        'Kakariko Village',
        1.5,
        '2006-11-19'
    ),
    (
        'Curiosity Shop',
        'Man in Green',
        'Clock Town',
        0.8,
        '2000-04-27'
    ),
    (
        'Happy Mask Shop',
        'Happy Mask Salesman',
        'Hyrule Castle Town',
        2.0,
        '1998-11-21'
    );

-- Insert sample item purchases
INSERT INTO
    item_purchases (shop_id, purchase_date, rupee_amount, item_name)
VALUES
    (1, '2023-03-10', 120.00, 'Golden Beetle'),
    (2, '2023-03-12', 80.00, 'Red Potion'),
    (3, '2023-03-15', 40.00, 'Bombs (10)'),
    (1, '2023-03-20', 200.00, 'Goddess Plume'),
    (2, '2023-03-25', 50.00, 'Deku Shield'),
    (4, '2023-03-28', 300.00, 'All-Night Mask'),
    (5, '2023-04-01', 20.00, 'Keaton Mask'),
    (1, '2023-04-05', 85.00, 'Ancient Flower');
