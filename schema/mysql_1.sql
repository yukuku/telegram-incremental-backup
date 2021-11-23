/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table Message
# ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS `Message` (
  `id` bigint(11) unsigned NOT NULL,
  `message` mediumtext,
  `peer_user_id` bigint(20) DEFAULT NULL,
  `peer_chat_id` bigint(20) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `out` tinyint(1) DEFAULT NULL,
  `json_dump` longtext,
  `backup_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table MessageBackupStatus
# ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS `MessageBackupStatus` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `message_id_from` bigint(20) NOT NULL DEFAULT '0',
  `message_id_to` bigint(20) NOT NULL DEFAULT '0',
  `done_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_id_from` (`message_id_from`,`message_id_to`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
