DROP DATABASE IF EXISTS `3278_GroupProject`;
CREATE DATABASE `3278_GroupProject` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `3278_GroupProject`;

CREATE TABLE `Student` (
  `student_uid` int NOT NULL,
  `student_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email_address` varchar(319) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `degree` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `enrollment_date` date NOT NULL,
  `year_of_study` int NOT NULL,
  `student_photo` longblob,
  PRIMARY KEY (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Course` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `course_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Tutorial` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  `venue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_day` date NOT NULL,
  `last_day` date NOT NULL,
  PRIMARY KEY (`course_code`,`group_number`),
  CONSTRAINT `Tutorial.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecture` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `venue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_day` date NOT NULL,
  `last_day` date NOT NULL,
  PRIMARY KEY (`course_code`,`lecture_code`),
  CONSTRAINT `Lecture.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Tutor` (
  `instructor_id` int NOT NULL,
  `instructor_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `instructor_email` varchar(319) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`instructor_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecturer` (
  `instructor_id` int NOT NULL,
  `instructor_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `instructor_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`instructor_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `RecognitionModel` (
  `model_id` int NOT NULL,
  `student_uid` int NOT NULL,
  `date_created` date NOT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`model_id`),
  KEY `RecognitionModel.student_uid_idx` (`student_uid`),
  CONSTRAINT `RecognitionModel.student_uid` FOREIGN KEY (`student_uid`) REFERENCES `Student` (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `LoginHistory` (
  `login_id` int NOT NULL,
  `student_uid` int NOT NULL,
  `login_time` datetime NOT NULL,
  `logout_time` datetime NOT NULL,
  PRIMARY KEY (`login_id`,`student_uid`),
  KEY `LoginHistory.student_uid_idx` (`student_uid`),
  CONSTRAINT `LoginHistory.student_uid` FOREIGN KEY (`student_uid`) REFERENCES `Student` (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Holidays` (
  `holiday_id` int NOT NULL,
  `holiday_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `holiday_date_start` date NOT NULL,
  `holiday_date_end` date NOT NULL,
  PRIMARY KEY (`holiday_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `LecturerTeachesLecture` (
  `instructor_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`instructor_id`,`course_code`,`lecture_code`),
  KEY `LTL.course_code_idx` (`course_code`),
  KEY `LTL.lecture_code_idx` (`lecture_code`),
  CONSTRAINT `LTL.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  CONSTRAINT `LTL.instructor_id` FOREIGN KEY (`instructor_id`) REFERENCES `Lecturer` (`instructor_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `TutorTeachesTutorial` (
  `instructor_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  PRIMARY KEY (`instructor_id`,`course_code`,`group_number`),
  KEY `TTT.course_code_idx` (`course_code`),
  KEY `TTT.group_number_idx` (`group_number`),
  CONSTRAINT `TTT.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  CONSTRAINT `TTT.instructor_id` FOREIGN KEY (`instructor_id`) REFERENCES `Tutor` (`instructor_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `StudentTakesCourse` (
  `student_uid` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`student_uid`,`course_code`),
  KEY `STC.course_code_idx` (`course_code`),
  CONSTRAINT `STC.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  CONSTRAINT `STC.student_uid` FOREIGN KEY (`student_uid`) REFERENCES `Student` (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `LectureCancelIfHolidays` (
  `holiday_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`holiday_id`,`course_code`,`lecture_code`),
  KEY `LCIH.course_code_idx` (`course_code`),
  KEY `LCIH.lecture_code_idx` (`lecture_code`),
  CONSTRAINT `LCIH.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  CONSTRAINT `LCIH.holiday_id` FOREIGN KEY (`holiday_id`) REFERENCES `Holidays` (`holiday_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `TutorialCancelIfHalidays` (
  `holiday_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  PRIMARY KEY (`holiday_id`,`course_code`,`group_number`),
  KEY `TCIH.course_code_idx` (`course_code`),
  KEY `TCIH.group_number_idx` (`group_number`),
  CONSTRAINT `TCIH.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  CONSTRAINT `TCIH.holiday_id` FOREIGN KEY (`holiday_id`) REFERENCES `Holidays` (`holiday_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Tutorial_timeslots` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `day_of_the_week` int NOT NULL,
  KEY `TT.group_number_idx` (`group_number`),
  KEY `TT.course_code_idx` (`course_code`),
  CONSTRAINT `TT.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecture_timeslots` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `day_of_the_week` int NOT NULL,
  KEY `LT.course_code_idx` (`course_code`),
  CONSTRAINT `LT.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecture_zoom_links` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `zoom_links` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  KEY `LZL.lecture_code_idx` (`lecture_code`),
  KEY `LZL.course_code_idx` (`course_code`),
  CONSTRAINT `LZL.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Tutorial_zoom_links` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  `zoom_links` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`course_code`,`group_number`,`zoom_links`),
  KEY `TZL.group_number_idx` (`group_number`),
  CONSTRAINT `TZL.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Course_teacher_message` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_message` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`course_code`,`teacher_message`),
  CONSTRAINT `CTM.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Course_lecture_and_tutorial_notes` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_and_tutorial_notes` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`course_code`,`lecture_and_tutorial_notes`),
  CONSTRAINT `CLATN.course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

