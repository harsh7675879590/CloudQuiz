-- Demo Data for the Online Quiz System
USE quizdb;

-- Passwords are hashed versions of "Admin@123" and "Student@123" respectively
INSERT INTO users (name, email, password, role) VALUES 
('System Admin', 'admin@quiz.com', 'scrypt:32768:8:1$Cq7l1fOovI5d1KZr$0799f2fd8b8f2d72106e2cf2d3077afaff9f9c0c1b4ac4b025d5d67ba5b9aee', 'admin'),
('John Doe', 'student@quiz.com', 'scrypt:32768:8:1$KJrYwE0o2n1zR3sZ$4275f3a09c0d1e37bc9e1a12e3408bfbfccb9000a8aef40c34f3c75ab3f27f0', 'student');

-- Insert a sample AWS Quiz
INSERT INTO quizzes (title, description, time_limit, pass_score, is_active, created_by) VALUES
('AWS Cloud Basics Challenge', 'Test your fundamental knowledge of AWS services like EC2, S3, and RDS.', 300, 60, 1, 1);

-- Insert Questions for Quiz 1
INSERT INTO questions (quiz_id, text, points, order_num) VALUES
(1, 'Which AWS service is used for scalable computing capacity in the cloud?', 1, 1),
(1, 'Which storage service is best suited for hosting a static website frontend?', 1, 2),
(1, 'RDS is short for:', 1, 3);

-- Options for Q1 (EC2)
INSERT INTO options (question_id, text, is_correct) VALUES
(1, 'Amazon S3', 0),
(1, 'Amazon EC2', 1),
(1, 'AWS Lambda', 0),
(1, 'Amazon RDS', 0);

-- Options for Q2 (S3)
INSERT INTO options (question_id, text, is_correct) VALUES
(2, 'Amazon S3', 1),
(2, 'Amazon EBS', 0),
(2, 'Amazon RDS', 0),
(2, 'Amazon DynamoDB', 0);

-- Options for Q3 (RDS)
INSERT INTO options (question_id, text, is_correct) VALUES
(3, 'Relational Database Server', 0),
(3, 'Relational Database Service', 1),
(3, 'Remote Data Storage', 0),
(3, 'Redundant Data System', 0);
