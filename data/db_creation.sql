DROP DATABASE Safe;
CREATE DATABASE Safe;

USE Safe;

CREATE TABLE Users(
  UserId INT NOT NULL,
  Xp INT NOT NULL,
  PRIMARY KEY (UserId)
);

CREATE TABLE Groupz(
  GroupId INT NOT NULL AUTO_INCREMENT,
  RomanName VARCHAR(255) NOT NULL,
  RawName VARCHAR(255) CHARACTER SET utf32,
  AddedBy INT,
  PRIMARY KEY (GroupId)
);

CREATE TABLE Members(
  MemberId INT NOT NULL AUTO_INCREMENT,
  GroupId INT NOT NULL,
  RomanName VARCHAR(255) NOT NULL,
  RawName VARCHAR(255) CHARACTER SET utf32,
  AddedBy INT,
  PRIMARY KEY (MemberId),
  FOREIGN KEY (GroupId) REFERENCES Groupz(GroupId)
);

CREATE TABLE Tags(
  TagId INT NOT NULL AUTO_INCREMENT,
  TagName VARCHAR(255) NOT NULL,
  PRIMARY KEY (TagId)
);
 
CREATE TABLE Links(
  LinkId INT NOT NULL AUTO_INCREMENT,
  Link VARCHAR(255) NOT NULL,
  AddedBy INT,
  Primary KEY (LinkId)
);

CREATE TABLE Link_Tags(
  LinkId INT NOT NULL,
  TagId INT NOT NULL,
  PRIMARY KEY (LinkId, TagId),
  FOREIGN KEY (LinkId) REFERENCES Links(LinkId),
  FOREIGN KEY (TagId) REFERENCES Tags(TagId)
);

CREATE TABLE Link_Members(
  LinkId INT NOT NULL,
  MemberId INT NOT NULL,
  PRIMARY KEY (LinkId, MemberId),
  FOREIGN KEY (LinkId) REFERENCES Links(LinkId),
  FOREIGN KEY (MemberId) REFERENCES Members(MemberId)
);

CREATE TABLE CustomCommands(
   CommandName VARCHAR(255) CHARACTER SET utf32,
   Command VARCHAR(255) CHARACTER SET utf32,
   AddedBy INT
);