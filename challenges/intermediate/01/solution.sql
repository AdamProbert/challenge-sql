-- Solution for the intermediate JOIN challenge
SELECT
    ip.purchase_id,
    ip.purchase_date,
    ip.rupee_amount,
    s.shop_name || ' in ' || s.location AS shop_details
FROM
    item_purchases ip
    INNER JOIN shops s ON ip.shop_id = s.shop_id;
