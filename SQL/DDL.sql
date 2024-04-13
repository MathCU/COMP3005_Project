CREATE TABLE administration_staff (
	staff_id			SERIAL  	PRIMARY KEY,
	password			TEXT    	NOT NULL,
	first_name			TEXT		NOT NULL,
	last_name			TEXT		NOT NULL,
	phone_number		CHAR(10)	NOT NULL,
	email				TEXT		NOT NULL,
	street				TEXT		NOT NULL,
	home_number			INT			NOT NULL,
	postal_code			TEXT		NOT	NULL
);

CREATE TABLE trainer (
	trainer_id			SERIAL		PRIMARY KEY,
	password			TEXT		NOT NULL,
	first_name			TEXT		NOT NULL,
	last_name			TEXT		NOT NULL,
	phone_number		CHAR(10)	NOT NULL,
	email				TEXT		NOT NULL,
	street				TEXT		NOT NULL,
	home_number			INT			NOT NULL,
	postal_code			TEXT		NOT	NULL
);

CREATE TABLE member (
	member_id			SERIAL		PRIMARY KEY,
	password			TEXT		NOT NULL,
	first_name			TEXT		NOT NULL,
	last_name			TEXT		NOT NULL,
	phone_number		CHAR(10)	NOT NULL,
	email				TEXT		NOT NULL,
	street				TEXT		NOT NULL,
	home_number			INT			NOT NULL,
	postal_code			TEXT		NOT	NULL,
	height				INT,
	weight				INT
);

CREATE TABLE room (
	room_number 		CHAR(4)		PRIMARY KEY
);

CREATE TABLE equipment (
	bar_code			CHAR(10)	PRIMARY KEY,
	model				TEXT		NOT NULL		UNIQUE,
	last_maintenance	DATE,
	room_number			CHAR(4)		NOT NULL,
	FOREIGN KEY (room_number)		REFERENCES room (room_number)
);

CREATE TABLE class (
	class_id			SERIAL		PRIMARY KEY,
	name				TEXT		NOT NULL,
	date				DATE		NOT NULL,
	starting_time		TIME		NOT NULL,
	ending_time			TIME		NOT NULL,
	room_number			CHAR(4)		NOT NULL,
	trainer_id			INT			NOT NULL,
	staff_id			INT			NOT NULL,
	FOREIGN KEY (room_number)		REFERENCES room (room_number),
	FOREIGN KEY (trainer_id)		REFERENCES trainer (trainer_id),
	FOREIGN KEY (staff_id)			REFERENCES administration_staff (staff_id)
);

CREATE TABLE member_class (
	member_id			INT,
	class_id			INT,
	PRIMARY KEY (member_id, class_id),
	FOREIGN KEY (member_id)			REFERENCES member (member_id),
	FOREIGN KEY (class_id)			REFERENCES class (class_id)
);

CREATE TABLE availability (
	trainer_id			INT,
	date_time			TIMESTAMP	NOT NULL,
	PRIMARY KEY (trainer_id, date_time),
	FOREIGN KEY (trainer_id)		REFERENCES trainer (trainer_id)
);

CREATE TABLE private_session (
	trainer_id			INT,
	member_id			INT,
	date				DATE,
	starting_time		TIME		NOT NULL,
	ending_time			TIME		NOT NULL,
	PRIMARY KEY (trainer_id, member_id, date),
	FOREIGN KEY (trainer_id)		REFERENCES trainer (trainer_id),
	FOREIGN KEY (member_id)			REFERENCES member (member_id)
);

CREATE TABLE fitness_goal (
	goal_id				SERIAL		PRIMARY KEY,
	weight_goal			INT			NOT NULL,
	start_date			DATE,
	end_date			DATE,
	member_id			INT,
	FOREIGN KEY (member_id)			REFERENCES member (member_id)
);

CREATE TABLE exercise (
	exercise_name		TEXT		PRIMARY KEY,
	type				TEXT		NOT NULL
);

CREATE TABLE routine (
	routine_id			SERIAL		PRIMARY KEY,
	name				TEXT		NOT NULL,
	description			TEXT,
	member_id			INT,
	FOREIGN KEY (member_id)			REFERENCES member (member_id)
);

CREATE TABLE routine_exercise (
	routine_id			INT,
	exercise_name		TEXT,
	PRIMARY KEY (routine_id, exercise_name),
	FOREIGN KEY (routine_id)		REFERENCES routine (routine_id),
	FOREIGN KEY	(exercise_name)		REFERENCES exercise (exercise_name)
);

CREATE TABLE achievement (
	member_id			INT,
	achievement			TEXT,
	PRIMARY KEY (member_id, achievement),
	FOREIGN KEY (member_id)			REFERENCES member (member_id)
);

CREATE TABLE payment (
	transaction_id		SERIAL		PRIMARY KEY,
	date				DATE		NOT NULL,
	amount				MONEY		NOT NULL,
	method				TEXT		NOT NULL,
	member_id			INT,
	staff_id			INT,
	FOREIGN KEY (member_id)			REFERENCES member (member_id),
	FOREIGN KEY (staff_id)			REFERENCES administration_staff (staff_id)
);

CREATE TABLE invoice (
	invoice_number		SERIAL		PRIMARY KEY,
	invoice_date		DATE		NOT NULL,
	amount				MONEY		NOT NULL,
	due_date			DATE		NOT NULL,
	member_id			INT,
	staff_id			INT,
	FOREIGN KEY (member_id)			REFERENCES member (member_id),
	FOREIGN KEY (staff_id)			REFERENCES administration_staff (staff_id)
);