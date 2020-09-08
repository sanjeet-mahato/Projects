-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 08, 2020 at 02:29 PM
-- Server version: 10.1.32-MariaDB
-- PHP Version: 5.6.36

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hosp`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `Appo_Id` varchar(15) NOT NULL,
  `Pat_Id` varchar(15) NOT NULL,
  `Doc_Id` varchar(15) NOT NULL,
  `Date` varchar(12) NOT NULL,
  `Time` varchar(8) NOT NULL,
  `Complain` text NOT NULL,
  `Status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`Appo_Id`, `Pat_Id`, `Doc_Id`, `Date`, `Time`, `Complain`, `Status`) VALUES
('AP102818025709', 'PT102718032427', 'DR102818061019', '29/10/2018', '13:25', 'Stomach Pain', 'Accepted');

-- --------------------------------------------------------

--
-- Table structure for table `bed`
--

CREATE TABLE `bed` (
  `Bed_Id` varchar(15) NOT NULL,
  `Nurse_Id` varchar(15) NOT NULL,
  `Pat_Id` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bed`
--

INSERT INTO `bed` (`Bed_Id`, `Nurse_Id`, `Pat_Id`) VALUES
('BD102818052715', 'NR102718030039', 'PT102718032427');

-- --------------------------------------------------------

--
-- Table structure for table `invoice`
--

CREATE TABLE `invoice` (
  `Date` varchar(12) NOT NULL,
  `Invoice_Id` varchar(15) NOT NULL,
  `Pat_Id` varchar(15) NOT NULL,
  `User` varchar(15) NOT NULL,
  `User_Id` varchar(15) NOT NULL,
  `Details` text NOT NULL,
  `Amount` varchar(7) NOT NULL,
  `Status` varchar(10) NOT NULL,
  `Acc_Id` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `invoice`
--

INSERT INTO `invoice` (`Date`, `Invoice_Id`, `Pat_Id`, `User`, `User_Id`, `Details`, `Amount`, `Status`, `Acc_Id`) VALUES
('10/10/2018', 'IN102818105204', 'PT102718032427', 'akshay', 'LB102718064359', 'Blood Report', '970', 'Paid', 'AC102718065422'),
('12/10/2018', 'IN102818110605', 'PT102718032427', 'akshay', 'LB102718064359', 'Sugar Test', '1000', 'Paid', 'AC102718065422'),
('23/10/2018', 'IN102818111616', 'PT102718032427', 'Ravindra', 'PH102718062627', 'Paracetamol', '100', 'Paid', 'AC102718065422'),
('25/10/2018', 'IN102818111711', 'PT102718032427', 'Ravindra', 'PH102718062627', 'Calpol', '75', 'Pending', 'none');

-- --------------------------------------------------------

--
-- Table structure for table `medicine`
--

CREATE TABLE `medicine` (
  `Med_Id` varchar(15) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Details` varchar(20) NOT NULL,
  `Price` varchar(6) NOT NULL,
  `Quantity` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `medicine`
--

INSERT INTO `medicine` (`Med_Id`, `Name`, `Details`, `Price`, `Quantity`) VALUES
('MD102818074103', 'Paracetamol', '650mg', '100', '2000'),
('MD102818074223', 'Canditral', '200mg', '225', '3000');

-- --------------------------------------------------------

--
-- Table structure for table `monitor`
--

CREATE TABLE `monitor` (
  `Mon_Id` varchar(15) NOT NULL,
  `Pat_Id` varchar(15) NOT NULL,
  `Nurse_Id` varchar(15) NOT NULL,
  `Doc_Id` varchar(15) NOT NULL,
  `Date` varchar(12) NOT NULL,
  `BP` varchar(25) NOT NULL,
  `Temp` varchar(6) NOT NULL,
  `Other` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `monitor`
--

INSERT INTO `monitor` (`Mon_Id`, `Pat_Id`, `Nurse_Id`, `Doc_Id`, `Date`, `BP`, `Temp`, `Other`) VALUES
('MT102818061045', 'PT102718032427', 'NR102718030039', 'DR102818061019', '01/11/2018', '120/80', '98.6', 'NA');

-- --------------------------------------------------------

--
-- Table structure for table `prescription`
--

CREATE TABLE `prescription` (
  `Pres_Id` varchar(15) NOT NULL,
  `Pat_Id` varchar(15) NOT NULL,
  `Doc_Id` varchar(15) NOT NULL,
  `Nurse_Id` varchar(15) NOT NULL,
  `Medicine` text NOT NULL,
  `Advice` text NOT NULL,
  `Date` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `prescription`
--

INSERT INTO `prescription` (`Pres_Id`, `Pat_Id`, `Doc_Id`, `Nurse_Id`, `Medicine`, `Advice`, `Date`) VALUES
('PR102818094844', 'PT102718032427', 'DR102818061019', 'NR102718030039', 'Paracetamol,Calpol', 'Regular Exercise', '23/10/2018');

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `User_Id` varchar(15) NOT NULL,
  `Password` varchar(15) NOT NULL,
  `User_Type` varchar(15) NOT NULL,
  `Department` varchar(15) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Sex` varchar(8) NOT NULL,
  `Age` varchar(3) NOT NULL,
  `Blood_Group` varchar(6) NOT NULL,
  `Email_Id` varchar(20) NOT NULL,
  `Telephone_No` varchar(12) NOT NULL,
  `Address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`User_Id`, `Password`, `User_Type`, `Department`, `Name`, `Sex`, `Age`, `Blood_Group`, `Email_Id`, `Telephone_No`, `Address`) VALUES
('AD12345', 'admin', 'Admin', '', 'Admin', 'Male', '30', 'A+', 'admin76@gmailcom', '9007471357', '18/B, Jagadipota, Kolkata-107'),
('NR102718030039', 'password', 'Nurse', 'Gasentrology', 'Sonia', 'Female', '24', 'O+', 'sonia876@gmail.com', '9674581523', '287, Anandapur, Kolkata-107'),
('PT102718032427', 'password', 'Patient', 'Sammadar', 'Ajay', 'Male', '30', 'A+', 'ajay78@gmail.com', '8759654256', '13/C, Mukudapur, Kolkata-099'),
('PH102718062627', 'password', 'Pharmacist', 'none', 'Ravindra', 'Male', '32', 'AB+', 'ravindra04@gmail.com', '9748685826', '14/B, Ajaynagar, Kolkata-099'),
('LB102718064359', 'password', 'Laboratorist', 'none', 'akshay', 'Male', '42', 'O+', 'akshay56@gmail.com', '9858691425', '17/B, Madurdaha, Kolkata-099'),
('AC102718065422', 'password', 'Accountant', 'none', 'Harishchandra', 'Male', '44', 'O+', 'harish456@gmail.com', '9845263625', '14/B, Gariahat, Kolkata-109'),
('DR102818061019', 'password', 'Doctor', 'General', 'Sammadar', 'Male', '49', 'B+', 'sammadar87@gmail.com', '9785684586', '13/B, Kalikapur,Kolkata-107'),
('PT102818065105', 'password', 'Patient', 'doctor', 'name', 'x', '0', 'x', 'email', 'tel', 'add'),
('NR102818065119', 'password', 'Nurse', 'dep', 'name', 'x', '0', 'x', 'email', 'tel', 'add'),
('PH102818065127', 'password', 'Pharmacist', 'none', 'name', 'x', '0', 'x', 'email', 'tel', 'add'),
('LB102818065131', 'password', 'Laboratorist', 'none', 'name', 'x', '0', 'x', 'email', 'tel', 'add'),
('AC102818065141', 'password', 'Accountant', 'none', 'Ravi', 'Male', '34', 'B+', 'ravi01@gmail.com', '8769583526', '13/C,Mukundapur, Kolkata-099'),
('PT032120074223', 'password', 'Patient', 'doctor', 'name', 'x', '0', 'x', 'email', 'tel', 'add'),
('PT032120074519', 'password', 'Patient', 'doctor', 'name', 'x', '0', 'x', 'email', 'tel', 'add');

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `Report_Id` varchar(15) NOT NULL,
  `Pat_Id` varchar(15) NOT NULL,
  `Doc_Id` varchar(15) NOT NULL,
  `Lab_Id` varchar(15) NOT NULL,
  `Caption` varchar(20) NOT NULL,
  `Details` text NOT NULL,
  `Date` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`Report_Id`, `Pat_Id`, `Doc_Id`, `Lab_Id`, `Caption`, `Details`, `Date`) VALUES
('RE102818083733', 'PT102718032427', 'DR102818061019', 'LB102718064359', 'Blood Report', 'Normal', '10/10/2018');

-- --------------------------------------------------------

--
-- Table structure for table `salary`
--

CREATE TABLE `salary` (
  `Salary_Id` varchar(15) NOT NULL,
  `User_Id` varchar(15) NOT NULL,
  `Acc_Id` varchar(15) NOT NULL,
  `Date` varchar(12) NOT NULL,
  `Amount` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `salary`
--

INSERT INTO `salary` (`Salary_Id`, `User_Id`, `Acc_Id`, `Date`, `Amount`) VALUES
('SA102818093058', 'DR102818061019', 'AC102718065422', '12/10/2018', '10000'),
('SA102818094738', 'LB102718064359', 'AC102718065422', '13/10/2018', '20000'),
('SA102818094851', 'NR102718030039', 'AC102818065141', '15/10/2018', '30000'),
('SA102818095624', 'PH102718062627', 'AC102818065141', '25/10/2018', '8000'),
('SA102818100224', 'AC102718065422', 'AC102818065141', '30/10/2018', '15000'),
('SA103118065259', 'AC102818065141', 'AC102718065422', 'dd/mm/yyyy', '9500');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
