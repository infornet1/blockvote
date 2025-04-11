/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.5-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: blockchain_vote
-- ------------------------------------------------------
-- Server version	11.4.5-MariaDB-0ubuntu0.24.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `blocks`
--

DROP TABLE IF EXISTS `blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `blocks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `previous_hash` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp(),
  `proof` int(11) DEFAULT NULL,
  `voter_id` varchar(50) NOT NULL,
  `candidate_id` varchar(50) NOT NULL,
  `hash` varchar(64) NOT NULL,
  `miner_address` varchar(64) DEFAULT NULL,
  `nonce` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voter_id` (`voter_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blocks`
--

LOCK TABLES `blocks` WRITE;
/*!40000 ALTER TABLE `blocks` DISABLE KEYS */;
INSERT INTO `blocks` VALUES
(1,'0','2025-04-09 05:01:53',123,'K7411','3','b41a883b53052024359ba30f34de9d0ce8818b6e1309ad14cd0b4cfd09d35de4',NULL,0),
(2,'b41a883b53052024359ba30f34de9d0ce8818b6e1309ad14cd0b4cfd09d35de4','2025-04-09 05:02:20',123,'K7445','3','29caa5b441e00aca787690fb2087e591d15b266034f69de6f8cae1491b62e314',NULL,0),
(3,'29caa5b441e00aca787690fb2087e591d15b266034f69de6f8cae1491b62e314','2025-04-09 05:02:34',123,'K7455','2','61e98e0358fc7983171fadc14b284609eea2cd797657a44e2f27e657da4cf2bc',NULL,0),
(4,'61e98e0358fc7983171fadc14b284609eea2cd797657a44e2f27e657da4cf2bc','2025-04-09 05:36:31',123,'K7415','1','50543884a0e22c007a8ceedc4aac9b78231272e0d91d52827503213b74c7fb67',NULL,0),
(5,'50543884a0e22c007a8ceedc4aac9b78231272e0d91d52827503213b74c7fb67','2025-04-09 05:56:46',0,'AB01','4','569a1d71e021d54e29b4885866b3ba8e8b68d6c35f9a1fd360e26df0d681b675','miner_1234',49016),
(6,'569a1d71e021d54e29b4885866b3ba8e8b68d6c35f9a1fd360e26df0d681b675','2025-04-09 06:00:27',0,'K7450','2','37259958c2e8545ef293b5815d263502a3207aaca7c90e7718bf72058922ad1c','miner_4010',9187),
(7,'37259958c2e8545ef293b5815d263502a3207aaca7c90e7718bf72058922ad1c','2025-04-09 06:33:14',0,'K7447','1','88b7e0b970cceeeab9addfdf8b84ffdd1cabf336cb7c6922e14e9d0922768be4','miner_9684',17797),
(8,'88b7e0b970cceeeab9addfdf8b84ffdd1cabf336cb7c6922e14e9d0922768be4','2025-04-09 09:25:04',0,'Juan ','1','ba50e3ea8ed0955db8db47db6f11efbdf1e6600576b8df8a5a992838cf0fea06','miner_4545',88638),
(9,'ba50e3ea8ed0955db8db47db6f11efbdf1e6600576b8df8a5a992838cf0fea06','2025-04-09 14:47:13',0,'AL001','3','ebe12b190256f9fd7362badc05cd27d94b5ec75d50ae0c841732684f2b582fff','miner_6348',58735),
(10,'ebe12b190256f9fd7362badc05cd27d94b5ec75d50ae0c841732684f2b582fff','2025-04-10 14:19:57',0,'AB002','2','726846cbfe46284e7a986132dd37c881453dff001520ffc4272dafbda092ef59','miner_3299',82582),
(11,'726846cbfe46284e7a986132dd37c881453dff001520ffc4272dafbda092ef59','2025-04-10 14:32:43',0,'jh001','4','8bf2306f407e735ce56ba2fda37567cc455f7f1ddd1be71745cc5efd07526347','miner_3107',14242),
(12,'8bf2306f407e735ce56ba2fda37567cc455f7f1ddd1be71745cc5efd07526347','2025-04-10 14:33:29',0,'jh002','2','0b67c1ea8a5af04030576dca8f2d7b189627b550a8a9d4b2e9e7f54644226f55','miner_9473',21671),
(13,'0b67c1ea8a5af04030576dca8f2d7b189627b550a8a9d4b2e9e7f54644226f55','2025-04-11 00:29:36',0,'TR001','3','59d68b5451254def7570b42e67398cb8adc2fdb57e4fae85f0965f1d098453cb','miner_6840',17763),
(14,'59d68b5451254def7570b42e67398cb8adc2fdb57e4fae85f0965f1d098453cb','2025-04-11 00:31:14',0,'TR002','5','2404fcde65a5c7725b12cb08d9951d397e769057fa45c32270c95071d1cebc85','miner_5698',65425),
(15,'2404fcde65a5c7725b12cb08d9951d397e769057fa45c32270c95071d1cebc85','2025-04-11 01:06:44',0,'TR003','5','646f0a15d03e00d9f4102eedc142a9291f84eb394fa7218a7e3ac60057fb1997','miner_6944',23439),
(16,'646f0a15d03e00d9f4102eedc142a9291f84eb394fa7218a7e3ac60057fb1997','2025-04-11 01:12:56',0,'TR004','5','c0966f814590724b4c3456282479f8d5856783aad16ab0a917ef918a46baa941','miner_4122',63594);
/*!40000 ALTER TABLE `blocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidates`
--

DROP TABLE IF EXISTS `candidates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidates` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `votes` int(11) DEFAULT 0,
  `active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidates`
--

LOCK TABLES `candidates` WRITE;
/*!40000 ALTER TABLE `candidates` DISABLE KEYS */;
INSERT INTO `candidates` VALUES
('1','Juan',3,1),
('2','Pedro',4,1),
('3','Carlos',4,1),
('4','Jorge',2,1),
('5','Gustavo',3,1);
/*!40000 ALTER TABLE `candidates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `miners`
--

DROP TABLE IF EXISTS `miners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `miners` (
  `address` varchar(64) NOT NULL,
  `balance` decimal(10,2) DEFAULT 0.00,
  `total_blocks_mined` int(11) DEFAULT 0,
  PRIMARY KEY (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `miners`
--

LOCK TABLES `miners` WRITE;
/*!40000 ALTER TABLE `miners` DISABLE KEYS */;
INSERT INTO `miners` VALUES
('miner_1234',1.00,1),
('miner_3107',1.00,1),
('miner_3299',1.00,1),
('miner_4010',1.00,1),
('miner_4122',1.00,1),
('miner_4545',1.00,1),
('miner_5698',1.00,1),
('miner_6348',1.00,1),
('miner_6840',1.00,1),
('miner_6944',1.00,1),
('miner_9473',1.00,1),
('miner_9684',1.00,1);
/*!40000 ALTER TABLE `miners` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-10 23:17:01
