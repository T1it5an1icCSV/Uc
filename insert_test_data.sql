-- Вставка тестовых категорий
INSERT INTO store_category (name, slug, description) VALUES
('Инструменты', 'tools', 'Ручные и электроинструменты для строительства и ремонта'),
('Крепеж', 'fasteners', 'Гвозди, шурупы, болты и другие крепежные элементы'),
('Отделочные материалы', 'finishing', 'Краски, штукатурки, обои и другие отделочные материалы'),
('Сантехника', 'plumbing', 'Трубы, фитинги, смесители и другие сантехнические изделия');

-- Вставка тестовых продуктов
INSERT INTO store_product (category_id, name, slug, description, price, stock, available) VALUES
(1, 'Молоток строительный', 'hammer', 'Профессиональный молоток с деревянной ручкой', 1200.00, 50, true),
(1, 'Дрель электрическая', 'drill', 'Мощная дрель с набором сверл', 3500.00, 30, true),
(2, 'Шурупы по дереву', 'wood-screws', 'Набор шурупов 100 шт.', 250.00, 200, true),
(2, 'Дюбели универсальные', 'dowels', 'Набор дюбелей 50 шт.', 180.00, 150, true),
(3, 'Краска белая', 'white-paint', 'Водоэмульсионная краска 10л', 1200.00, 40, true),
(3, 'Обои флизелиновые', 'wallpaper', 'Рулон обоев 10м', 800.00, 60, true),
(4, 'Смеситель для ванной', 'bath-mixer', 'Современный смеситель с душем', 2500.00, 25, true),
(4, 'Труба ПВХ 50мм', 'pvc-pipe', 'Труба ПВХ 3м', 350.00, 100, true);

-- Создание тестового пользователя (пароль: testpass123)
INSERT INTO auth_user (username, password, email, is_staff, is_active, is_superuser, date_joined)
VALUES ('testuser', 'pbkdf2_sha256$600000$hash', 'test@example.com', false, true, false, CURRENT_TIMESTAMP);

-- Создание тестового заказа
INSERT INTO store_order (user_id, first_name, last_name, email, address, city, phone, status, total_amount)
VALUES (1, 'Иван', 'Иванов', 'test@example.com', 'ул. Примерная, 1', 'Москва', '+79001234567', 'pending', 4700.00);

-- Добавление товаров в заказ
INSERT INTO store_orderitem (order_id, product_id, price, quantity)
VALUES 
(1, 1, 1200.00, 1),
(1, 3, 250.00, 2),
(1, 5, 1200.00, 1); 