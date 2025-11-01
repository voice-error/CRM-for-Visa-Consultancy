-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 15, 2025 at 10:26 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_crm`
--
CREATE DATABASE IF NOT EXISTS `db_crm` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `db_crm`;

-- --------------------------------------------------------

--
-- Table structure for table `agent`
--

CREATE TABLE `agent` (
  `id` bigint(10) NOT NULL,
  `user_id` bigint(10) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `phone` bigint(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agent`
--

INSERT INTO `agent` (`id`, `user_id`, `first_name`, `last_name`, `phone`) VALUES
(1, 17, 'RajKumar', 'Karki', 9878448488),
(2, 22, 'Pradip', 'Lamichhane', 5888747484);

-- --------------------------------------------------------

--
-- Table structure for table `agent_report`
--

CREATE TABLE `agent_report` (
  `id` bigint(20) NOT NULL,
  `agent_id` bigint(10) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agent_report`
--

INSERT INTO `agent_report` (`id`, `agent_id`, `content`, `date`) VALUES
(1, 1, 'VISA CONSULTANCY AGENT REPORT\nReport Date: [YYYY-MM-DD]\nAgent Name: [Agent\'s Full Name]\nAgent ID: [Agent ID Number]\n\n---\n\nCLIENT INFORMATION\n\n* Client Full Name: [Client\'s Full Name]\n* Client ID/Reference: [Client ID or Reference Number]\n* Contact Number: [Client\'s Phone Number]\n* Email Address: [Client\'s Email Address]\n* Nationality: [Client\'s Nationality]\n\n---\n\nVISA APPLICATION DETAILS\n\n* Visa Type Applied For: [e.g., Student Visa, Tourist Visa, Work Permit, Family Sponsorship]\n* Destination Country: [Country of Application]\n* Intended Travel Date: [YYYY-MM-DD] (Approximate)\n* Application Status: [e.g., New Application, In Progress, Submitted, Approved, Rejected, On Hold]\n* Application Submission Date: [YYYY-MM-DD]\n* Expected Decision Date: [YYYY-MM-DD] (If applicable)\n* Current Stage: [e.g., Document Collection, Application Filling, Interview Scheduled, Biometrics Done, Waiting for Decision]\n\n---\n\nDOCUMENTATION CHECKLIST & STATUS\n\n* Passport: [Received', '2025-07-12');

-- --------------------------------------------------------

--
-- Table structure for table `chat_message`
--

CREATE TABLE `chat_message` (
  `id` int(11) NOT NULL,
  `room_id` varchar(5) NOT NULL,
  `sender_id` bigint(10) NOT NULL,
  `message` text NOT NULL,
  `sent_on` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_message`
--

INSERT INTO `chat_message` (`id`, `room_id`, `sender_id`, `message`, `sent_on`, `is_read`) VALUES
(35, 'FT9PS', 16, 'mero kina rejict vayeo', '2025-10-03 12:54:18', 0),
(36, 'FT9PS', 17, 'checkint wait bro', '2025-10-03 12:54:55', 0);

-- --------------------------------------------------------

--
-- Table structure for table `chat_room`
--

CREATE TABLE `chat_room` (
  `id` varchar(5) NOT NULL,
  `agent_id` bigint(10) NOT NULL,
  `client_id` bigint(10) NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_room`
--

INSERT INTO `chat_room` (`id`, `agent_id`, `client_id`, `created_on`) VALUES
('FT9PS', 1, 7, '2025-09-16 13:03:24');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `id` bigint(10) NOT NULL,
  `user_id` bigint(10) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `phone` bigint(10) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`id`, `user_id`, `first_name`, `last_name`, `phone`, `status`) VALUES
(7, 16, 'Nirjung', 'jaigadi', 9978448455, '1'),
(8, 19, 'Narendra', 'Chand', 975484548, '1'),
(9, 20, 'Ankit', 'Ghimire', 97848484, '1'),
(10, 21, 'Naresh', 'Saud', 9865974266, '1'),
(16, 26, 'Prabin', 'Lamichhane', 9769866766, '1'),
(19, 28, 'pradip', 'lc', 9874563210, '1');

-- --------------------------------------------------------

--
-- Table structure for table `country`
--

CREATE TABLE `country` (
  `id` int(8) NOT NULL,
  `code` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `country`
--

INSERT INTO `country` (`id`, `code`, `name`) VALUES
(1, 'AU', 'Australia'),
(2, 'UK', 'United Kingdom'),
(3, 'USA', 'United State Of America');

-- --------------------------------------------------------

--
-- Table structure for table `owner`
--

CREATE TABLE `owner` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `phone` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `owner`
--

INSERT INTO `owner` (`id`, `user_id`, `first_name`, `last_name`, `phone`) VALUES
(1, 18, 'Prabin', 'Lamichhane', 9784848564);

-- --------------------------------------------------------

--
-- Table structure for table `passreset`
--

CREATE TABLE `passreset` (
  `id` int(11) NOT NULL,
  `user_id` bigint(10) NOT NULL,
  `reset_code` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program`
--

CREATE TABLE `program` (
  `id` int(8) NOT NULL,
  `university_id` int(8) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program`
--

INSERT INTO `program` (`id`, `university_id`, `name`) VALUES
(1, 1, 'Bachelor of Computer Applications'),
(2, 1, 'BSc Cyber Security'),
(3, 2, 'BSc Psychology'),
(4, 2, 'BSc in Sports Science'),
(5, 3, 'Bachelor of Computer Science'),
(6, 3, 'Bachelor in Civil Engineering'),
(7, 3, 'Bachelor in Electrical Engineering'),
(9, 5, 'Bachelor of Computer Applications'),
(10, 5, 'BSc Cyber Security'),
(11, 6, 'Bachelor of Computer Science'),
(12, 6, 'Bachelor in Civil Engineering'),
(13, 6, 'Bachelor of Electrical Engineering'),
(14, 7, 'BSc Psychology'),
(15, 7, 'BSc in Sports Science');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `id` bigint(10) NOT NULL,
  `code` varchar(30) NOT NULL,
  `name` varchar(20) NOT NULL DEFAULT 'User'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`id`, `code`, `name`) VALUES
(1, 'XXS', 'client'),
(2, 'M', 'agent'),
(3, 'XXL', 'admin'),
(4, 'LOW', 'User');

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `id` bigint(10) NOT NULL,
  `client_id` bigint(10) NOT NULL,
  `registration` int(9) NOT NULL DEFAULT 2500,
  `doc_process` int(9) NOT NULL DEFAULT 27000,
  `visa_process` int(9) NOT NULL DEFAULT 0,
  `consulting` int(9) NOT NULL DEFAULT 105000,
  `remaining` bigint(10) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`id`, `client_id`, `registration`, `doc_process`, `visa_process`, `consulting`, `remaining`) VALUES
(2, 7, 0, 0, 0, 105000, 105000),
(3, 8, 0, 27000, 875000, 105000, 985200),
(4, 9, 2500, 27000, 0, 105000, 1310200),
(9, 10, 2500, 27000, 1200000, 105000, 0),
(12, 16, 2500, 27000, 1200000, 105000, 1334500),
(15, 19, 0, 27000, 752000, 105000, 884000);

--
-- Triggers `sales`
--
DELIMITER $$
CREATE TRIGGER `visa_cost` BEFORE INSERT ON `sales` FOR EACH ROW SET NEW.visa_process = (
    SELECT u.visa_cost
    FROM university u
    WHERE u.id = (
        SELECT v.university_id
        FROM visa_application v
        WHERE v.client_id = NEW.client_id
        LIMIT 1
    )
)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `university`
--

CREATE TABLE `university` (
  `id` int(8) NOT NULL,
  `name` varchar(50) NOT NULL,
  `country_id` int(8) NOT NULL,
  `visa_cost` int(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `university`
--

INSERT INTO `university` (`id`, `name`, `country_id`, `visa_cost`) VALUES
(1, 'The University of Melbourne', 1, 925000),
(2, 'Duke University', 3, 700000),
(3, 'University of Cambridge', 2, 1200000),
(5, 'University of Sydney', 1, 875000),
(6, 'University of Leeds', 2, 1080000),
(7, 'Brown University', 3, 752000);

-- --------------------------------------------------------

--
-- Table structure for table `unverified`
--

CREATE TABLE `unverified` (
  `uv_id` int(8) NOT NULL,
  `user_id` bigint(10) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` bigint(10) NOT NULL,
  `visa_type` varchar(20) NOT NULL,
  `country_id` int(8) NOT NULL,
  `university_id` int(8) NOT NULL,
  `program_id` int(8) NOT NULL,
  `notes` varchar(50) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `unverified`
--

INSERT INTO `unverified` (`uv_id`, `user_id`, `first_name`, `last_name`, `email`, `phone`, `visa_type`, `country_id`, `university_id`, `program_id`, `notes`, `status`) VALUES
(4, 29, 'ankit', 'ghimire', 'twoingammer@gmail.com', 9812698296, 'Student', 1, 1, 1, 'Please i am poor help me!!!!!!!!!!!!!!!!!!!!!!!!!!', 1),
(5, 31, 'Prabin', 'Lamichhane', 'bhimlamichhane2022@gmail.com', 9865698621, 'Student', 3, 2, 3, 'Please contact first', 0);

-- --------------------------------------------------------

--
-- Table structure for table `unverified_agent`
--

CREATE TABLE `unverified_agent` (
  `ua_id` int(8) NOT NULL,
  `user_id` bigint(10) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` bigint(10) NOT NULL,
  `notes` varchar(50) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `unverified_agent`
--

INSERT INTO `unverified_agent` (`ua_id`, `user_id`, `first_name`, `last_name`, `email`, `phone`, `notes`, `status`) VALUES
(1, 30, 'dhan', 'bogati', 'thahaxamalai@gmail.com', 9868783106, 'i wood loke to join as a admin', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` bigint(10) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `created_on` date NOT NULL DEFAULT current_timestamp(),
  `status` varchar(10) DEFAULT '1',
  `role_id` bigint(10) NOT NULL DEFAULT 4
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `created_on`, `status`, `role_id`) VALUES
(16, 'test@client.com', 'test', '2025-07-08', '1', 1),
(17, 'test@agent.com', 'test', '2025-07-08', '1', 2),
(18, 'test@admin.com', 'test', '2025-07-08', '1', 3),
(19, 'test@client1.com', 'test', '2025-07-10', '1', 1),
(20, 'test@client2.com', 'test', '2025-07-10', '1', 1),
(21, 'test@client3.com', 'test', '2025-07-10', '1', 1),
(22, 'test@agent1.com', 'test', '2025-07-10', '1', 2),
(26, 'prabin700003@gmail.com', 'Prabin@123', '2025-09-04', '1', 1),
(28, 'secondsonly3423@gmail.com', 'lalChi123?', '2025-09-08', '1', 1),
(29, 'twoingammer@gmail.com', 'Ankit@123', '2025-09-08', '1', 4),
(30, 'thahaxamalai@gmail.com', 'pradipLc123', '2025-09-08', '1', 4),
(31, 'bhimlamichhane2022@gmail.com', 'SunSun@123', '2025-09-27', '1', 4);

-- --------------------------------------------------------

--
-- Table structure for table `visa_application`
--

CREATE TABLE `visa_application` (
  `id` bigint(20) NOT NULL,
  `client_id` bigint(20) NOT NULL,
  `agent_id` bigint(20) NOT NULL,
  `country_id` int(8) NOT NULL,
  `university_id` int(8) NOT NULL,
  `program_id` int(8) NOT NULL,
  `progress` varchar(50) NOT NULL DEFAULT 'verifying documents',
  `apply_date` date NOT NULL DEFAULT current_timestamp(),
  `status` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `visa_application`
--

INSERT INTO `visa_application` (`id`, `client_id`, `agent_id`, `country_id`, `university_id`, `program_id`, `progress`, `apply_date`, `status`) VALUES
(1, 7, 1, 3, 2, 3, 'in progress', '2025-07-08', 1),
(2, 8, 1, 2, 3, 5, 'in progress', '2025-07-10', 1),
(3, 9, 2, 3, 2, 4, 'in progress', '2025-07-10', 1),
(4, 10, 2, 2, 3, 6, 'completed', '2025-07-10', 1),
(7, 16, 2, 2, 3, 7, 'verifying documents', '2025-09-07', 1),
(10, 19, 1, 3, 7, 14, 'in progress', '2025-09-08', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agent`
--
ALTER TABLE `agent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`user_id`);

--
-- Indexes for table `agent_report`
--
ALTER TABLE `agent_report`
  ADD PRIMARY KEY (`id`),
  ADD KEY `agent_id` (`agent_id`);

--
-- Indexes for table `chat_message`
--
ALTER TABLE `chat_message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `chat_room`
--
ALTER TABLE `chat_room`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `agent_id` (`agent_id`,`client_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`user_id`);

--
-- Indexes for table `country`
--
ALTER TABLE `country`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `owner`
--
ALTER TABLE `owner`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `passreset`
--
ALTER TABLE `passreset`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `program`
--
ALTER TABLE `program`
  ADD PRIMARY KEY (`id`),
  ADD KEY `university_id` (`university_id`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `role_id` (`id`),
  ADD UNIQUE KEY `r_name` (`name`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `university`
--
ALTER TABLE `university`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `country_id` (`country_id`);

--
-- Indexes for table `unverified`
--
ALTER TABLE `unverified`
  ADD PRIMARY KEY (`uv_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `unverified_agent`
--
ALTER TABLE `unverified_agent`
  ADD PRIMARY KEY (`ua_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_name` (`username`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `visa_application`
--
ALTER TABLE `visa_application`
  ADD PRIMARY KEY (`id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `university_id` (`university_id`),
  ADD KEY `program_id` (`program_id`),
  ADD KEY `country_id` (`country_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agent`
--
ALTER TABLE `agent`
  MODIFY `id` bigint(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `agent_report`
--
ALTER TABLE `agent_report`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chat_message`
--
ALTER TABLE `chat_message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `id` bigint(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `country`
--
ALTER TABLE `country`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `passreset`
--
ALTER TABLE `passreset`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `program`
--
ALTER TABLE `program`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `id` bigint(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `id` bigint(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `university`
--
ALTER TABLE `university`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `unverified`
--
ALTER TABLE `unverified`
  MODIFY `uv_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `unverified_agent`
--
ALTER TABLE `unverified_agent`
  MODIFY `ua_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` bigint(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `visa_application`
--
ALTER TABLE `visa_application`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agent`
--
ALTER TABLE `agent`
  ADD CONSTRAINT `foreign ley` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `agent_report`
--
ALTER TABLE `agent_report`
  ADD CONSTRAINT `agent_report_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`id`);

--
-- Constraints for table `chat_message`
--
ALTER TABLE `chat_message`
  ADD CONSTRAINT `chat_message_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_message_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `chat_room` (`id`);

--
-- Constraints for table `chat_room`
--
ALTER TABLE `chat_room`
  ADD CONSTRAINT `chat_room_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_room_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `client_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `owner`
--
ALTER TABLE `owner`
  ADD CONSTRAINT `owner_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `passreset`
--
ALTER TABLE `passreset`
  ADD CONSTRAINT `passreset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `program`
--
ALTER TABLE `program`
  ADD CONSTRAINT `program_ibfk_1` FOREIGN KEY (`university_id`) REFERENCES `university` (`id`);

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`);

--
-- Constraints for table `university`
--
ALTER TABLE `university`
  ADD CONSTRAINT `university_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`);

--
-- Constraints for table `unverified`
--
ALTER TABLE `unverified`
  ADD CONSTRAINT `unverified_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `unverified_agent`
--
ALTER TABLE `unverified_agent`
  ADD CONSTRAINT `unverified_agent_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);

--
-- Constraints for table `visa_application`
--
ALTER TABLE `visa_application`
  ADD CONSTRAINT `visa_application_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`id`),
  ADD CONSTRAINT `visa_application_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  ADD CONSTRAINT `visa_application_ibfk_3` FOREIGN KEY (`university_id`) REFERENCES `university` (`id`),
  ADD CONSTRAINT `visa_application_ibfk_4` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
  ADD CONSTRAINT `visa_application_ibfk_5` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
