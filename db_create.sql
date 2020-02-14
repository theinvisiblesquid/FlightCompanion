CREATE DATABASE flightcompanion;
USE flightcompanion;
CREATE TABLE `adsb` (
  `adsb_id` int(11) NOT NULL AUTO_INCREMENT,
  `hex` varchar(20) DEFAULT NULL,
  `squawk` int(11) DEFAULT NULL,
  `flight` varchar(20) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `nucp` int(11) DEFAULT NULL,
  `seen_pos` double DEFAULT NULL,
  `altitude` int(11) DEFAULT NULL,
  `vert_rate` int(11) DEFAULT NULL,
  `track` int(11) DEFAULT NULL,
  `speed` int(11) DEFAULT NULL,
  `messages` int(11) DEFAULT NULL,
  `seen` double DEFAULT NULL,
  `rssi` double DEFAULT NULL,
  PRIMARY KEY (`adsb_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
CREATE TABLE `aircraft` (
  `ac_id` varchar(20) NOT NULL,
  `ac_reg` varchar(50) DEFAULT NULL,
  `ac_make` varchar(100) DEFAULT NULL,
  `ac_model` varchar(100) DEFAULT NULL,
  `ac_photo` varchar(255) DEFAULT NULL,
  `ac_airline` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ac_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `arr` (
  `arr_id` varchar(10) NOT NULL,
  `arr_iata` varchar(10) DEFAULT NULL,
  `arr_name` varchar(255) DEFAULT NULL,
  `arr_tz` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`arr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `dep` (
  `dep_id` varchar(10) NOT NULL,
  `dep_iata` varchar(10) DEFAULT NULL,
  `dep_name` varchar(255) DEFAULT NULL,
  `dep_tz` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `flnum` (
  `fn_id` varchar(20) NOT NULL,
  `fn_iata` varchar(20) DEFAULT NULL,
  `fn_icao` varchar(20) DEFAULT NULL,
  `dep_time` varchar(100) DEFAULT NULL,
  `dep_date` varchar(100) DEFAULT NULL,
  `arr_time` varchar(100) DEFAULT NULL,
  `arr_date` varchar(100) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  PRIMARY KEY (`fn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `flights` (
  `flight_id` int(11) NOT NULL AUTO_INCREMENT,
  `fn_id` varchar(20) DEFAULT NULL,
  `ac_id` varchar(20) DEFAULT NULL,
  `dep_id` varchar(10) DEFAULT NULL,
  `arr_id` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`flight_id`),
  KEY `FK_FN` (`fn_id`),
  KEY `FK_AC` (`ac_id`),
  KEY `FK_DEP` (`dep_id`),
  KEY `FK_ARR` (`arr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE USER 'flightcompanion'@'localhost' IDENTIFIED BY 'fc1234';
GRANT ALL PRIVILEGES ON flightcompanion.* TO 'flightcompanion'@'localhost';
FLUSH PRIVILEGES;