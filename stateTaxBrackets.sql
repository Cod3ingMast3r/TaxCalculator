CREATE TABLE state_tax_brackets (
    id INTEGER,
    states TEXT,
    tax_rates REAL,
    flat_or_progressive TEXT
);

INSERT INTO state_tax_brackets (id, states, tax_rates, flat_or_progressive) 
VALUES (0, 'MI', 4.25/100, 'flat')

SELECT * FROM state_tax_brackets;