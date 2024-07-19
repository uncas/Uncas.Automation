CREATE TABLE Prices (Model Text, PricePerMillionInput Integer, PricePerMillionOutput Integer)

INSERT INTO Prices (Model, PricePerMillionInput, PricePerMillionOutput)
VALUES ('gpt-3.5-turbo', 0.5, 1.5)

INSERT INTO Prices (Model, PricePerMillionInput, PricePerMillionOutput)
VALUES ('gpt-4o', 5, 15)

INSERT INTO Prices (Model, PricePerMillionInput, PricePerMillionOutput)
VALUES ('gpt-4o-mini', 0.15, 0.6)

SELECT * FROM Prices
