SELECT itemID
FROM Item
WHERE currently = (SELECT currently
                  FROM Item
                  ORDER BY CAST(replace(replace(replace(Currently, '$', ''), '.', ''), ',', '') as INT)
                  Desc
                  LIMIT 1);