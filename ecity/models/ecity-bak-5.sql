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
  `correct_notes` text DEFAULT '',
  PRIMARY KEY (`answer_id`),
  KEY `question_id` (`question_id`),
  KEY `exam_id` (`exam_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`),
  CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES
(3,3,1,'D',''),
(4,4,1,'D',''),
(5,5,1,'B',''),
(6,6,1,'A',''),
(7,7,1,'B',''),
(8,8,1,'H',''),
(9,27,10,'A',''),
(10,28,10,'D',''),
(11,29,10,'C',''),
(12,30,10,'D',''),
(13,31,10,'C',''),
(14,32,11,'C',''),
(15,33,11,'A',''),
(16,34,11,'B',''),
(17,35,11,'A',''),
(18,36,11,'D',''),
(24,42,13,'B',''),
(25,43,13,'B',''),
(28,46,1,'A','No explanation'),
(29,47,1,'B','None'),
(30,48,13,'',''),
(77,101,48,'A','asdfasdfs');
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
  `student_choice` varchar(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`answer_sheet_id`),
  KEY `user_id` (`user_id`),
  KEY `exam_id` (`exam_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answer_sheet_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `answer_sheet_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`),
  CONSTRAINT `answer_sheet_ibfk_3` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=445 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer_sheet`
--

LOCK TABLES `answer_sheet` WRITE;
/*!40000 ALTER TABLE `answer_sheet` DISABLE KEYS */;
INSERT INTO `answer_sheet` VALUES
(291,77,1,3,'D','2023-09-22 23:45:15'),
(292,77,1,4,'D','2023-09-22 23:45:15'),
(293,77,1,5,'B','2023-09-22 23:45:15'),
(294,77,1,6,'A','2023-09-22 23:45:15'),
(295,77,1,7,'B','2023-09-22 23:45:15'),
(296,77,1,8,'H','2023-09-22 23:45:15'),
(297,77,1,46,'A','2023-09-22 23:45:15'),
(298,77,1,47,'A','2023-09-22 23:45:15'),
(299,77,10,27,NULL,'2023-09-22 23:45:15'),
(300,77,10,28,NULL,'2023-09-22 23:45:15'),
(301,77,10,29,NULL,'2023-09-22 23:45:15'),
(302,77,10,30,NULL,'2023-09-22 23:45:15'),
(303,77,10,31,NULL,'2023-09-22 23:45:15'),
(304,77,11,32,NULL,'2023-09-22 23:45:15'),
(305,77,11,33,NULL,'2023-09-22 23:45:15'),
(306,77,11,34,NULL,'2023-09-22 23:45:15'),
(307,77,11,35,NULL,'2023-09-22 23:45:15'),
(308,77,11,36,NULL,'2023-09-22 23:45:15'),
(309,77,13,42,NULL,'2023-09-22 23:45:15'),
(310,77,13,43,NULL,'2023-09-22 23:45:15'),
(311,77,13,48,NULL,'2023-09-22 23:45:15'),
(351,18,1,3,NULL,'2023-09-26 10:11:36'),
(352,18,1,4,NULL,'2023-09-26 10:11:36'),
(353,18,1,5,NULL,'2023-09-26 10:11:36'),
(354,18,1,6,NULL,'2023-09-26 10:11:36'),
(355,18,1,7,NULL,'2023-09-26 10:11:36'),
(356,18,1,8,NULL,'2023-09-26 10:11:36'),
(357,18,1,46,NULL,'2023-09-26 10:11:36'),
(358,18,1,47,NULL,'2023-09-26 10:11:36'),
(359,18,10,27,NULL,'2023-09-26 10:11:36'),
(360,18,10,28,NULL,'2023-09-26 10:11:36'),
(361,18,10,29,NULL,'2023-09-26 10:11:36'),
(362,18,10,30,NULL,'2023-09-26 10:11:36'),
(363,18,10,31,NULL,'2023-09-26 10:11:36'),
(364,18,11,32,NULL,'2023-09-26 10:11:36'),
(365,18,11,33,NULL,'2023-09-26 10:11:36'),
(366,18,11,34,NULL,'2023-09-26 10:11:36'),
(367,18,11,35,NULL,'2023-09-26 10:11:36'),
(368,18,11,36,NULL,'2023-09-26 10:11:36'),
(369,18,13,42,NULL,'2023-09-26 10:11:36'),
(370,18,13,43,NULL,'2023-09-26 10:11:36'),
(371,18,13,48,NULL,'2023-09-26 10:11:36');
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
  `instruction` text NOT NULL DEFAULT 'Examination instruction...',
  `no_of_questions` tinyint(4) NOT NULL,
  `time_allowed` int(11) NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime DEFAULT NULL,
  `exam_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`exam_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `exam_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam`
--

LOCK TABLES `exam` WRITE;
/*!40000 ALTER TABLE `exam` DISABLE KEYS */;
INSERT INTO `exam` VALUES
(1,'Computer Science','Welcome to the Computer Science exam. Below you will find important information and guidelines to\r\nensure a smooth examination process.\r\n\r\nTechnical Requirements:\r\n   - Stable internet connection will be required throughout this examination.\r\n   - Chrome and Firefox web browsers are recommended (though not mandatory).\r\n\r\nExam Format:\r\n   - The exam consists of a total of 8 multiple-choice questions which must all be attempted.\r\n\r\nExam Rules and Regulations:\r\n   - You are under no circumstance allowed to refer to external resources such as textbooks, notes, or\r\n     online materials throughout the duration of this examination.\r\n   - You are advised to pay strict adherence to academic integrity and no plagiarism.\r\n   - Consequences of violation of the rules stated above will lead to the cancellation of your examination.\r\n\r\nSubmission Instructions:\r\n   - After attempting the last question of the examination, the \"SUBMIT\" button will be made available to\r\n     you. Click the button to submit your examinations.\r\n   - However, it is important that you know that the \"SUBMIT\" button will not be made available until you\r\n     have attempted all questions in the examination.\r\n\r\nTroubleshooting:\r\n   - In case of any technical difficulties, please contact Provide contact person or IT support details.\r\n\r\n\r\n\r\n\r\nPlease read the exam instructions carefully and make sure to follow all guidelines.\r\nIf you have any questions or require clarification, please reach out to us beforehand.\r\n\r\n\r\nWishing you success in your Computer Science exam!\r\n\r\nBest regards,\r\nAlexander Ikpeama\r\nExaminer',8,60,'2023-05-31 10:02:44','2023-09-27 09:53:58','2023-09-27','11:00:00','00:48:00',2),
(10,'Machine Learning','Examination instruction...',5,60,'2023-09-19 22:25:05','2023-09-22 03:21:09','2023-09-22','04:22:00','05:22:00',2),
(11,'Psychology','Examination instruction...',5,120,'2023-09-19 22:30:20','2023-09-21 17:15:51','2023-09-21','18:00:00','20:00:00',2),
(13,'Philosophy 311','Examination instruction...',3,1,'2023-09-19 22:37:59','2023-09-20 15:50:13','2023-09-22','09:30:00','09:31:00',2),
(48,'asdfasdasdf','asdfasdf',1,60,'2023-10-03 07:55:58','2023-10-04 23:06:07','2023-10-07','00:04:00','01:04:00',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES
(3,'Which of the following is an example of a computer hardware?','Linux','Windows','LibreOffice','Mouse','MS Word','CorelDraw',NULL,NULL,1),
(4,'Who invented Napier\'s bone?','Stephen Napier','Joe Napier','Matthew Napier','John Napier',NULL,NULL,NULL,NULL,1),
(5,'Is C a high level programming language?','True','False',NULL,NULL,NULL,NULL,NULL,NULL,1),
(6,'Which of the following programming languages does not have garbage collector?','C Programming Language','Python Programming Language','JavaScript Programming Language','Ruby',NULL,NULL,NULL,NULL,1),
(7,'Python cannot be used in building web applications.','True','False',NULL,NULL,NULL,NULL,NULL,NULL,1),
(8,'Which of the following is a computer virus capable of doing?','Turning off a computer\'s display.','Duplicating user files.','Rendering a computer unusable.','Turning off a computer.','Capturing video/images using the user\'s webcam with user\'s permission.','Deleting user files without user\'s permission.','creating a back door for a hacker to gain access to your system.','All of the above.',1),
(27,'Machine Learning question 1?','Machine option 1','Machine option 2',NULL,NULL,NULL,NULL,NULL,NULL,10),
(28,'Machine Learning question 2?','Machine option A','Machine option B',NULL,NULL,NULL,NULL,NULL,NULL,10),
(29,'Machine Learning question 3?','Machine option A','Machine option B','Machine option C',NULL,NULL,NULL,NULL,NULL,10),
(30,'Machine Learning question 4?','Machine option A','Machine option B','Machine option C',NULL,NULL,NULL,NULL,NULL,10),
(31,'Machine Learning question 5?','Machine option A','Machine option B',NULL,NULL,NULL,NULL,NULL,NULL,10),
(32,'Psychology question 1?','Option A','Option B',NULL,NULL,NULL,NULL,NULL,NULL,11),
(33,'Psychology question 2?','Option A','Option B','Option C','Option D','Option E',NULL,NULL,NULL,11),
(34,'Psychology question 3?','Option A','Option B','Option C','Option D',NULL,NULL,NULL,NULL,11),
(35,'Psychology question 4?','Option A','Option B','Option C',NULL,NULL,NULL,NULL,NULL,11),
(36,'Psychology question 5?','Option A','Option B','Option C',NULL,NULL,NULL,NULL,NULL,11),
(42,'Why was Philosophy called \'Philosophy\'?','I know','I don\'t know',NULL,NULL,NULL,NULL,NULL,NULL,13),
(43,'In fact why Philosophy?','I don\'t know','I also don\'t know',NULL,NULL,NULL,NULL,NULL,NULL,13),
(46,'This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.\r\nJust consider it as a bonus.\r\nAsdasdfasdf\r\nThis is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. \r\nJe vous remercie.This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                                                           It was created for the sake of testing a newly added feature.                                                                                                                                                     \r\nJust consider it as a bonus.\r\nJe vous remercie. This is not a question.                                                                                                                                 ','Oui','Non',NULL,NULL,NULL,NULL,NULL,NULL,1),
(47,'Anything goes in here','This is just a joke','An option','The most annoying answer',NULL,NULL,NULL,NULL,NULL,1),
(48,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,13),
(101,'asdfadsasf','asdfdsadsf','asdfadsfas','asdfasdfasd',NULL,NULL,NULL,NULL,NULL,48);
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
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES
(94,77,1,7,8),
(95,77,10,0,5),
(96,77,11,0,5),
(97,77,13,0,3),
(118,18,1,0,8),
(119,18,10,0,5),
(120,18,11,0,5),
(121,18,13,0,3);
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
  `username` varchar(128) NOT NULL DEFAULT 'guest',
  `firstname` varchar(128) NOT NULL DEFAULT 'Guest',
  `lastname` varchar(128) NOT NULL,
  `middlename` varchar(128) NOT NULL,
  `password` longtext NOT NULL,
  `email` varchar(128) NOT NULL DEFAULT 'guest@ecity.com',
  `gender` enum('M','F') DEFAULT NULL,
  `is_student` enum('T','F') DEFAULT NULL,
  `is_examiner` enum('T','F') DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `last_logout` datetime DEFAULT NULL,
  `logged_in` enum('T','F') NOT NULL,
  `teachers` text DEFAULT NULL,
  `students` text DEFAULT NULL,
  `dp` varchar(256) DEFAULT 'profile-icon-grey.webp',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `email_2` (`email`),
  UNIQUE KEY `username_2` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=192 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(2,'Xandex','Alexander','Ikpeama','Udochukwu','$2b$12$l1yOTC6b2ptV8wOG2e0TP.YJ3fh4TMtayHGLU3.O5Lhj8VRMEQRm.','alexanderikpeama@gmail.com','M','T','T','2023-05-31 09:32:19','2023-10-05 12:22:47','2023-10-05 13:12:00','2023-10-05 13:12:02','F','','18, 77, 183, 187, 188, 189, 190','dp-2.jpg'),
(18,'guest','Guest','Guest','Guest','guest','guest@ecity.com',NULL,'T',NULL,'2023-06-08 09:23:02','2023-06-08 09:23:02','2023-09-26 10:13:04','2023-09-26 10:14:51','F','2,','','profile-icon-grey.webp'),
(77,'ok','Okay','Okay','Really','$2b$12$l1yOTC6b2ptV8wOG2e0TP.EDpGh0Ja/JQH.fVW2EbZVte8giVlqm.','ok@gmail.com',NULL,'T',NULL,'2023-09-18 08:14:42','2023-10-05 13:04:57','2023-10-05 13:12:11','2023-10-05 13:12:14','F','2,','','dp-77.jpg'),
(187,'phil','Philip','Phil','','$2b$12$l1yOTC6b2ptV8wOG2e0TP.Y6/W5R3BulPpeI2iYOI3YMpJXlbqXcC','philiphil@gmail.com','M','T',NULL,'2023-10-03 23:09:02','2023-10-03 23:25:55','2023-10-03 23:28:24',NULL,'T','2,',NULL,'profile-icon-grey.webp'),
(188,'+#xe/=3T','jude','jude','jude','$2b$12$l1yOTC6b2ptV8wOG2e0TP.ZeIF95TUpxWb1ho1PTqU3yuPF6MF14m','jude@gmail.com','M','T',NULL,'2023-10-04 20:15:18','2023-10-04 20:20:17','2023-10-04 20:24:25',NULL,'T','2,',NULL,'profile-icon-grey.webp'),
(189,'x15xc!(xc','Enoch','Mdjim','','$2b$12$l1yOTC6b2ptV8wOG2e0TP.Y6/W5R3BulPpeI2iYOI3YMpJXlbqXcC','enoch@yahoo.com','M','T',NULL,'2023-10-04 20:25:18','2023-10-04 20:42:44','2023-10-04 20:46:28','2023-10-04 20:48:50','F','2,',NULL,'profile-icon-grey.webp'),
(190,'loveth','Loveth','Emmanuel','Chidinma','$2b$12$l1yOTC6b2ptV8wOG2e0TP.Y6/W5R3BulPpeI2iYOI3YMpJXlbqXcC','loveth@gmail.com','F','T',NULL,'2023-10-05 06:43:16','2023-10-05 07:09:13','2023-10-05 07:08:46','2023-10-05 09:22:16','F','2,',NULL,'profile-icon-grey.webp');
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

-- Dump completed on 2023-10-05 15:10:41
