drop table if exists Item;

drop table if exists Auction;

drop table if exists User;

drop table if exists Category;

create table Item (
    ItemID CHAR(10) PRIMARY KEY,
    Name VARCHAR,
    Currently CHAR(10),
    Buy_Price CHAR(10),
    First_Bid CHAR(10),
    Number_of_Bids CHAR(5),
    Started CHAR(20),
    Ends CHAR(20),
    Seller_UserID VARCHAR,
    Description VARCHAR,
    FOREIGN KEY (Seller_UserID) REFERENCES User(UserID)
);

create table User(
    UserID VARCHAR PRIMARY KEY,
    Location VARCHAR,
    Country VARCHAR,
    Rating VARCHAR
);

create table Auction(
    ItemID CHAR(10),
    UserID VARCHAR,
    Time VARCHAR,
    Amount VARCHAR,
    PRIMARY KEY(ItemID, UserID, Time),FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

create table Category(
    ItemID CHAR(10),
    Category VARCHAR,
    PRIMARY KEY(ItemID, Category)
);