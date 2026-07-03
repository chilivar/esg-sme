-- ============================================
-- База данных
-- ============================================

CREATE DATABASE IF NOT EXISTS business_sustainability
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE business_sustainability;

SET NAMES utf8mb4;

-- ============================================
-- 3. Новости (НЕ ТРОГАЕМ)
-- ============================================

CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    title_en VARCHAR(500),
    title_kz VARCHAR(500),
    url VARCHAR(1000),
    published_at DATETIME NOT NULL
) COMMENT='Новости';

-- ============================================
-- 4. Результат анализа новости
-- ============================================

CREATE TABLE news_analysis (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    news_id INT NOT NULL UNIQUE,

    pestel_type ENUM(
        'POLITICAL',
        'ECONOMIC',
        'SOCIAL',
        'TECHNOLOGICAL',
        'ENVIRONMENTAL',
        'LEGAL'
    ) NOT NULL,

    impact_type ENUM(
        'THREAT',
        'OPPORTUNITY'
    ) NOT NULL,

    impact_strength DECIMAL(5,2) NOT NULL COMMENT '0..1',

    sdg_codes VARCHAR(50) NOT NULL COMMENT 'например 8,7 или 13',

    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_news_analysis_news
        FOREIGN KEY (news_id)
        REFERENCES news(id)
        ON DELETE CASCADE
) COMMENT='Результат анализа новости';