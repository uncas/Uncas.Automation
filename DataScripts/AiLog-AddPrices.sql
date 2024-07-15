CREATE TABLE Prices (Model Text, PricePerMillionInput Integer, PricePerMillionOutput Integer)

INSERT INTO Prices (Model, PricePerMillionInput, PricePerMillionOutput)
VALUES ('gpt-3.5-turbo', 0.5, 1.5)

INSERT INTO Prices (Model, PricePerMillionInput, PricePerMillionOutput)
VALUES ('gpt-4o', 5, 15)