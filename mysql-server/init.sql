-- Smart Absen Database Initialization
CREATE DATABASE IF NOT EXISTS smart_absen;
USE smart_absen;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    face_encoding TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('masuk', 'keluar') DEFAULT 'masuk',
    confidence FLOAT DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create admin user (optional)
INSERT IGNORE INTO users (name, email) VALUES 
('Admin', 'admin@smartabsen.com'),
('Fahri Juru', 'fahri@smartabsen.com');

-- Grant permissions
GRANT ALL PRIVILEGES ON smart_absen.* TO 'absen_user'@'%';
FLUSH PRIVILEGES;
