-- Создание базы данных
CREATE DATABASE construction_store;

-- Подключение к созданной базе данных
\c construction_store;

-- Создание схемы для таблиц
CREATE SCHEMA IF NOT EXISTS store;

-- Установка поискового пути
SET search_path TO store, public;

-- Создание таблицы категорий
CREATE TABLE store_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    image VARCHAR(255)
);

-- Создание таблицы продуктов
CREATE TABLE store_product (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES store_category(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL,
    image VARCHAR(255),
    available BOOLEAN DEFAULT TRUE,
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы заказов
CREATE TABLE store_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    address VARCHAR(250) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL
);

-- Создание таблицы элементов заказа
CREATE TABLE store_orderitem (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES store_order(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES store_product(id) ON DELETE CASCADE,
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1
);

-- Создание индексов
CREATE INDEX idx_product_category ON store_product(category_id);
CREATE INDEX idx_product_slug ON store_product(slug);
CREATE INDEX idx_order_user ON store_order(user_id);
CREATE INDEX idx_orderitem_order ON store_orderitem(order_id);
CREATE INDEX idx_orderitem_product ON store_orderitem(product_id);

-- Создание триггера для автоматического обновления поля updated
CREATE OR REPLACE FUNCTION update_updated_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_updated
    BEFORE UPDATE ON store_product
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_column();

CREATE TRIGGER update_order_updated
    BEFORE UPDATE ON store_order
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_column(); 