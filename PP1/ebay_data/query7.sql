SELECT COUNT(DISTINCT Category)
FROM ItemCategory
WHERE itemID in (SELECT itemID
                 FROM Bids
                 WHERE cast(replace(replace(Amount, '$', ''),',','') as INT) > 100
                 order by cast(replace(replace(Amount, '$', ''),',','') as INT));