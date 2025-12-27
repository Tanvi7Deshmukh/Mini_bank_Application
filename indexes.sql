CREATE INDEX idx_account_number ON accounts(account_number);
CREATE INDEX idx_from_account ON transactions(from_account);
CREATE INDEX idx_to_account ON transactions(to_account);
CREATE INDEX idx_user_email ON users(email);
SHOW INDEX FROM accounts;
SHOW INDEX FROM transactions;
