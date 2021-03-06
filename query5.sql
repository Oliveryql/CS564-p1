WITH  S AS (SELECT DISTINCT Seller_UserID FROM Item)

SELECT COUNT(*)
FROM User U, S
WHERE U.UserID = S.Seller_UserID
AND CAST(U.Rating AS INT ) > 1000;