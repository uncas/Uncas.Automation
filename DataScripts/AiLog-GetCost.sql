SELECT L.Model
	, COUNT(*) AS Requests
	, SUM(L.PromptTokens) AS PromptTokens
	, SUM(L.CompletionTokens) AS CompletionTokens
	, 	P.PricePerMillionInput * SUM(L.PromptTokens)/1000.0/1000 +
		P.PricePerMillionOutput * SUM(L.CompletionTokens)/1000.0/1000
		AS Dollars
	, 	(P.PricePerMillionInput * SUM(L.PromptTokens)/1000.0/1000 +
		P.PricePerMillionOutput * SUM(L.CompletionTokens)/1000.0/1000)
		/ COUNT(*) * 100 AS CentsPerRequest
FROM AiLog AS L
JOIN Prices AS P ON L.Model = P.Model
GROUP BY L.Model
