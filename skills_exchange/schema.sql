-- Skills Exchange Database Schema
-- Run this file once to set up the database

CREATE DATABASE IF NOT EXISTS skills_exchange CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE skills_exchange;

CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    is_admin    TINYINT(1)   DEFAULT 0,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Insert a default admin user (password: admin123)
-- Change the password after first login!
INSERT IGNORE INTO users (username, email, password, is_admin)
VALUES (
    'admin',
    'admin@skillsexchange.com',
    '$2b$12$KIX8V1yXN6yqKpCpZVpNWOvJ3JkOjL5kRYkH5nXQN2kFbM1aWQIUu',
    1
);
