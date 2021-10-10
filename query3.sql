SELECT COUNT(I.ItemID)
FROM Item I
WHERE (SELECT COUNT(*) 
       FROM Category C
       WHERE I.ItemID=C.ItemID
       GROUP BY C.ItemID
       ) = 4; 