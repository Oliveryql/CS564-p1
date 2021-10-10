WITH A AS (SELECT DISTINCT UserID FROM Auction),
    B AS (SELECT DISTINCT Seller_UserID FROM Item)

SELECT COUNT(*)
FROM User U,A,B
WHERE U.UserID = B.Seller_UserID
AND B.Seller_UserID = A.UserID;
