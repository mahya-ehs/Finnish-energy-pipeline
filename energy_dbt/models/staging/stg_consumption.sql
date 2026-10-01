SELECT 
startTime AS time,
endTime AS end_time,
value AS consumption_mw, 
date_diff('minute', startTime, endTime) AS resolution_minutes
FROM read_json('../data/raw/fingrid/consumption/*/data.json')
