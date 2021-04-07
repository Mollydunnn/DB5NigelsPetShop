DROP TABLE IF EXISTS Person
CREATE TABLE Person 
	(PersonID NUMERIC(11,0) NOT NULL,
		Username VARCHAR(25) NOT NULL,
		Password VARCHAR(25) NOT NULL,
		Name VARCHAR(25) NOT NULL,
		ShippingAddress VARCHAR(40), 
		BillingAddress VARCHAR(40), 
		EmployeePosition CHAR(25), 
		PersonType CHAR(15) NOT NULL,
		CONSTRAINT Person_PK PRIMARY KEY (PersonID);
CREATE TABLE Adoption
	(AdoptionID NUMERIC(11,0) NOT NULL,
		DateOfAdoption DATE,
		EmployeeID NUMERIC(11,0) NOT NULL,
		CustomerID NUMERIC(11,0) NOT NULL,
		AnimalID NUMERIC(11,0),
		CONSTRAINT Adoption_PK PRIMARY KEY (AdoptionID),
		CONSTRAINT Adoption_FK1 FOREIGN KEY (EmployeeID)
			REFERENCES Person(PersonID),
		CONSTRAINT Adoption_FK2 FOREIGN KEY (CustomerID)
			REFERENCES Person(PersonID),
		CONSTRAINT Adoption_FK3 FOREIGN KEY (AnimalID)
			REFERENCES Animal(AnimalID)); 
					  
CREATE TABLE Inventory
		(InventoryID decimal(11,0), 
		 ProductName varchar(20), 
		 Price decimal(6,2), 
		 CONSTRAINT Inventory_PK PRIMARY KEY(InventoryID));
			     
CREATE TABLE Order1
		(OrderID decimal(11,0), 
		 OrderDate date, 
		 PersonID decimal(11,0), 
		 CONSTRAINT Order_PK PRIMARY KEY(OrderID), 
		 CONSTRAINT Order_FK1 FOREIGN KEY(PersonID) REFERENCES Person(PersonID));
									      
CREATE TABLE OrderLine
		(OrderedQuantity int, 
		 InventoryID decimal(11,0), 
		 OrderID decimal(11,0),
		 CONSTRAINT OrderLine_FK1 FOREIGN KEY(InventoryID) REFERENCES Inventory(InventoryID), 
		 CONSTRAINT OrderLine_FK2 FOREIGN KEY(OrderID) REFERENCES Order1(OrderID));
--adding values:
INSERT INTO Inventory
VALUES ( 001, ‘Green Grass Kibble’, 40.00);

INSERT INTO Inventory
VALUES ( 002, ‘Indestructible Squeaky Toy’, 25.00);
INSERT INTO Inventory
VALUES ( 003, ‘Princess Leash’, 20.00);

INSERT INTO Inventory
VALUES ( 004, ‘Custom Collar’, 15.00);
										 

										 
										 
										 
