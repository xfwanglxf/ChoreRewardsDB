
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for reward_logs
-- ----------------------------
DROP TABLE IF EXISTS `reward_logs`;
CREATE TABLE `reward_logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `timestamp` datetime NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of reward_logs
-- ----------------------------

-- ----------------------------
-- Table structure for rewards
-- ----------------------------
DROP TABLE IF EXISTS `rewards`;
CREATE TABLE `rewards`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `points_needed` int NOT NULL,
  `type` enum('reward','consumption') CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of rewards
-- ----------------------------
INSERT INTO `rewards` VALUES (25, '玩IPad 15分钟', 5, 'consumption');
INSERT INTO `rewards` VALUES (26, '玩IPad 1小时', 10, 'consumption');
INSERT INTO `rewards` VALUES (27, '玩IPad 2小时', 20, 'consumption');
INSERT INTO `rewards` VALUES (28, '玩IPad 全天', 100, 'consumption');
INSERT INTO `rewards` VALUES (29, '看电视 30分钟', 3, 'consumption');
INSERT INTO `rewards` VALUES (30, '看电视 1小时', 5, 'consumption');
INSERT INTO `rewards` VALUES (31, '去游乐场玩', 5, 'consumption');

-- ----------------------------
-- Table structure for tasks
-- ----------------------------
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `points` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tasks
-- ----------------------------
INSERT INTO `tasks` VALUES (1, '洗澡', 1);
INSERT INTO `tasks` VALUES (2, '刷牙', 1);
INSERT INTO `tasks` VALUES (3, '买菜', 2);
INSERT INTO `tasks` VALUES (4, '拖地', 2);
INSERT INTO `tasks` VALUES (5, '不剩饭', 1);
INSERT INTO `tasks` VALUES (6, '取快递', 3);
INSERT INTO `tasks` VALUES (7, '写作业', 5);
INSERT INTO `tasks` VALUES (8, '早睡觉', 5);
INSERT INTO `tasks` VALUES (9, '打架子鼓', 2);
INSERT INTO `tasks` VALUES (10, '户外运动', 6);
INSERT INTO `tasks` VALUES (11, '晒衣服', 2);
INSERT INTO `tasks` VALUES (12, '叠衣服', 2);
INSERT INTO `tasks` VALUES (13, '受到表扬', 5);
INSERT INTO `tasks` VALUES (14, '奖励积分', 1);
INSERT INTO `tasks` VALUES (15, '晚睡', -2);
INSERT INTO `tasks` VALUES (16, '晚起', -2);
INSERT INTO `tasks` VALUES (17, '不听话', -2);
INSERT INTO `tasks` VALUES (18, '不按时刷牙洗脸', -2);

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `points_change` int NOT NULL,
  `timestamp` datetime NULL DEFAULT current_timestamp,
  `task_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of transactions
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `points` int NULL DEFAULT 0,
  `role` enum('admin','child') CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
