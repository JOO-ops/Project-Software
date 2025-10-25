CREATE DATABASE IF NOT EXISTS HomeCare_Maintenance_System;
USE HomeCare_Maintenance_System;

CREATE TABLE `Users` (
    `ID` VARCHAR(50) PRIMARY KEY,
    `Email` VARCHAR(300) UNIQUE NOT NULL,
    `Password` VARCHAR(300) NOT NULL,
    `Role` ENUM('tenant', 'admin', 'technician') NOT NULL,
    `FirstName` VARCHAR(100),
    `LastName` VARCHAR(100),
    `Phone` VARCHAR(50),
    `CreatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `UpdatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE `Maintenance_Requests` (
    `ID` VARCHAR(50) PRIMARY KEY,
    `UserID` VARCHAR(50) NOT NULL,
    `AssignedTechnicianID` VARCHAR(50),
    `Title` VARCHAR(300) NOT NULL,
    `Description` TEXT,
    `Category` ENUM('plumbing', 'electrical', 'cleaning', 'general') NOT NULL,
    `Priority` ENUM('low', 'medium', 'high', 'emergency') DEFAULT 'medium',
    `Location` VARCHAR(255),
    `Status` ENUM('pending', 'in-progress', 'completed', 'rejected') DEFAULT 'pending',
    `Images` BLOB,
    `CreatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `UpdatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `CompletedAt` TIMESTAMP,
    FOREIGN KEY (`UserID`) REFERENCES `Users`(`ID`),
    FOREIGN KEY (`AssignedTechnicianID`) REFERENCES `Users`(`ID`)
) ENGINE=InnoDB;

CREATE TABLE `Comments` (
    `ID` INT AUTO_INCREMENT PRIMARY KEY,
    `RequestID` VARCHAR(50) NOT NULL,
    `UserID` VARCHAR(50) NOT NULL,
    `CommentText` TEXT NOT NULL,
    `CreatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`RequestID`) REFERENCES `Maintenance_Requests`(`ID`) ON DELETE CASCADE,
    FOREIGN KEY (`UserID`) REFERENCES `Users`(`ID`)
) ENGINE=InnoDB;
