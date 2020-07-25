CREATE TABLE line (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    weight INT NOT NULL,
    turn INT UNIQUE NOT NULL,
    CHECK (weight > 0)
);


INSERT INTO line VALUES (5, 'George Washington', 250, 1);
INSERT INTO line VALUES (4, 'Thomas Lucas', 101, 5);
INSERT INTO line VALUES (3, 'John Adams', 350, 2);
INSERT INTO line VALUES (6, 'Thomas Jefferson', 200, 3);
INSERT INTO line VALUES (1, 'James Elephant', 500, 6);
INSERT INTO line VALUES (2, 'Will Johnliams', 100, 4);


SELECT name FROM line 
WHERE turn = 
(   
    SELECT A.amount
    FROM
    (
        SELECT 2 AS amount, SUM(weight) AS weight FROM line 
        WHERE turn < 3
        UNION ALL
        SELECT 3 AS amount, SUM(weight) AS weight FROM line 
        WHERE turn < 4
        UNION ALL
        SELECT 4 AS amount, SUM(weight) AS weight FROM line 
        WHERE turn < 5
        UNION ALL       
        SELECT 5 AS amount, SUM(weight) AS weight FROM line 
        WHERE turn < 6
        UNION ALL
        SELECT 6 AS amount, SUM(weight) AS weight FROM line 
        WHERE turn = 6      
    ) A
    WHERE A.weight = 
    (
        SELECT MAX(B.weight)
        FROM
        (
            SELECT 2 AS amount, SUM(weight) AS weight FROM line 
            WHERE turn < 3
            UNION ALL
            SELECT 3 AS amount, SUM(weight) AS weight FROM line 
            WHERE turn < 4
            UNION ALL
            SELECT 4 AS amount, SUM(weight) AS weight FROM line 
            WHERE turn < 5
            UNION ALL       
            SELECT 5 AS amount, SUM(weight) AS weight FROM line 
            WHERE turn < 6
            UNION ALL
            SELECT 6 AS amount, SUM(weight) AS weight FROM line 
            WHERE turn = 6          
        ) B 
        WHERE B.weight <= 1000
    )
)


