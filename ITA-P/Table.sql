------------------------------------------
-- E.T.A --------
-----------------------------------------

Create table User_data (
    User_id INTEGER PRIMARY KEY ,
    Telegram_user_id NULL,
    FIO VARCHAR(255) NOT NULL ,
    Date_brith Date not null,
    Gender VARCHAR(10) NOT NULL CHECK(Gender IN ('М', 'Ж')),
    Year_grad_fr_school INT NOT NULL CHECK(Year_grad_fr_school > 1900)
);

Create table User_rights(
    User_id INT NOT NULL ,
    User_type VARCHAR(10) NOT NULL CHECK(User_type IN ('Admin', 'admin', 'A', 'a', 'User', 'user', 'U', 'u', 'Test', 'test', 'T', 't')) ,
    -- 
    constraint pk_user_id_rights foreign key (User_id) 
    references User_data(User_id)
);

Create table Users_contacts(
    User_id INT NOT NULL ,
    Email VARCHAR(255) NULL ,
    Phone VARCHAR(20) NULL ,

    constraint pk_user_id_contacts foreign key (User_id)
    references User_data(User_id)
)

CREATE TABLE Faculty(
    Faculty_id INTEGER PRIMARY KEY,
    Faculty_name VARCHAR(255) NOT NULL
);

CREATE TABLE User_faculty(
    User_id INT NOT NULL ,
    Faculty_id INT NOT NULL,

    constraint pk_user_id_faculty foreign key (User_id) 
    references User_data(User_id),
    --

    constraint pk_faculty foreign key (Faculty_id) 
    references Faculty(Faculty_id)
);

--Добавляем факультеты
INSERT INTO Faculty(Faculty_name) VALUES 
('Факультет информационных технологий и управления'),
('Факультет филологии'),
('Факультет биологии'),
('Факультет права и социальных технологий'),
('Факультет естественных наук и технологий'),
('Экономический факультет');

-- добавляем тестового пользователя (Алгоритм добавления нового пользователя)
INSERT INTO User_data(User_id, FIO, Date_brith, Gender, Year_grad_fr_school) VALUES (1, 'Иван Иванов Иванович', 01.01.1999, 'М', 2019);
Insert INTO User_rights(User_id, User_type) VALUES (1, 'Test');
Insert into Users_contacts(User_id, Email, Phone) VALUES (1, 'ivanivanov@gmail.com', '+7(888)999-01-01');
