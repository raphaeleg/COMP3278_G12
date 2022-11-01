DROP DATABASE IF EXISTS `3278_GroupProject`;
CREATE DATABASE `3278_GroupProject` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `3278_GroupProject`;

CREATE TABLE `Student` (
  `student_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `student_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email_address` varchar(319) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `degree` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `enrollment_date` date NOT NULL,
  `year_of_study` int NOT NULL,
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
  PRIMARY KEY (`course_code`,`group_number`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecture` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `venue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`course_code`,`lecture_code`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
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
  `student_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `date_created` date NOT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`model_id`),
  FOREIGN KEY (`student_uid`) REFERENCES `Student` (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `LoginHistory` (
  `login_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `student_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `login_time` datetime NOT NULL,
  `logout_time` datetime,
  PRIMARY KEY (`login_id`,`student_uid`),
  FOREIGN KEY (`student_uid`) REFERENCES `Student` (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `LecturerTeachesLecture` (
  `instructor_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`instructor_id`,`course_code`,`lecture_code`),
  FOREIGN KEY (`instructor_id`) REFERENCES `Lecturer` (`instructor_id`),
  FOREIGN KEY (`course_code`, `lecture_code`) REFERENCES `Lecture` (`course_code`, `lecture_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `TutorTeachesTutorial` (
  `instructor_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  PRIMARY KEY (`instructor_id`,`course_code`,`group_number`),
  FOREIGN KEY (`instructor_id`) REFERENCES `Tutor` (`instructor_id`),
  FOREIGN KEY (`course_code`, `group_number`) REFERENCES `Tutorial` (`course_code`, `group_number`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `StudentTakesCourse` (
  `student_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  PRIMARY KEY (`student_uid`,`course_code`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  FOREIGN KEY (`student_uid`) REFERENCES `Student` (`student_uid`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Tutorial_timeslots` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `day_of_the_week` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  FOREIGN KEY (`course_code`, `group_number`) REFERENCES `Tutorial` (`course_code`, `group_number`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecture_timeslots` (
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `day_of_the_week` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  FOREIGN KEY (`course_code`, `lecture_code`) REFERENCES `Lecture` (`course_code`, `lecture_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lecture_zoom_links` (
  `zoom_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `zoom_links` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`zoom_id`),
  FOREIGN KEY (`course_code`, `lecture_code`) REFERENCES `Lecture` (`course_code`, `lecture_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Tutorial_zoom_links` (
  `zoom_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_number` int NOT NULL,
  `zoom_links` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`zoom_id`),
  FOREIGN KEY (`course_code`, `group_number`) REFERENCES `Tutorial` (`course_code`, `group_number`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Course_teacher_message` (
  `message_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_message` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`message_id`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Course_lecture_and_tutorial_notes` (
  `note_id` int NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lecture_and_tutorial_notes` longblob NOT NULL,
  PRIMARY KEY (`note_id`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
