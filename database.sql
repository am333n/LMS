/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - hr
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`hr` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `hr`;

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `loginid` int(100) DEFAULT NULL,
  `empid` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `dept` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `address` varchar(300) DEFAULT NULL,
  `photo` varchar(300) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `empstatus` varchar(100) DEFAULT NULL,
  `working` varchar(100) DEFAULT NULL,
  KEY `loginid` (`loginid`),
  KEY `empid` (`empid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

insert  into `employee`(`loginid`,`empid`,`name`,`dept`,`post`,`address`,`photo`,`dob`,`empstatus`,`working`) values 
(10,1,'emp4','computer','ex','abcd','/static/employee/20230508-194707.jpg','2023-05-10','accepted','working'),
(13,2,'emp1','Sales','salesman','abcdef','/static/employee/20230510-131927.jpg','2023-05-15','accepted','working');

/*Table structure for table `leave` */

DROP TABLE IF EXISTS `leave`;

CREATE TABLE `leave` (
  `loginid` int(100) DEFAULT NULL,
  `leaveid` int(100) NOT NULL AUTO_INCREMENT,
  `empid` int(100) DEFAULT NULL,
  `normal` int(100) DEFAULT NULL,
  `ntaken` int(100) DEFAULT NULL,
  `medical` int(100) DEFAULT NULL,
  `mtaken` int(100) DEFAULT NULL,
  `emergency` int(100) DEFAULT NULL,
  `etaken` int(100) DEFAULT NULL,
  PRIMARY KEY (`leaveid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `leave` */

insert  into `leave`(`loginid`,`leaveid`,`empid`,`normal`,`ntaken`,`medical`,`mtaken`,`emergency`,`etaken`) values 
(10,2,1,11,0,8,0,11,0),
(13,3,2,10,10,6,6,4,0);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `loginid` int(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  KEY `loginid` (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`loginid`,`username`,`password`,`type`) values 
(6,'hr','hr','hr'),
(7,'emp2','emp2','employee'),
(10,'emp4','emp4','employee'),
(11,'man1','MAN1','manager'),
(13,'emp1','emp1','employee');

/*Table structure for table `manager` */

DROP TABLE IF EXISTS `manager`;

CREATE TABLE `manager` (
  `manid` int(100) NOT NULL AUTO_INCREMENT,
  `loginid` int(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `address` varchar(300) DEFAULT NULL,
  `photo` varchar(300) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `manstatus` varchar(100) DEFAULT NULL,
  KEY `manid` (`manid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `manager` */

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `empid` int(100) DEFAULT NULL,
  `loginid` int(100) DEFAULT NULL,
  `leaveid` int(100) DEFAULT NULL,
  `requestid` int(100) NOT NULL AUTO_INCREMENT,
  `type` varchar(100) DEFAULT NULL,
  `leavestatus` varchar(100) DEFAULT NULL,
  `datefrom` date DEFAULT NULL,
  `dateto` date DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `days` int(100) DEFAULT NULL,
  KEY `requestid` (`requestid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `request` */

insert  into `request`(`empid`,`loginid`,`leaveid`,`requestid`,`type`,`leavestatus`,`datefrom`,`dateto`,`reason`,`days`) values 
(1,10,2,1,'emergency','accepted','2023-05-10','2023-05-15','operation',5),
(3,13,3,3,'emergency','rejected','2023-05-12','2023-05-13','marriage',1),
(3,13,3,4,'emergency','accepted','2023-05-15','2023-05-17','bla',-2);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
