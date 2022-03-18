-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 18, 2022 at 10:07 AM
-- Server version: 8.0.17
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `temperature`
--

-- --------------------------------------------------------

--
-- Table structure for table `factory`
--

CREATE TABLE `factory` (
  `id` int(11) NOT NULL,
  `name` text COLLATE utf8_unicode_ci NOT NULL,
  `position` int(11) NOT NULL,
  `description` text COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `factory`
--

INSERT INTO `factory` (`id`, `name`, `position`, `description`, `created_at`) VALUES
(1, 'B04', 0, 'LyG', '2022-03-15 15:27:07'),
(2, 'B05', 1, 'Netgear', '2022-03-15 15:27:26'),
(3, 'B06', 2, 'Ubee', '2022-03-17 10:09:19');

-- --------------------------------------------------------

--
-- Table structure for table `temperature`
--

CREATE TABLE `temperature` (
  `id` int(11) NOT NULL,
  `id_factory` int(11) NOT NULL,
  `name` text COLLATE utf8_unicode_ci NOT NULL,
  `win` int(11) NOT NULL,
  `temp_in` float NOT NULL,
  `temp_out` float NOT NULL,
  `humidity_in` float NOT NULL,
  `humidity_out` float NOT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `temperature`
--

INSERT INTO `temperature` (`id`, `id_factory`, `name`, `win`, `temp_in`, `temp_out`, `humidity_in`, `humidity_out`, `description`, `created_at`) VALUES
(1, 1, 'B04', 1, 22, 25, 80, 88, 'Sương mù, Mưa', '2022-03-15 16:05:54'),
(2, 1, 'B04', 2, 25, 29, 81, 88, 'Sương mù, ', '2022-03-15 16:22:19'),
(3, 3, 'B04', 2, 22, 22, 88, 80, '', '2022-03-17 16:46:32'),
(4, 1, '', 0, 22, 25, 81, 88, '', '2022-03-18 11:06:30'),
(5, 1, 'B04', 1, 22, 25, 81, 88, 'Mưa, ', '2022-03-18 11:07:56'),
(6, 1, 'B05', 0, 22, 25, 81, 88, 'Mưa, Nắng', '2022-03-18 11:11:36'),
(7, 1, 'B05', 1, 22, 24, 88, 89, 'Mưa, Nắng', '2022-03-18 11:12:33'),
(8, 1, 'B04', 1, 22, 25, 80, 88, 'Sương mù, Mưa', '2022-03-15 16:05:54'),
(9, 1, 'B04', 2, 25, 29, 81, 88, 'Sương mù, ', '2022-03-15 16:22:19'),
(10, 3, 'B04', 2, 22, 22, 88, 80, '', '2022-03-17 16:46:32'),
(11, 1, '', 0, 22, 25, 81, 88, '', '2022-03-18 11:06:30'),
(12, 1, 'B04', 1, 22, 25, 81, 88, 'Mưa, ', '2022-03-18 11:07:56'),
(13, 1, 'B05', 0, 22, 25, 81, 88, 'Mưa, Nắng', '2022-03-18 11:11:36'),
(14, 1, 'B05', 1, 22, 24, 88, 89, 'Mưa, Nắng', '2022-03-18 11:12:33'),
(15, 1, 'B04', 1, 22, 25, 80, 88, 'Sương mù, Mưa', '2022-03-15 16:05:54'),
(16, 1, 'B04', 2, 25, 29, 81, 88, 'Sương mù, ', '2022-03-15 16:22:19'),
(17, 3, 'B04', 2, 22, 22, 88, 80, '', '2022-03-17 16:46:32'),
(18, 1, '', 0, 22, 25, 81, 88, '', '2022-03-18 11:06:30'),
(19, 1, 'B04', 1, 22, 25, 81, 88, 'Mưa, ', '2022-03-18 11:07:56'),
(20, 1, 'B05', 0, 22, 25, 81, 88, 'Mưa, Nắng', '2022-03-18 11:11:36'),
(21, 1, 'B05', 1, 22, 24, 88, 89, 'Mưa, Nắng', '2022-03-18 11:12:33'),
(22, 1, 'B04', 1, 22, 25, 80, 88, 'Sương mù, Mưa', '2022-03-15 16:05:54'),
(23, 1, 'B04', 2, 25, 29, 81, 88, 'Sương mù, ', '2022-03-15 16:22:19'),
(24, 3, 'B04', 2, 22, 22, 88, 80, '', '2022-03-17 16:46:32'),
(25, 1, '', 0, 22, 25, 81, 88, '', '2022-03-18 11:06:30'),
(26, 1, 'B04', 1, 22, 25, 81, 88, 'Mưa, ', '2022-03-18 11:07:56'),
(27, 1, 'B05', 0, 22, 25, 81, 88, 'Mưa, Nắng', '2022-03-18 11:11:36'),
(28, 1, 'B05', 1, 22, 24, 88, 89, 'Mưa, Nắng', '2022-03-18 11:12:33');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `factory`
--
ALTER TABLE `factory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `temperature`
--
ALTER TABLE `temperature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_temp_factory` (`id_factory`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `factory`
--
ALTER TABLE `factory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `temperature`
--
ALTER TABLE `temperature`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
