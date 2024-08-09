SELECT L.Date, L.Messages
FROM AiLog AS L
WHERE L.Messages LIKE '%dark%'
ORDER BY L.Date DESC
LIMIT 10