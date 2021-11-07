
DROP TABLE IF EXISTS User;

CREATE TABLE IF NOT EXISTS User( 
    userID varchar(30) NOT NULL,
    schoolName varchar(30) NOT NULL,
    password varchar(30) NOT NULL, 
    Email varchar(50) NOT NULL,
    isAdmin int ,
    identityCode varchar(30),
    accessKey varchar(100),
    PRIMARY KEY (userID) );


