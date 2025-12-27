DELIMITER $$

CREATE PROCEDURE transfer_funds (
    IN sender_acc VARCHAR(20),
    IN receiver_acc VARCHAR(20),
    IN transfer_amount DECIMAL(12,2)
)
BEGIN
    DECLARE sender_balance DECIMAL(12,2);

    START TRANSACTION;

    SELECT balance INTO sender_balance
    FROM accounts
    WHERE account_number = sender_acc
    FOR UPDATE;

    IF sender_balance < transfer_amount THEN
        ROLLBACK;
        SELECT 'INSUFFICIENT_BALANCE' AS result;
    ELSE
        UPDATE accounts
        SET balance = balance - transfer_amount
        WHERE account_number = sender_acc;

        UPDATE accounts
        SET balance = balance + transfer_amount
        WHERE account_number = receiver_acc;

        INSERT INTO transactions
        (from_account, to_account, amount, txn_type)
        VALUES
        (sender_acc, receiver_acc, transfer_amount, 'TRANSFER');

        COMMIT;
        SELECT 'SUCCESS' AS result;
    END IF;
END$$

DELIMITER ;
