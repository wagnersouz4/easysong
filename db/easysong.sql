SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `easysong` ;
CREATE SCHEMA IF NOT EXISTS `easysong` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `easysong` ;

-- -----------------------------------------------------
-- Table `easysong`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `easysong`.`user` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `easysong`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(48) NULL ,
  `password` VARCHAR(128) NULL ,
  `money` DECIMAL UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `easysong`.`songs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `easysong`.`songs` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `easysong`.`songs` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `title` VARCHAR(64) NOT NULL ,
  `artist` VARCHAR(64) NOT NULL ,
  `album` VARCHAR(64) NOT NULL ,
  `genre` VARCHAR(64) NOT NULL ,
  `price` DECIMAL UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

SHOW WARNINGS;
USE `easysong` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
