DROP TABLE IF EXISTS Person
CREATE TABLE Person 
	(PersonID NUMERIC(11,0) NOT NULL,
		Username VARCHAR(25) NOT NULL,
		Password VARCHAR(25) NOT NULL,
		Name VARCHAR(25) NOT NULL,
		ShippingAddress VARCHAR(40), 
		BillingAddress VARCHAR(40), 
		EmployeePosition(25), 
		PersonType(15) NOT NULL,
		CONSTRAINT Person_PK PRIMARY KEY (PersonID); 