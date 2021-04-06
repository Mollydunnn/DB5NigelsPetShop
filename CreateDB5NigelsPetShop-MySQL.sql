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
		CONSTRAINT Adoption_FK3 FOREIGN KEY (AdoptionID)
			REFERENCES Animal(AnimalID)); 