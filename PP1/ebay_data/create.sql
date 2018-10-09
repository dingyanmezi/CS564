drop table if exists Item;
drop table if exists Users;
drop table if exists Bids;
drop table if exists ItemCategory;

CREATE TABLE Item (
	ItemID	INT PRIMARY KEY,
	Name	TEXT,
	Currently	TEXT,
	Buy_Price	TEXT,
	First_Bid	TEXT,
	Number_of_Bids	INT,
	Description		TEXT,
	Started			TEXT,
	Ends	TEXT,
	SellerID	TEXT,
	FOREIGN KEY (SellerID) REFERENCES Users(UserID)
);

CREATE TABLE Users (
	UserID	TEXT PRIMARY KEY,
	Location	TEXT,
	Country	TEXT, 
	Rating	INT 
);

CREATE TABLE Bids(
	ItemID INT,
	BidderID TEXT,
	Timet TEXT,
	Amount TEXT,
	FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
	FOREIGN KEY (BidderID) REFERENCES Users(UserID)
);

CREATE TABLE ItemCategory(
	ItemID INT,
	Category TEXT,
	FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);