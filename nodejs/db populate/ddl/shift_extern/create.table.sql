USE shift;

CREATE TABLE shift_extern
(
		id INT PRIMARY KEY AUTO_INCREMENT NOT NULL
,		id_intern INT NOT NULL
,		id_extern INT NOT NULL
,		weekday DATE NOT NULL
,		time_start TIME NOT NULL
,		time_end TIME NOT NULL
,		confirm SMALLINT DEFAULT 0 NOT NULL
,		active SMALLINT DEFAULT 1 NOT NULL
,		FOREIGN KEY (id_intern) REFERENCES intern(id)
,		FOREIGN KEY (id_extern) REFERENCES extern(id)
);

