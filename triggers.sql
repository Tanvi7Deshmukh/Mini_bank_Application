DELIMITER $$

CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    INSERT INTO transaction_audit
    (from_account, to_account, amount, status)
    VALUES
    (NEW.from_account, NEW.to_account, NEW.amount, 'AUTO-LOGGED');
END$$

DELIMITER ;
SHOW TRIGGERS;
