CREATE DATABASE online_banking_db;
USE online_banking_db;
SHOW TABLES;
INSERT INTO users (full_name, email, password_hash)
VALUES ('Test User', 'test@gmail.com', 'hashed_password');
INSERT INTO accounts (user_id, account_number, balance)
VALUES (1, 'ACC10001', 10000.00);
SELECT * FROM users;
SELECT * FROM accounts;
INSERT INTO accounts (user_id, account_number, balance)
VALUES (1, 'ACC10002', 5000.00);
CALL transfer_funds('ACC10001', 'ACC10002', 2000.00);
SELECT account_number, balance FROM accounts;
SELECT * FROM transactions;
CALL transfer_funds('ACC10001', 'ACC10002', 999999.00);
SELECT * FROM transactions;
DROP PROCEDURE IF EXISTS transfer_funds;
SELECT * FROM accounts;
SELECT * FROM transactions ORDER BY txn_time DESC;
SELECT user_id, email, password_hash FROM users;
SELECT balance FROM accounts WHERE user_id = 1;
SELECT * FROM transactions ORDER BY txn_time DESC;
ALTER TABLE accounts
ADD COLUMN full_name VARCHAR(100);
ALTER TABLE accounts
ADD COLUMN phone VARCHAR(15);
ALTER TABLE accounts
MODIFY user_id INT NULL;
INSERT INTO accounts 
(account_number, balance, status, created_at, full_name, phone)
VALUES
('ACC1001', 12000.00, 'ACTIVE', NOW(), 'Amit Sharma', '9876543210'),
('ACC1002', 5400.50, 'ACTIVE', NOW(), 'Priya Verma', '9876543211'),
('ACC1003', 25000.00, 'ACTIVE', NOW(), 'Rohit Patil', '9876543212'),
('ACC1004', 800.00, 'ACTIVE', NOW(), 'Sneha Kulkarni', '9876543213'),
('ACC1005', 15000.75, 'ACTIVE', NOW(), 'Rahul Mehta', '9876543214'),

('ACC1006', 6200.00, 'ACTIVE', NOW(), 'Neha Joshi', '9876543215'),
('ACC1007', 9800.25, 'ACTIVE', NOW(), 'Kunal Deshpande', '9876543216'),
('ACC1008', 300.00, 'BLOCKED', NOW(), 'Anjali Singh', '9876543217'),
('ACC1009', 47000.00, 'ACTIVE', NOW(), 'Vikas Rao', '9876543218'),
('ACC1010', 11200.00, 'ACTIVE', NOW(), 'Pooja Nair', '9876543219'),

('ACC1011', 5600.90, 'ACTIVE', NOW(), 'Suresh Iyer', '9876543220'),
('ACC1012', 7200.00, 'ACTIVE', NOW(), 'Nikita More', '9876543221'),
('ACC1013', 9100.45, 'ACTIVE', NOW(), 'Manish Gupta', '9876543222'),
('ACC1014', 30500.00, 'ACTIVE', NOW(), 'Aishwarya Patil', '9876543223'),
('ACC1015', 450.00, 'ACTIVE', NOW(), 'Rakesh Jain', '9876543224'),

('ACC1016', 8800.80, 'ACTIVE', NOW(), 'Shubham Kale', '9876543225'),
('ACC1017', 19999.99, 'ACTIVE', NOW(), 'Kavita Kulkarni', '9876543226'),
('ACC1018', 6000.00, 'BLOCKED', NOW(), 'Deepak Yadav', '9876543227'),
('ACC1019', 14300.00, 'ACTIVE', NOW(), 'Meenal Shah', '9876543228'),
('ACC1020', 27500.00, 'ACTIVE', NOW(), 'Akash Bhosale', '9876543229');

SELECT account_id, account_number, full_name, phone, user_id
FROM accounts;

UPDATE accounts
SET full_name = 'John Keneddy',phone ='4578855598'
WHERE account_id = 1;

UPDATE accounts
SET full_name = 'Suresh Rajput',phone ='6463676598'
WHERE account_id = 2;