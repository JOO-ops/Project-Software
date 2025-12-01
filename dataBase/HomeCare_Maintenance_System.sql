CREATE DATABASE  IF NOT EXISTS `homecare_maintenance_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `homecare_maintenance_system`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: homecare_maintenance_system
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_dashboard`
--

DROP TABLE IF EXISTS `admin_dashboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_dashboard` (
  `ID` int NOT NULL DEFAULT '1',
  `TotalUsers` int DEFAULT '0',
  `TenantsCount` int DEFAULT '0',
  `TechniciansCount` int DEFAULT '0',
  `AdminsCount` int DEFAULT '0',
  `TotalRequests` int DEFAULT '0',
  `PendingRequests` int DEFAULT '0',
  `InProgressRequests` int DEFAULT '0',
  `CompletedRequests` int DEFAULT '0',
  `RejectedRequests` int DEFAULT '0',
  `AverageRating` float DEFAULT '0',
  `TopRatedTechnicianID` varchar(50) DEFAULT NULL,
  `LastUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `TopRatedTechnicianID` (`TopRatedTechnicianID`),
  CONSTRAINT `admin_dashboard_ibfk_1` FOREIGN KEY (`TopRatedTechnicianID`) REFERENCES `users` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_dashboard`
--

LOCK TABLES `admin_dashboard` WRITE;
/*!40000 ALTER TABLE `admin_dashboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_dashboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attachments`
--

DROP TABLE IF EXISTS `attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attachments` (
  `ID` varchar(50) NOT NULL,
  `RequestID` varchar(50) NOT NULL,
  `FilePath` varchar(500) NOT NULL,
  `UploadedBy` varchar(50) DEFAULT NULL,
  `UploadedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `RequestID` (`RequestID`),
  KEY `UploadedBy` (`UploadedBy`),
  CONSTRAINT `attachments_ibfk_1` FOREIGN KEY (`RequestID`) REFERENCES `maintenance_requests` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `attachments_ibfk_2` FOREIGN KEY (`UploadedBy`) REFERENCES `users` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attachments`
--

LOCK TABLES `attachments` WRITE;
/*!40000 ALTER TABLE `attachments` DISABLE KEYS */;
/*!40000 ALTER TABLE `attachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `RequestID` varchar(50) NOT NULL,
  `UserID` varchar(50) NOT NULL,
  `CommentText` text NOT NULL,
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `RequestID` (`RequestID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`RequestID`) REFERENCES `maintenance_requests` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `ID` varchar(50) NOT NULL,
  `RequestID` varchar(50) NOT NULL,
  `UserID` varchar(50) NOT NULL,
  `Rating` int DEFAULT NULL,
  `Comments` text,
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `UserID` (`UserID`),
  KEY `idx_feedback_request` (`RequestID`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`RequestID`) REFERENCES `maintenance_requests` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `feedback_chk_1` CHECK ((`Rating` between 1 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_requests`
--

DROP TABLE IF EXISTS `maintenance_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_requests` (
  `ID` varchar(50) NOT NULL,
  `UserID` varchar(50) NOT NULL,
  `AssignedTechnicianID` varchar(50) DEFAULT NULL,
  `Title` varchar(300) NOT NULL,
  `Description` text,
  `Category` enum('plumbing','electrical','cleaning','general') NOT NULL,
  `Priority` enum('low','medium','high','emergency') DEFAULT 'medium',
  `Location` varchar(255) DEFAULT NULL,
  `Status` enum('pending','in-progress','completed','rejected') DEFAULT 'pending',
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CompletedAt` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `AssignedTechnicianID` (`AssignedTechnicianID`),
  KEY `idx_request_status` (`Status`),
  KEY `idx_request_user` (`UserID`),
  CONSTRAINT `maintenance_requests_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `maintenance_requests_ibfk_2` FOREIGN KEY (`AssignedTechnicianID`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_requests`
--

LOCK TABLES `maintenance_requests` WRITE;
/*!40000 ALTER TABLE `maintenance_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `maintenance_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `ID` varchar(50) NOT NULL,
  `UserID` varchar(50) NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Message` text NOT NULL,
  `IsRead` tinyint(1) DEFAULT '0',
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `idx_notification_user` (`UserID`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request_history`
--

DROP TABLE IF EXISTS `request_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_history` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `RequestID` varchar(50) NOT NULL,
  `ChangedBy` varchar(50) DEFAULT NULL,
  `OldStatus` enum('pending','in-progress','completed','rejected') DEFAULT NULL,
  `NewStatus` enum('pending','in-progress','completed','rejected') DEFAULT NULL,
  `ChangeNote` text,
  `ChangedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `RequestID` (`RequestID`),
  KEY `ChangedBy` (`ChangedBy`),
  CONSTRAINT `request_history_ibfk_1` FOREIGN KEY (`RequestID`) REFERENCES `maintenance_requests` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `request_history_ibfk_2` FOREIGN KEY (`ChangedBy`) REFERENCES `users` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request_history`
--

LOCK TABLES `request_history` WRITE;
/*!40000 ALTER TABLE `request_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `request_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `technician_dashboard`
--

DROP TABLE IF EXISTS `technician_dashboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `technician_dashboard` (
  `UserID` varchar(50) NOT NULL,
  `TotalAssigned` int DEFAULT '0',
  `InProgressJobs` int DEFAULT '0',
  `CompletedJobs` int DEFAULT '0',
  `UpcomingJobs` int DEFAULT '0',
  `AverageRating` float DEFAULT '0',
  `LastUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserID`),
  CONSTRAINT `technician_dashboard_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `technician_dashboard`
--

LOCK TABLES `technician_dashboard` WRITE;
/*!40000 ALTER TABLE `technician_dashboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `technician_dashboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `technician_schedules`
--

DROP TABLE IF EXISTS `technician_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `technician_schedules` (
  `ID` varchar(50) NOT NULL,
  `TechnicianID` varchar(50) NOT NULL,
  `AvailableFrom` datetime NOT NULL,
  `AvailableTo` datetime NOT NULL,
  `IsBooked` tinyint(1) DEFAULT '0',
  `RequestID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `TechnicianID` (`TechnicianID`),
  KEY `RequestID` (`RequestID`),
  CONSTRAINT `technician_schedules_ibfk_1` FOREIGN KEY (`TechnicianID`) REFERENCES `users` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `technician_schedules_ibfk_2` FOREIGN KEY (`RequestID`) REFERENCES `maintenance_requests` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `technician_schedules`
--

LOCK TABLES `technician_schedules` WRITE;
/*!40000 ALTER TABLE `technician_schedules` DISABLE KEYS */;
/*!40000 ALTER TABLE `technician_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant_dashboard`
--

DROP TABLE IF EXISTS `tenant_dashboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenant_dashboard` (
  `UserID` varchar(50) NOT NULL,
  `TotalRequests` int DEFAULT '0',
  `PendingRequests` int DEFAULT '0',
  `InProgressRequests` int DEFAULT '0',
  `CompletedRequests` int DEFAULT '0',
  `RejectedRequests` int DEFAULT '0',
  `AverageRating` float DEFAULT '0',
  `UnreadNotifications` int DEFAULT '0',
  `LastUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserID`),
  CONSTRAINT `tenant_dashboard_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant_dashboard`
--

LOCK TABLES `tenant_dashboard` WRITE;
/*!40000 ALTER TABLE `tenant_dashboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `tenant_dashboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `ID` varchar(50) NOT NULL,
  `Email` varchar(300) NOT NULL,
  `Password` varchar(300) NOT NULL,
  `Role` enum('tenant','admin','technician') NOT NULL,
  `FirstName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `Phone` varchar(50) DEFAULT NULL,
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Email` (`Email`),
  KEY `idx_user_email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-28  0:05:38
