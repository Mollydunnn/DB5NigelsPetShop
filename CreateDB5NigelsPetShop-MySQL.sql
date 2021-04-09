DROP TABLE IF EXISTS Person;
CREATE TABLE person 
	(PersonID int NOT NULL,
		Username VARCHAR(25),
		Password VARCHAR(25),
		Name VARCHAR(25),
		ShippingAddress VARCHAR(40), 
		BillingAddress VARCHAR(40), 
		EmployeePosition CHAR(25), 
		CONSTRAINT Person_PK PRIMARY KEY (PersonID);
CREATE TABLE Adoption
	(AdoptionID int,
		DateOfAdoption DATE,
		EmployeeID int,
		CustomerID int,
		AnimalID NUMERIC(11,0),
		CONSTRAINT Adoption_PK PRIMARY KEY (AdoptionID),
		CONSTRAINT Adoption_FK1 FOREIGN KEY (EmployeeID)
			REFERENCES person(PersonID),
		CONSTRAINT Adoption_FK2 FOREIGN KEY (CustomerID)
			REFERENCES person(PersonID),
		CONSTRAINT Adoption_FK3 FOREIGN KEY (AnimalID)
			REFERENCES Animal(AnimalID)); 
					  
CREATE TABLE Inventory
		(InventoryID int, 
		 ProductName varchar(20), 
		 Price decimal(6,2), 
		 CONSTRAINT Inventory_PK PRIMARY KEY(InventoryID));
			     
CREATE TABLE Order1
		(OrderID int, 
		 OrderDate date, 
		 PersonID int, 
		 CONSTRAINT Order_PK PRIMARY KEY(OrderID), 
		 CONSTRAINT Order_FK1 FOREIGN KEY(PersonID) REFERENCES Person(PersonID));
									      
CREATE TABLE OrderLine
		(OrderedQuantity int, 
		 InventoryID int, 
		 OrderID int,
		 CONSTRAINT OrderLine_FK1 FOREIGN KEY(InventoryID) REFERENCES Inventory(InventoryID), 
		 CONSTRAINT OrderLine_FK2 FOREIGN KEY(OrderID) REFERENCES Order1(OrderID));
INSERT INTO person(PersonID, Username, Password, Name)
VALUES ( 3, 'joe', 'schmo', 'joe schmo')
										 
INSERT INTO Inventory
VALUES ( 1, 'Green Grass Kibble', 40.00);

INSERT INTO Inventory
VALUES ( 2, 'Indestructible Squeaky Toy', 25.00);
INSERT INTO Inventory
VALUES ( 3, 'Princess Leash', 20.00);

INSERT INTO Inventory
VALUES ( 4, 'Custom Collar', 15.00);

INSERT INTO Order1
VALUES (1, 2021-04-07, 3)
	
INSERT INTO Order1
VALUES (2, 2021-04-04, 3)
										 
INSERT INTO OrderLine
VALUES (3, 1, 1)
										 
INSERT INTO OrderLine
VALUES (4, 2, 2)										
										 
										 
										 
