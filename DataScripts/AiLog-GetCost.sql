SELECT L.Model
	, COUNT(*) AS Requests
	, SUM(L.PromptTokens) AS PromptTokens
	, SUM(L.CompletionTokens) AS CompletionTokens
	, 	IFNULL(P.PricePerMillionInput, 0) * SUM(L.PromptTokens)/1000.0/1000 +
		IFNULL(P.PricePerMillionOutput, 0) * SUM(L.CompletionTokens)/1000.0/1000
		AS Dollars
	, 	(IFNULL(P.PricePerMillionInput, 0)* SUM(L.PromptTokens)/1000.0/1000 +
		IFNULL(P.PricePerMillionOutput, 0) * SUM(L.CompletionTokens)/1000.0/1000)
		/ COUNT(*) * 100 AS CentsPerRequest
FROM AiLog AS L
LEFT JOIN Prices AS P ON L.Model = P.Model
GROUP BY L.Model
ORDER BY COUNT(*) DESC