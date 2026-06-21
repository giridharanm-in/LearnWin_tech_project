-- ============================================================
--  Besant Technologies – Database Setup
--  Run this file once in MySQL to create the database and tables
--  Command:  mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS besant_tech
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE besant_tech;

-- ── Courses ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS courses (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150)  NOT NULL,
    category    VARCHAR(100)  NOT NULL,
    duration    VARCHAR(60)   NOT NULL,
    description TEXT,
    mode        ENUM('Online','Offline','Both') DEFAULT 'Both',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Registrations ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS registrations (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(120)  NOT NULL,
    email         VARCHAR(150)  NOT NULL,
    phone         VARCHAR(20)   NOT NULL,
    course_id     INT           NOT NULL,
    gender        ENUM('Male','Female','Other') NOT NULL,
    qualification VARCHAR(100)  NOT NULL,
    message       TEXT,
    registered_on DATE          NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY uq_email_course (email, course_id)
);

-- ── Attendance ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(120)  NOT NULL,
    email      VARCHAR(150)  NOT NULL,
    course_id  INT           NOT NULL,
    att_date   DATE          NOT NULL,
    status     ENUM('Present','Absent','Late') DEFAULT 'Present',
    session    ENUM('Morning','Afternoon','Evening','Full Day') DEFAULT 'Morning',
    marked_at  DATETIME      NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY uq_att (email, course_id, att_date, session)
);

-- ── Contact Messages ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS contact_messages (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(120) NOT NULL,
    email      VARCHAR(150) NOT NULL,
    subject    VARCHAR(200) NOT NULL,
    message    TEXT         NOT NULL,
    sent_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Seed: Sample Courses ──────────────────────────────────────
INSERT INTO courses (course_name, category, duration, description, mode) VALUES
-- Programming
('Python Programming',        'Programming',       '45 Days', 'Learn Python from basics to advanced concepts including OOP, file handling, and projects.', 'Both'),
('Java Programming',          'Programming',       '60 Days', 'Core Java, OOP, Collections, Exception Handling, Multithreading and JDBC.', 'Both'),
('C & C++ Programming',       'Programming',       '45 Days', 'Structured and object-oriented programming with C and C++.', 'Both'),
('JavaScript Fundamentals',   'Programming',       '30 Days', 'DOM manipulation, ES6+, async/await, and modern JavaScript practices.', 'Both'),

-- Web Development
('Full Stack Web Development', 'Web Development',  '90 Days', 'HTML, CSS, JavaScript, React, Node.js, MySQL – build complete web apps.', 'Both'),
('React JS',                   'Web Development',  '45 Days', 'Build interactive UIs with React, Hooks, Redux, and REST APIs.', 'Both'),
('Django Web Framework',       'Web Development',  '45 Days', 'Python-based full-stack web development with Django and PostgreSQL.', 'Both'),
('PHP & MySQL',                'Web Development',  '45 Days', 'Server-side scripting with PHP and relational databases with MySQL.', 'Both'),

-- Data Science & AI
('Data Science with Python',   'Data Science & AI','90 Days', 'Pandas, NumPy, Matplotlib, Scikit-learn, and real-world data projects.', 'Both'),
('Machine Learning',           'Data Science & AI','60 Days', 'Supervised, unsupervised learning algorithms and model deployment.', 'Both'),
('Artificial Intelligence',    'Data Science & AI','75 Days', 'AI fundamentals, neural networks, and practical AI applications.', 'Both'),
('Deep Learning & NLP',        'Data Science & AI','60 Days', 'TensorFlow, Keras, CNNs, RNNs, and natural language processing.', 'Both'),

-- Database
('SQL & Database Design',      'Database',         '30 Days', 'Relational databases, SQL queries, normalization and query optimization.', 'Both'),
('MongoDB',                    'Database',         '30 Days', 'NoSQL database fundamentals, CRUD operations, aggregation, and indexing.', 'Both'),

-- Cloud & DevOps
('AWS Cloud Computing',        'Cloud & DevOps',   '45 Days', 'EC2, S3, RDS, Lambda and core AWS services for cloud architecture.', 'Both'),
('Docker & Kubernetes',        'Cloud & DevOps',   '30 Days', 'Containerization, orchestration, deployment pipelines with Docker & K8s.', 'Both'),

-- Testing
('Manual Testing',             'Software Testing', '30 Days', 'Test planning, test cases, bug tracking, and SDLC/STLC methodologies.', 'Both'),
('Selenium with Python',       'Software Testing', '45 Days', 'Automated web testing using Selenium WebDriver and Python frameworks.', 'Both'),

-- Design
('UI/UX Design',               'Design',           '45 Days', 'User research, wireframing, prototyping with Figma and design principles.', 'Both'),
('Graphic Design',             'Design',           '30 Days', 'Adobe Photoshop, Illustrator, and brand identity design.', 'Both');
