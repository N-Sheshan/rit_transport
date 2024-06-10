-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 29, 2024 at 11:09 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rit_transport`
--

-- --------------------------------------------------------

--
-- Table structure for table `application_master_vechicle`
--

CREATE TABLE `application_master_vechicle` (
  `vehicle_no` varchar(100) NOT NULL,
  `Usage` varchar(100) DEFAULT NULL,
  `Driver_Name` varchar(100) DEFAULT NULL,
  `fule_type` varchar(100) NOT NULL,
  `vehicle_type` varchar(100) DEFAULT NULL,
  `Driver_Number` varchar(100) DEFAULT NULL,
  `route_name` varchar(1000) DEFAULT NULL,
  `Previous_km` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_master_vechicle`
--

INSERT INTO `application_master_vechicle` (`vehicle_no`, `Usage`, `Driver_Name`, `fule_type`, `vehicle_type`, `Driver_Number`, `route_name`, `Previous_km`) VALUES
('TN 1234', '2', '3053', 'Diesel', 'Four Wheeler', '1234567890', 'madurai', 50),
('TN 67 AM 9785', '01', 'Spare', 'Diesel', 'Six Wheeler', 'Nil', 'RJPM', 25000);

-- --------------------------------------------------------

--
-- Table structure for table `application_transport_approval`
--

CREATE TABLE `application_transport_approval` (
  `bill_id` varchar(100) NOT NULL,
  `vehicle_no` varchar(100) DEFAULT NULL,
  `vehicle_type` varchar(100) DEFAULT NULL,
  `fule_type` varchar(100) DEFAULT NULL,
  `driver_id` varchar(100) NOT NULL,
  `buying_date` date DEFAULT NULL,
  `starting_KM` double DEFAULT NULL,
  `reason` varchar(500) DEFAULT NULL,
  `fuel_quantity` int(11) DEFAULT NULL,
  `route` varchar(200) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `Mileage` varchar(50) DEFAULT NULL,
  `Ending_KM` double DEFAULT NULL,
  `proof_date` varchar(500) DEFAULT NULL,
  `distilled_water_quantity` varchar(50) DEFAULT NULL,
  `engine_oil_quantity` varchar(200) DEFAULT NULL,
  `grease_company` varchar(200) DEFAULT NULL,
  `grease_quantity` varchar(200) DEFAULT NULL,
  `pdf_generated_proof` varchar(50) DEFAULT NULL,
  `billed_date` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_transport_approval`
--

INSERT INTO `application_transport_approval` (`bill_id`, `vehicle_no`, `vehicle_type`, `fule_type`, `driver_id`, `buying_date`, `starting_KM`, `reason`, `fuel_quantity`, `route`, `status`, `Mileage`, `Ending_KM`, `proof_date`, `distilled_water_quantity`, `engine_oil_quantity`, `grease_company`, `grease_quantity`, `pdf_generated_proof`, `billed_date`) VALUES
('RIT202405001', 'TN 67 AM 9785', 'Six Wheeler', 'Diesel', '2500', '2024-05-28', 25000, 'Tank Full', 50, 'RJPM', 'Yes', '20.0', 26000, '2024-05-28 18:30:23', 'None', 'None', 'None', 'None', NULL, '2024-05-28 18:26:41'),
('RIT202405002', 'TN 67 AM 9785', 'Six Wheeler', 'Diesel', 'Spare', '2024-05-30', 26000, 'Tank Full', 55, 'RJPM', 'Yes', '18.18', 27000, '2024-05-28 18:33:11', 'None', 'None', 'None', 'None', NULL, '2024-05-28 18:32:35'),
('RIT202405003', 'TN 67 AM 9785', 'Six Wheeler', 'Diesel', 'ggferg', '2024-05-29', NULL, 'gdgfdgf', NULL, 'RJPM', 'Yes', NULL, NULL, NULL, '10', '1', 'LLB', '23', NULL, '2024-05-28 18:43:12'),
('RIT202405004', 'TN 1234', 'Four Wheeler', 'Diesel', 'hhtr', '2024-05-29', 50, 'htht', 25, 'madurai', 'Yes', '2.0', 100, '2024-05-29 10:19:52', 'None', 'None', 'None', 'None', NULL, '2024-05-29 10:19:08'),
('RIT202405005', 'TN 1234', 'Four Wheeler', 'Diesel', 'gdsgds', '2024-05-31', NULL, 'dgdlkgnn', NULL, 'madurai', 'Yes', NULL, NULL, NULL, '2', '1', 'None', 'None', NULL, '2024-05-29 12:27:54'),
('RIT202405006', 'TN 1234', 'Four Wheeler', 'Diesel', '123CFFGX', '2024-05-29', NULL, 'GGFGFG', NULL, 'madurai', 'Yes', NULL, NULL, NULL, '23', '1', 'LLB', '1', NULL, '2024-05-29 14:10:22'),
('RIT202405007', 'TN 1234', 'Four Wheeler', 'Diesel', '2555', '2024-05-29', NULL, 'Tank Full', NULL, 'madurai', 'Yes', NULL, NULL, NULL, 'None', 'None', 'None', 'None', NULL, '2024-05-29 14:22:28');

-- --------------------------------------------------------

--
-- Table structure for table `application_user`
--

CREATE TABLE `application_user` (
  `id` bigint(20) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `conform_Password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_user`
--

INSERT INTO `application_user` (`id`, `Name`, `user_name`, `email`, `Password`, `conform_Password`) VALUES
(1, 'sheshan', '', '953621243053@ritrjpm.ac.in', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
(2, 'GOVINDARAJU N', '', 'transport@ritrjpm.ac.in', '64637c419a7dbcdf2e773bfdf3ff7b0706d97e46a5f2303e6e55ac373442e0e4', '64637c419a7dbcdf2e773bfdf3ff7b0706d97e46a5f2303e6e55ac373442e0e4');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add transport_approval', 7, 'add_transport_approval'),
(26, 'Can change transport_approval', 7, 'change_transport_approval'),
(27, 'Can delete transport_approval', 7, 'delete_transport_approval'),
(28, 'Can view transport_approval', 7, 'view_transport_approval'),
(29, 'Can add master_ vechicle', 8, 'add_master_vechicle'),
(30, 'Can change master_ vechicle', 8, 'change_master_vechicle'),
(31, 'Can delete master_ vechicle', 8, 'delete_master_vechicle'),
(32, 'Can view master_ vechicle', 8, 'view_master_vechicle'),
(33, 'Can add user', 9, 'add_user'),
(34, 'Can change user', 9, 'change_user'),
(35, 'Can delete user', 9, 'delete_user'),
(36, 'Can view user', 9, 'view_user'),
(37, 'Can add custom user', 10, 'add_customuser'),
(38, 'Can change custom user', 10, 'change_customuser'),
(39, 'Can delete custom user', 10, 'delete_customuser'),
(40, 'Can view custom user', 10, 'view_customuser');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(10, 'application', 'customuser'),
(8, 'application', 'master_vechicle'),
(7, 'application', 'transport_approval'),
(9, 'application', 'user'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-05-22 08:25:44.946040'),
(2, 'auth', '0001_initial', '2024-05-22 08:25:50.667547'),
(3, 'admin', '0001_initial', '2024-05-22 08:25:52.401041'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-05-22 08:25:52.431043'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-05-22 08:25:52.463042'),
(6, 'application', '0001_initial', '2024-05-22 08:25:52.618474'),
(7, 'contenttypes', '0002_remove_content_type_name', '2024-05-22 08:25:53.102987'),
(8, 'auth', '0002_alter_permission_name_max_length', '2024-05-22 08:25:53.668674'),
(9, 'auth', '0003_alter_user_email_max_length', '2024-05-22 08:25:53.795674'),
(10, 'auth', '0004_alter_user_username_opts', '2024-05-22 08:25:53.824708'),
(11, 'auth', '0005_alter_user_last_login_null', '2024-05-22 08:25:54.478755'),
(12, 'auth', '0006_require_contenttypes_0002', '2024-05-22 08:25:54.502740'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2024-05-22 08:25:54.530738'),
(14, 'auth', '0008_alter_user_username_max_length', '2024-05-22 08:25:54.672770'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2024-05-22 08:25:54.761767'),
(16, 'auth', '0010_alter_group_name_max_length', '2024-05-22 08:25:54.853794'),
(17, 'auth', '0011_update_proxy_permissions', '2024-05-22 08:25:54.883793'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2024-05-22 08:25:54.986793'),
(19, 'sessions', '0001_initial', '2024-05-22 08:25:55.519889'),
(20, 'application', '0002_transport_approval_status', '2024-05-22 08:30:36.341307'),
(21, 'application', '0003_alter_transport_approval_buying_date_and_more', '2024-05-22 15:23:42.660611'),
(22, 'application', '0004_rename_overall_km_transport_approval_ending_km_and_more', '2024-05-23 08:29:10.306065'),
(23, 'application', '0005_master_vechicle_and_more', '2024-05-23 10:50:21.583327'),
(24, 'application', '0006_transport_approval_proof_date', '2024-05-24 08:14:24.359818'),
(25, 'application', '0007_transport_approval_distilled_water_quantity_and_more', '2024-05-25 20:27:22.482290'),
(26, 'application', '0008_rename_pdf_generrated_proof_transport_approval_pdf_generated_proof', '2024-05-25 20:28:41.069889'),
(27, 'application', '0009_transport_approval_billed_date', '2024-05-27 05:01:39.385609'),
(28, 'application', '0010_user', '2024-05-28 05:32:27.178492'),
(29, 'application', '0011_master_vechicle_previous_us', '2024-05-28 11:34:33.631910'),
(30, 'application', '0012_rename_previous_us_master_vechicle_previous_km', '2024-05-28 11:47:52.046496'),
(31, 'application', '0013_alter_master_vechicle_previous_km', '2024-05-28 11:58:29.842121'),
(32, 'application', '0014_customuser_delete_user', '2024-05-28 15:46:12.316556'),
(33, 'application', '0015_user_delete_customuser', '2024-05-29 01:45:11.154176');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('06u42p9h9es7waajqdukl6l820z7b83r', 'eyJ1c2VyX2F1dGgiOmZhbHNlfQ:1sCErd:IcHwwnItJfrGB6Bbw8V56pofEfNhoByOuNzxy6dwq1k', '2024-06-12 08:40:53.355839'),
('hkhrfwi31g872x9jlo4410fqn56ms78z', 'eyJ1c2VyX2F1dGgiOmZhbHNlfQ:1sCDJv:5cWX1pGpOPtqJlHx2yBOp-1eGkp4fNjIWq2yTd082G0', '2024-06-12 07:01:59.085437'),
('ka7krie037651f7dn3h2j03xajicig3l', 'eyJ1c2VyX2F1dGgiOnRydWV9:1sCDZg:brK8ezRjgoE1ka1tE4C4bMzPNkouemN9q8GngMkPpZY', '2024-06-12 07:18:16.352742'),
('oe6tvj975b6cvkjphijudmfinbvw3ckv', 'e30:1sBpqe:rfRWsIXebfbM4MVhBAbVwco9KjMz5ZCOMVEnh__rGzc', '2024-06-11 05:58:12.389491'),
('qnkcggkj6kdvbb2wak7fa67to8us07lr', 'eyJ1c2VyX2F1dGgiOnRydWV9:1sCF1a:GKL9lOcMiCYQANFVpUVuXzcztqF9U6cmA1NNj_vJjmk', '2024-06-12 08:51:10.568696');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `application_master_vechicle`
--
ALTER TABLE `application_master_vechicle`
  ADD PRIMARY KEY (`vehicle_no`);

--
-- Indexes for table `application_transport_approval`
--
ALTER TABLE `application_transport_approval`
  ADD PRIMARY KEY (`bill_id`);

--
-- Indexes for table `application_user`
--
ALTER TABLE `application_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `application_user`
--
ALTER TABLE `application_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
