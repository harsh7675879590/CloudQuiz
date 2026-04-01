import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

admin_pwd = generate_password_hash('Admin@123')
student_pwd = generate_password_hash('Student@123')

cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role) VALUES (1, 'System Admin', 'admin@quiz.com', ?, 'admin')", (admin_pwd,))
cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role) VALUES (2, 'John Doe', 'student@quiz.com', ?, 'student')", (student_pwd,))

cursor.execute("INSERT OR IGNORE INTO quizzes (id, title, description, time_limit, pass_score, is_active, created_by) VALUES (1, 'AWS Cloud Basics Challenge', 'Test your fundamental knowledge of AWS services like EC2, S3, and RDS.', 300, 60, 1, 1)")

cursor.execute("INSERT OR IGNORE INTO questions (id, quiz_id, text, points, order_num) VALUES (1, 1, 'Which AWS service is used for scalable computing capacity in the cloud?', 1, 1)")
cursor.execute("INSERT OR IGNORE INTO questions (id, quiz_id, text, points, order_num) VALUES (2, 1, 'Which storage service is best suited for hosting a static website frontend?', 1, 2)")
cursor.execute("INSERT OR IGNORE INTO questions (id, quiz_id, text, points, order_num) VALUES (3, 1, 'RDS is short for:', 1, 3)")

# Q1
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (1, 'Amazon S3', 0)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (1, 'Amazon EC2', 1)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (1, 'AWS Lambda', 0)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (1, 'Amazon RDS', 0)")

# Q2
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (2, 'Amazon S3', 1)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (2, 'Amazon EBS', 0)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (2, 'Amazon RDS', 0)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (2, 'Amazon DynamoDB', 0)")

# Q3
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (3, 'Relational Database Server', 0)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (3, 'Relational Database Service', 1)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (3, 'Remote Data Storage', 0)")
cursor.execute("INSERT OR IGNORE INTO options (question_id, text, is_correct) VALUES (3, 'Redundant Data System', 0)")

conn.commit()
conn.close()
print("Seed data inserted successfully.")
