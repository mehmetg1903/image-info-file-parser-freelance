CREATE TABLE Seminar.dbo.Tarrant (  ID INT PRIMARY KEY IDENTITY (1, 1) NOT NULL,  Document_Number VARCHAR (255) NULL,  Filing_Date date NULL,  Name VARCHAR (255) NULL,  Owner VARCHAR (255) NULL,  Address VARCHAR (255) NULL,  City VARCHAR (255) NULL, State VARCHAR (255) NULL, Zip VARCHAR (255) NULL,);
CREATE TABLE dbo.Bexar (  ID INT PRIMARY KEY IDENTITY (1, 1) NOT NULL,  Document_Number VARCHAR (255) NULL,  Filing_Date date NULL,  Name VARCHAR (255) NULL,  Owner VARCHAR (255) NULL,  Address VARCHAR (255) NULL,  City VARCHAR (255) NULL, State VARCHAR (255) NULL, Zip VARCHAR (255) NULL,);
CREATE TABLE dbo.Collin (  ID INT PRIMARY KEY IDENTITY (1, 1) NOT NULL,  Document_Number VARCHAR (255) NULL,  Filing_Date date NULL,  Name VARCHAR (255) NULL,  Owner VARCHAR (255) NULL,  Address VARCHAR (255) NULL,  City VARCHAR (255) NULL, State VARCHAR (255) NULL, Zip VARCHAR (255) NULL,);