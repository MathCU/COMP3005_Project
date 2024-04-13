INSERT INTO administration_staff (password, first_name, last_name, phone_number, email, street, home_number, postal_code)
VALUES
('Xmanager789', 'Tim', 'Obrien', '6136136613', 'tim.obrien@GymXYZ.com', 'Rideau', 1, 'A1B2C4'),
('Gstaff456', 'Markus ', 'Dotson', '6134569873', 'markus.dotson@GymXYZ.com', 'Wellington', 5, 'A1B9Z8'),
('Gstaff123', 'Nadine', 'Miles', '6131234567', 'nadine.miles@GymXYZ.com', 'Bronson', 3, 'C5H4T7');

INSERT INTO trainer (password, first_name, last_name, phone_number, email, street, home_number, postal_code)
VALUES
('TTrainn654', 'Penelope', 'Bright', '6139998888', 'Penelope.Bright@gmail.com', 'Sommerset', 10, 'G8R6U7'),
('Dudez332', 'Jaime', 'Shelton', '6136634859', 'Jaime.Shelton@gmail.com', 'Albert', 50, 'Y6T5R3'),
('ABC555', 'Solomon', 'Russell', '6134548989', 'Solomon.Russell@gmail.com', 'Slater', 30, 'Q9W8E7');

INSERT INTO member (password, first_name, last_name, phone_number, email, street, home_number, postal_code, height, weight)
VALUES
('Gym777', 'Frank', 'Mercado', '6131112222', 'Frank.Mercado@gmail.com', 'Bank', 1000, 'B6V4M3', 180, 90),
('New987', 'Denise', 'Saunders', '6132359674', 'Denise.Saunders@gmail.com', 'Kent', 500, 'B6V1A1', 150, 50),
('ZZZ555', 'Christopher', 'Bowman', '6135558888', 'Christopher.Bowman@gmail.com', 'Lyon', 300, 'B6V9H8', 175, 80);

INSERT INTO room (room_number)
VALUES
('A100'),
('A101'),
('A102'),
('B100'),
('B101'),
('B102');

INSERT INTO equipment (bar_code, model, last_maintenance, room_number)
VALUES
('0000000001', 'Dumbbell 5kg', '2024-04-25', 'A100'),
('0000000002', 'Squat Rack XPro', '2024-04-30', 'B100'),
('0000000025', 'Yoga Mat Blue', '2024-03-31', 'A101'),
('0000002354', 'Elastic Band - Medium', '2024-03-31', 'A101'),
('0000000264', 'Treadmill Super', '2024-04-30', 'A100');

INSERT INTO class (name, date, starting_time, ending_time, room_number, trainer_id, staff_id)
VALUES
('Yoga 101', '2024-05-01', '8:00', '9:00', 'A101', 1, 2),
('Super Core', '2024-05-02', '13:00', '14:00', 'B101', 3, 3),
('Activia', '2024-05-02', '13:00', '14:00', 'A102', 2, 3);

INSERT INTO member_class (member_id, class_id)
VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO availability (trainer_id, date_time)
VALUES
(1, '2024-05-03 11:00:00'),
(1, '2024-05-03 11:30:00'),
(2, '2024-05-04 10:00:00');

INSERT INTO private_session (trainer_id, member_id, date, starting_time, ending_time)
VALUES
(3, 1, '2024-05-10', '10:00', '11:00'),
(2, 2, '2024-05-11', '9:00', '10:00'),
(1, 3, '2024-05-12', '15:00', '16:00');

INSERT INTO fitness_goal (weight_goal, start_date, end_date, member_id)
VALUES
(170, '2024-05-01', '2024-05-31', 1),
(140, '2024-05-01', '2024-05-31', 2),
(165, '2024-05-01', '2024-05-31', 3);

INSERT INTO exercise (exercise_name, type)
VALUES
('Squat', 'Leg Focus'),
('Barbell Curl', 'Arm Focus'),
('Plank', 'Core'),
('Deadlift', 'Leg Focus'),
('Lunges', 'Leg Focus'),
('Abs Crusher', 'Core');

INSERT INTO routine (name, description, member_id)
VALUES
('Leg Day', 'Leg Routine', 1),
('Core Day', 'Core Routine', 2);

INSERT INTO routine_exercise (routine_id, exercise_name)
VALUES
(1, 'Squat'),
(1, 'Deadlift'),
(1, 'Lunges'),
(2, 'Plank'),
(2, 'Abs Crusher');

INSERT INTO achievement (member_id, achievement)
VALUES
(3, 'Started to go at the Gym!');

INSERT INTO payment (date, amount, method, member_id, staff_id)
VALUES
('2024-03-01', 50, 'Cash', 1, 1),
('2024-03-01', 50, 'Credit Card', 2, 1),
('2024-03-01', 50, 'Cash', 3, 1),
('2024-03-15', 100, 'Credit Card', 2, 2);

INSERT INTO invoice (invoice_date, amount, due_date, member_id, staff_id)
VALUES
('2024-03-01', 50, '2024-03-31', 1, 1),
('2024-03-01', 50, '2024-03-31', 2, 1),
('2024-03-01', 50, '2024-03-31', 3, 1),
('2024-03-29', 120, '2024-04-28', 1, 2),
('2024-03-15', 100, '2024-03-31', 2, 2),
('2024-03-31', 75, '2024-04-30', 3, 3);