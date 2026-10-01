SELECT 
timezone('UTC', startTime) AS time,
timezone('UTC', endTime) AS end_time,
value AS consumption_mw, 
date_diff('minute', startTime, endTime) AS resolution_minutes
FROM read_json('../data/raw/fingrid/consumption/*/data.json')
