/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost
 Source Database       : work

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : utf-8

 Date: 07/15/2018 13:11:46 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `zhixiao`
-- ----------------------------
DROP TABLE IF EXISTS `zhixiao`;
CREATE TABLE `zhixiao` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `icon_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `app_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `app_author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `app_pv_num` int(11) DEFAULT NULL COMMENT '浏览量',
  `app_collect_num` int(11) DEFAULT NULL COMMENT '收藏量',
  `app_tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '分类 逗号分隔',
  `publish_time` timestamp NULL DEFAULT NULL COMMENT '发布时间',
  `app_qr_code_addr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '小程序码地址',
  `screenshots` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '截图 逗号分隔',
  `app_intro` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '简介',
  `star_value` float DEFAULT NULL COMMENT '评分',
  `star_num` int(11) DEFAULT NULL COMMENT '评分数量',
  `source_id` int(11) DEFAULT NULL COMMENT '来源ID',
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_source_id` (`source_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6666 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
