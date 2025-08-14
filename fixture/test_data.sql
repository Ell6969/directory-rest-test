INSERT INTO buildings (id, address, latitude, longitude, geom) VALUES
(1, 'ул. Ленина, 1', 55.7558, 37.6173, ST_SetSRID(ST_MakePoint(37.6173, 55.7558), 4326)),
(2, 'ул. Пушкина, 10', 59.9343, 30.3351, ST_SetSRID(ST_MakePoint(30.3351, 59.9343), 4326)),
(3, 'ул. Гагарина, 15', 56.8389, 60.6057, ST_SetSRID(ST_MakePoint(60.6057, 56.8389), 4326)),
(4, 'пр. Мира, 20', 55.7961, 49.1064, ST_SetSRID(ST_MakePoint(49.1064, 55.7961), 4326)),
(5, 'ул. Свердлова, 5', 54.9833, 73.3672, ST_SetSRID(ST_MakePoint(73.3672, 54.9833), 4326)),
(6, 'ул. Лермонтова, 8', 59.9311, 30.3609, ST_SetSRID(ST_MakePoint(30.3609, 59.9311), 4326)),
(7, 'ул. Куйбышева, 3', 56.3269, 44.0059, ST_SetSRID(ST_MakePoint(44.0059, 56.3269), 4326)),
(8, 'ул. Октябрьская, 9', 55.0415, 82.9346, ST_SetSRID(ST_MakePoint(82.9346, 55.0415), 4326)),
(9, 'ул. Горького, 12', 51.5331, 46.0342, ST_SetSRID(ST_MakePoint(46.0342, 51.5331), 4326)),
(10, 'ул. Чехова, 18', 56.3269, 44.0059, ST_SetSRID(ST_MakePoint(44.0059, 56.3269), 4326));

INSERT INTO organizations (id, name, building_id, created_at, updated_at) VALUES
(1, 'Организация 1', 1, NOW(), NOW()),
(2, 'Организация 2', 2, NOW(), NOW()),
(3, 'Организация 3', 3, NOW(), NOW()),
(4, 'Организация 4', 4, NOW(), NOW()),
(5, 'Организация 5', 5, NOW(), NOW()),
(6, 'Организация 6', 6, NOW(), NOW()),
(7, 'Организация 7', 7, NOW(), NOW()),
(8, 'Организация 8', 8, NOW(), NOW()),
(9, 'Организация 9', 9, NOW(), NOW()),
(10, 'Организация 10', 10, NOW(), NOW());

-- Добавим 30 контактов — по 3 контакта на организацию с разными типами
INSERT INTO organization_contacts (id, organization_id, contact_type, value, description) VALUES
-- Организация 1
(1, 1, 'PHONE', '+7-900-000-0001', 'Основной телефон'),
(2, 1, 'EMAIL', 'org1@example.com', 'Основной email'),
(3, 1, 'TELEGRAM', '@org1', NULL),

-- Организация 2
(4, 2, 'PHONE', '+7-900-000-0002', 'Основной телефон'),
(5, 2, 'EMAIL', 'org2@example.com', 'Основной email'),
(6, 2, 'WHATSAPP', '+7-900-000-0002', NULL),

-- Организация 3
(7, 3, 'PHONE', '+7-900-000-0003', 'Основной телефон'),
(8, 3, 'EMAIL', 'org3@example.com', 'Основной email'),
(9, 3, 'OTHER', 'skype:org3', NULL),

-- Организация 4
(10, 4, 'PHONE', '+7-900-000-0004', 'Основной телефон'),
(11, 4, 'EMAIL', 'org4@example.com', 'Основной email'),
(12, 4, 'TELEGRAM', '@org4', NULL),

-- Организация 5
(13, 5, 'PHONE', '+7-900-000-0005', 'Основной телефон'),
(14, 5, 'EMAIL', 'org5@example.com', 'Основной email'),
(15, 5, 'WHATSAPP', '+7-900-000-0005', NULL),

-- Организация 6
(16, 6, 'PHONE', '+7-900-000-0006', 'Основной телефон'),
(17, 6, 'EMAIL', 'org6@example.com', 'Основной email'),
(18, 6, 'OTHER', 'skype:org6', NULL),

-- Организация 7
(19, 7, 'PHONE', '+7-900-000-0007', 'Основной телефон'),
(20, 7, 'EMAIL', 'org7@example.com', 'Основной email'),
(21, 7, 'TELEGRAM', '@org7', NULL),

-- Организация 8
(22, 8, 'PHONE', '+7-900-000-0008', 'Основной телефон'),
(23, 8, 'EMAIL', 'org8@example.com', 'Основной email'),
(24, 8, 'WHATSAPP', '+7-900-000-0008', NULL),

-- Организация 9
(25, 9, 'PHONE', '+7-900-000-0009', 'Основной телефон'),
(26, 9, 'EMAIL', 'org9@example.com', 'Основной email'),
(27, 9, 'OTHER', 'skype:org9', NULL),

-- Организация 10
(28, 10, 'PHONE', '+7-900-000-0010', 'Основной телефон'),
(29, 10, 'EMAIL', 'org10@example.com', 'Основной email'),
(30, 10, 'TELEGRAM', '@org10', NULL);

INSERT INTO activities (id, name, parent_id, level) VALUES
(1, 'Деятельность 1', NULL, 1),
(2, 'Деятельность 2', NULL, 1),
(3, 'Деятельность 3', NULL, 1),

(4, 'Поддеятельность 1.1', 1, 2),
(5, 'Поддеятельность 1.2', 1, 2),
(6, 'Поддеятельность 2.1', 2, 2),
(7, 'Поддеятельность 2.2', 2, 2),
(8, 'Поддеятельность 3.1', 3, 2),
(9, 'Поддеятельность 3.2', 3, 2),

(10, 'Подподдеятельность 1.1.1', 4, 3),
(11, 'Подподдеятельность 1.1.2', 4, 3),
(12, 'Подподдеятельность 1.2.1', 5, 3),
(13, 'Подподдеятельность 1.2.2', 5, 3),
(14, 'Подподдеятельность 2.1.1', 6, 3),
(15, 'Подподдеятельность 2.1.2', 6, 3),
(16, 'Подподдеятельность 2.2.1', 7, 3),
(17, 'Подподдеятельность 2.2.2', 7, 3),
(18, 'Подподдеятельность 3.1.1', 8, 3),
(19, 'Подподдеятельность 3.1.2', 8, 3),
(20, 'Подподдеятельность 3.2.1', 9, 3),
(21, 'Подподдеятельность 3.2.2', 9, 3),

(22, 'Деятельность 4', NULL, 1),
(23, 'Деятельность 5', NULL, 1),
(24, 'Деятельность 6', NULL, 1),
(25, 'Деятельность 7', NULL, 1),
(26, 'Деятельность 8', NULL, 1),
(27, 'Деятельность 9', NULL, 1),
(28, 'Деятельность 10', NULL, 1);

-- Организация 1
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(1, 1),
(1, 4),
(1, 10);

-- Организация 2
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(2, 2),
(2, 6),
(2, 14);

-- Организация 3
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(3, 3),
(3, 8),
(3, 18);

-- Организация 4
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(4, 1),
(4, 5),
(4, 12);

-- Организация 5
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(5, 2),
(5, 7),
(5, 16);

-- Организация 6
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(6, 3),
(6, 9),
(6, 20);

-- Организация 7
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(7, 1),
(7, 4),
(7, 11);

-- Организация 8
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(8, 2),
(8, 6),
(8, 15);

-- Организация 9
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(9, 3),
(9, 8),
(9, 19);

-- Организация 10
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(10, 1),
(10, 5),
(10, 13);