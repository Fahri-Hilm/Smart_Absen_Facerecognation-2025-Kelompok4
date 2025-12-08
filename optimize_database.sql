-- Database Optimization Script for Smart Absen
-- Run this to add indexes for better query performance
-- Usage: mysql -u root -p absensi_karyawan_db < optimize_database.sql

USE absensi_karyawan_db;

-- Add indexes for frequently queried columns
ALTER TABLE attendance 
ADD INDEX IF NOT EXISTS idx_date (date),
ADD INDEX IF NOT EXISTS idx_employee_date (employee_id, date),
ADD INDEX IF NOT EXISTS idx_timestamp (timestamp);

ALTER TABLE employees 
ADD INDEX IF NOT EXISTS idx_name (name),
ADD INDEX IF NOT EXISTS idx_nik (nik);

ALTER TABLE activity_logs 
ADD INDEX IF NOT EXISTS idx_timestamp (timestamp),
ADD INDEX IF NOT EXISTS idx_user_id (user_id);

-- Optimize tables
OPTIMIZE TABLE attendance;
OPTIMIZE TABLE employees;
OPTIMIZE TABLE activity_logs;

-- Show index status
SHOW INDEX FROM attendance;
SHOW INDEX FROM employees;
SHOW INDEX FROM activity_logs;

SELECT 'Database optimization completed!' AS status;
