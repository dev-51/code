CREATE TABLE line (
    id INT NOT NULL PRIMARY KEY,
    NAME VARCHAR(255) NOT NULL,
    weight INT NOT NULL,
    turn INT UNIQUE NOT NULL,
    CHECK (weight > 0)
);


INSERT INTO line VALUES (5, 'George Washington', 250, 1);
INSERT INTO line VALUES (4, 'Thomas Jefferson', 175, 5);
INSERT INTO line VALUES (3, 'John Adams', 350, 2);
INSERT INTO line VALUES (6, 'Thomas Jefferson', 400, 3);
INSERT INTO line VALUES (1, 'James Elephant', 500, 6);
INSERT INTO line VALUES (2, 'Will Johnliams', 200, 4);


SELECT NAME FROM line 
WHERE turn <= 
(
    SELECT b.quantity FROM (
        SELECT 2 AS quantity, SUM(weight) AS weight FROM line 
        WHERE turn < 3
        UNION ALL
        SELECT 3 AS quantity, SUM(weight) AS weight FROM line 
        WHERE turn < 4
        UNION ALL
        SELECT 4 AS quantity, SUM(weight) AS weight FROM line 
        WHERE turn < 5
    ) b 
    WHERE b.weight = 1000 LIMIT 1
)
ORDER BY turn DESC LIMIT 1;


