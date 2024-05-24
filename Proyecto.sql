CREATE SCHEMA proyecto
CREATE DATABASE IF NOT EXISTS `proyecto`
CREATE TABLE IF NOT EXISTS `proyecto`.`datos_serial`
(
	`Id` INT AUTO_INCREMENT PRIMARY KEY,
    `Mensaje_Serial` LONGTEXT,
    `Tiempo` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT * FROM `proyecto`.`datos_serial`
ALTER TABLE `proyecto`.`datos_serial` MODIFY Mensaje_Serial LONGTEXT;
TRUNCATE TABLE `proyecto`.`datos_serial`