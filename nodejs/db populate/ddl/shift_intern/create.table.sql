USE shift;

CREATE TABLE shift_intern
(
		id INT PRIMARY KEY AUTO_INCREMENT NOT NULL
,		weekday DATE NOT NULL
,		timeon TIME NOT NULL
,		timeoff TIME NOT NULL
,		id_speciality INT NOT NULL
,		id_intern INT NOT NULL
,		price INT NOT NULL 
,		time_interval INT NOT NULL
,		FOREIGN KEY (id_speciality) REFERENCES speciality(id)
,		FOREIGN KEY (id_intern) REFERENCES intern(id)
);
