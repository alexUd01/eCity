-- MariaDB dump 10.19  Distrib 10.11.2-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ecity
-- ------------------------------------------------------
-- Server version	10.11.2-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer` (
  `answer_id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `correct_option` varchar(1) DEFAULT NULL,
  `correct_notes` text DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `question_id` (`question_id`),
  KEY `exam_id` (`exam_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`),
  CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES
(3,3,1,'D',NULL),
(4,4,1,'D',NULL),
(5,5,1,'B',NULL),
(6,6,1,'A',NULL),
(7,7,1,'B',NULL),
(8,8,1,'H',NULL);
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer_sheet`
--

DROP TABLE IF EXISTS `answer_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer_sheet` (
  `answer_sheet_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `student_choice` varchar(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`answer_sheet_id`),
  KEY `user_id` (`user_id`),
  KEY `exam_id` (`exam_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answer_sheet_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `answer_sheet_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`),
  CONSTRAINT `answer_sheet_ibfk_3` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer_sheet`
--

LOCK TABLES `answer_sheet` WRITE;
/*!40000 ALTER TABLE `answer_sheet` DISABLE KEYS */;
INSERT INTO `answer_sheet` VALUES
(1,4,1,3,'D','2023-06-05 13:12:45'),
(2,4,1,4,'A','2023-06-05 13:12:45'),
(3,4,1,5,'A','2023-06-05 13:12:45'),
(4,4,1,6,'A','2023-06-05 13:12:45'),
(5,4,1,7,'B','2023-06-05 13:12:45'),
(6,4,1,8,'B','2023-06-05 13:12:45'),
(7,4,1,3,'A','2023-06-05 14:11:17'),
(8,4,1,4,'B','2023-06-05 14:11:17'),
(9,4,1,5,'B','2023-06-05 14:11:17'),
(10,4,1,6,'B','2023-06-05 14:11:17'),
(11,4,1,7,'A','2023-06-05 14:11:17'),
(12,4,1,8,'B','2023-06-05 14:11:17'),
(13,4,1,3,'A','2023-06-05 23:12:33'),
(14,4,1,4,'D','2023-06-05 23:12:33'),
(15,4,1,5,'A','2023-06-05 23:12:33'),
(16,4,1,6,'C','2023-06-05 23:12:33'),
(17,4,1,7,'B','2023-06-05 23:12:33'),
(18,4,1,8,'B','2023-06-05 23:12:33'),
(19,4,1,3,'A','2023-06-06 13:27:50'),
(20,4,1,4,'B','2023-06-06 13:27:50'),
(21,4,1,5,'B','2023-06-06 13:27:50'),
(22,4,1,6,'A','2023-06-06 13:27:50'),
(23,4,1,7,'B','2023-06-06 13:27:50'),
(24,4,1,8,'C','2023-06-06 13:27:50');
/*!40000 ALTER TABLE `answer_sheet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam`
--

DROP TABLE IF EXISTS `exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam` (
  `exam_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(128) NOT NULL,
  `time_allowed` int(11) NOT NULL,
  `date_created` datetime NOT NULL,
  `date_taken` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`exam_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `exam_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam`
--

LOCK TABLES `exam` WRITE;
/*!40000 ALTER TABLE `exam` DISABLE KEYS */;
INSERT INTO `exam` VALUES
(1,'Computer Science',60,'2023-05-31 10:02:44','2023-05-31 10:10:29',2);
/*!40000 ALTER TABLE `exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `data` text NOT NULL,
  `A` text DEFAULT NULL,
  `B` text DEFAULT NULL,
  `C` text DEFAULT NULL,
  `D` text DEFAULT NULL,
  `E` text DEFAULT NULL,
  `F` text DEFAULT NULL,
  `G` text DEFAULT NULL,
  `H` text DEFAULT NULL,
  `exam_id` int(11) NOT NULL,
  PRIMARY KEY (`question_id`),
  KEY `exam_id` (`exam_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES
(3,'Which of the following is a computer hardware?','Linux','Windows','LibreOffice','Mouse',NULL,NULL,NULL,NULL,1),
(4,'Who invented Napier\'s bone?','Stephen Napier','Joe Napier','Matthew Napier','John Napier',NULL,NULL,NULL,NULL,1),
(5,'Is C a high level programming language?','True','False',NULL,NULL,NULL,NULL,NULL,NULL,1),
(6,'Which of the following programming languages does not have garbage collector?','C Programming Language','Python Programming Language','JavaScript Programming Language','Ruby',NULL,NULL,NULL,NULL,1),
(7,'Python cannot be used in building web applications.','True','False',NULL,NULL,NULL,NULL,NULL,NULL,1),
(8,'Which of the following is a computer virus capable of?','Turning off a computer\'s display.','Duplicating user files.','Rendering a computer unusable.','Turning off a computer.','Capturing video/images using the user\'s webcam with user\'s permission.','Deleting user files without user\'s permission.','creating a back door for a hacker to gain access to your system.','All of the above.',1);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score`
--

DROP TABLE IF EXISTS `score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `score` (
  `score_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `score_attainable` int(11) NOT NULL,
  PRIMARY KEY (`score_id`),
  KEY `user_id` (`user_id`),
  KEY `exam_id` (`exam_id`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `score_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES
(1,4,1,3,6),
(2,4,1,1,6),
(3,4,1,0,6),
(4,4,1,0,6),
(5,4,1,0,6),
(6,4,1,0,6),
(7,4,1,0,6),
(8,4,1,0,6),
(9,4,1,0,6),
(10,4,1,0,6),
(11,4,1,0,6),
(12,4,1,0,6),
(13,4,1,0,6),
(14,4,1,0,6),
(15,4,1,0,6),
(16,4,1,0,6),
(17,4,1,0,6),
(18,4,1,0,6),
(19,4,1,2,6),
(20,4,1,3,6);
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `firstname` varchar(128) NOT NULL,
  `lastname` varchar(128) NOT NULL,
  `middlename` varchar(128) DEFAULT NULL,
  `password` varchar(256) NOT NULL,
  `email` varchar(128) NOT NULL,
  `gender` enum('M','F') DEFAULT NULL,
  `is_student` enum('T','F') DEFAULT NULL,
  `is_examiner` enum('T','F') DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `last_login` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(1,'Lucy','Lucinda','John','Ada','lucinda','lucy@gmail.com','F','F','T','2023-05-31 09:32:19','2023-05-31 09:32:19','0000-00-00 00:00:00'),
(2,'Xandex','Alexander','Ikpeama','Udochukwu','alexander','alexanderikpeama@gmail.com','M','T','T','2023-05-31 09:32:19','2023-05-31 09:32:19','0000-00-00 00:00:00'),
(4,'Raymonis','Raymond','Ikpeama','Ikechukwu','raymond','rayikpeama@gmail.com','M','T','F','2023-05-31 12:28:52','2023-05-31 12:28:52','0000-00-00 00:00:00'),
(5,'Tesan#001','Destiny','Derik','Tesan','destiny','joetesan@gmail.com','M','T','F','2023-06-02 14:30:08','2023-06-02 14:30:08','0000-00-00 00:00:00'),
(8,'justifiedmultibiz','Justice','Ikpeama','Chimela','justice','justiceikpeamah@gmail.com',NULL,NULL,NULL,'2023-06-07 03:04:31','2023-06-07 03:04:31','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-07  7:49:54
