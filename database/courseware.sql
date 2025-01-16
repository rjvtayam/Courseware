CREATE DATABASE IF NOT EXISTS courseware;
USE courseware;

-- Users table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    is_teacher BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE course (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    teacher_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (teacher_id) REFERENCES user(id)
);

-- Assignments table
CREATE TABLE assignment (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    course_id INTEGER NOT NULL,
    due_date DATETIME,
    materials_path VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES course(id)
);

-- Submissions table
CREATE TABLE submission (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignment_id) REFERENCES assignment(id),
    FOREIGN KEY (student_id) REFERENCES user(id)
);

-- Enrollment table (many-to-many relationship between students and courses)
CREATE TABLE enrollment (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES user(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
);

-- Notifications table
CREATE TABLE notification (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20),
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Feedback table
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    submission_id INTEGER NOT NULL,
    FOREIGN KEY (assignment_id) REFERENCES assignment(id),
    FOREIGN KEY (student_id) REFERENCES user(id),
    FOREIGN KEY (teacher_id) REFERENCES user(id),
    FOREIGN KEY (submission_id) REFERENCES submission(id)
);

-- Grades table
CREATE TABLE grade (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    score FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignment_id) REFERENCES assignment(id),
    FOREIGN KEY (student_id) REFERENCES user(id)
);

-- Add indexes for better query performance
CREATE INDEX idx_course_teacher ON course(teacher_id);
CREATE INDEX idx_assignment_course ON assignment(course_id);
CREATE INDEX idx_feedback_assignment ON feedback(assignment_id);
CREATE INDEX idx_feedback_student ON feedback(student_id);
CREATE INDEX idx_feedback_teacher ON feedback(teacher_id);
CREATE INDEX idx_feedback_submission ON feedback(submission_id);
CREATE INDEX idx_grade_assignment ON grade(assignment_id);
CREATE INDEX idx_grade_student ON grade(student_id);
CREATE INDEX idx_notification_user ON notification(user_id);
CREATE INDEX idx_submission_assignment ON submission(assignment_id);
CREATE INDEX idx_submission_student ON submission(student_id);
