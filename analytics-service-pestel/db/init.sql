-- ============================================
-- База данных: PESTEL Risk Analysis Service
-- ============================================

CREATE DATABASE IF NOT EXISTS business_sustainability
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE business_sustainability;
SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;

-- ============================================
-- 1. Цели устойчивого развития (ЦУР)
-- ============================================

CREATE TABLE sdg_goal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE COMMENT 'Код ЦУР (7, 12 и т.д.)',
    name VARCHAR(255) NOT NULL COMMENT 'Название цели',
    description TEXT COMMENT 'Описание цели'
) COMMENT='Цели устойчивого развития ООН';

-- ============================================
-- 2. Индикаторы устойчивости (обобщённые)
-- ============================================

CREATE TABLE indicator (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT 'Название индикатора',
    description TEXT COMMENT 'Описание индикатора',
    sdg_goal_id INT NOT NULL,
    block_type ENUM('ECONOMIC','SOCIAL','ENVIRONMENTAL','GOVERNANCE') NOT NULL,
    base_weight DECIMAL(5,2) DEFAULT 1.00 COMMENT 'Базовый вес индикатора',

    CONSTRAINT fk_indicator_sdg
        FOREIGN KEY (sdg_goal_id)
        REFERENCES sdg_goal(id)
        ON DELETE RESTRICT
) COMMENT='Индикаторы устойчивого развития (обобщённые)';

-- ============================================
-- 3. PESTEL-факторы внешней среды
-- ============================================

CREATE TABLE pestel_factor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('P','E','S','T','E2','L') NOT NULL COMMENT 'PESTEL тип (E2 = Environmental)',
    title VARCHAR(255) NOT NULL COMMENT 'Краткое название фактора',
    description TEXT COMMENT 'Описание фактора',
    base_risk_level ENUM('LOW','MEDIUM','HIGH') NOT NULL,
    trend ENUM('POSITIVE','NEGATIVE','NEUTRAL') DEFAULT 'NEUTRAL'
) COMMENT='Факторы внешней среды PESTEL';

-- ============================================
-- 4. Влияние PESTEL-факторов на индикаторы
-- ============================================

CREATE TABLE pestel_indicator_impact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pestel_factor_id INT NOT NULL,
    indicator_id INT NOT NULL,
    impact_type ENUM('RISK','OPPORTUNITY') NOT NULL,
    impact_strength DECIMAL(5,2) NOT NULL COMMENT 'Сила влияния (0..1)',

    CONSTRAINT fk_impact_factor
        FOREIGN KEY (pestel_factor_id)
        REFERENCES pestel_factor(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_impact_indicator
        FOREIGN KEY (indicator_id)
        REFERENCES indicator(id)
        ON DELETE CASCADE
) COMMENT='Связь факторов PESTEL с индикаторами устойчивости';

-- ============================================
-- 5. Агрегированная оценка рисков
-- ============================================

CREATE TABLE risk_assessment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pestel_factor_id INT NOT NULL,
    total_risk_score DECIMAL(5,2) NOT NULL COMMENT 'Итоговый риск фактора',
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_risk_factor
        FOREIGN KEY (pestel_factor_id)
        REFERENCES pestel_factor(id)
        ON DELETE CASCADE
) COMMENT='Агрегированная оценка рисков PESTEL';

-- ============================================
-- 6. Новости (для будущего парсера)
-- ============================================

CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(255) NOT NULL COMMENT 'Источник новости',
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    published_at DATETIME NOT NULL
) COMMENT='Новости внешней среды';

-- ============================================
-- 7. Влияние новостей на PESTEL-факторы
-- ============================================

CREATE TABLE news_pestel_impact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    news_id INT NOT NULL,
    pestel_factor_id INT NOT NULL,
    impact_delta DECIMAL(5,2) NOT NULL COMMENT 'Изменение риска (+/-)',

    CONSTRAINT fk_news_impact_news
        FOREIGN KEY (news_id)
        REFERENCES news(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_news_impact_factor
        FOREIGN KEY (pestel_factor_id)
        REFERENCES pestel_factor(id)
        ON DELETE CASCADE
) COMMENT='Влияние новостей на факторы PESTEL';



-- ================================
-- ЗАПОЛНЕНИЕ БД
-- ================================


SET FOREIGN_KEY_CHECKS = 1;

-- ================
-- 1) SDG (твой список)
-- ================
INSERT INTO sdg_goal (code, name, description) VALUES
('1','Ликвидация бедности','Социальная защита, уязвимые группы'),
('3','Здоровье и благополучие','Охрана здоровья, безопасность труда'),
('4','Качественное образование','Обучение, навыки, подготовка кадров'),
('5','Гендерное равенство','Равные возможности'),
('6','Чистая вода и санитария','Вода, санитария, инфраструктура'),
('7','Доступная и чистая энергия','Энергоэффективность и энергия'),
('8','Достойная работа и экономический рост','МСБ, занятость, рост'),
('9','Индустриализация, инновации и инфраструктура','Технологии, инновации'),
('10','Уменьшение неравенства','Доступность и равные условия'),
('12','Ответственное потребление и производство','Отходы, ресурсы'),
('13','Борьба с изменением климата','Экология и климат'),
('14','Сохранение морских экосистем','Водоёмы и экосистемы'),
('15','Сохранение экосистем суши','Земля, биоразнообразие'),
('16','Мир, правосудие и эффективные институты','Право и институты'),
('17','Партнёрство в интересах устойчивого развития','Сотрудничество и партнёрства');

-- ================
-- 2) PESTEL FACTORS (6 типов)
-- ================
INSERT INTO pestel_factor (type, title, description, base_risk_level, trend) VALUES
('P','Госполитика и поддержка МСБ','Субсидии, госпрограммы, приоритеты', 'MEDIUM','NEUTRAL'),
('E','Макроэкономика и финансы','Инфляция, ставки, тарифы, курс',      'HIGH','NEGATIVE'),
('S','Социальная среда и рынок труда','Занятость, МЗП, миграция, ценности','MEDIUM','NEUTRAL'),
('T','Цифровизация и инновации','ИИ, автоматизация, киберриски',         'MEDIUM','POSITIVE'),
('E2','Экология и требования устойчивости','Нормы, штрафы, ESG, отходы',   'HIGH','NEGATIVE'),
('L','Правовое регулирование и контроль','Налоги, проверки, комплаенс',    'HIGH','NEGATIVE');

-- ================
-- 3) INDICATORS (реалистично, с правильными SDG)
-- ================
-- P -> SDG_17 (партнерство), SDG_8
INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Партнерства и программы поддержки', 'Участие бизнеса в госпрограммах, грантах, кластерах', id, 'GOVERNANCE', 1.00
FROM sdg_goal WHERE code='17';

INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Развитие занятости и МСБ', 'Рост занятости и устойчивость МСБ', id, 'ECONOMIC', 1.20
FROM sdg_goal WHERE code='8';

-- E -> SDG_8, SDG_7
INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Финансовая устойчивость', 'Инфляция, ставки, доступ к финансированию', id, 'ECONOMIC', 1.30
FROM sdg_goal WHERE code='8';

INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Энергоэффективность', 'Зависимость бизнеса от тарифов и энергоэффективности', id, 'ENVIRONMENTAL', 1.10
FROM sdg_goal WHERE code='7';

-- S -> SDG_3, SDG_4, SDG_5
INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Охрана труда и здоровье', 'Безопасность труда, профилактика, условия', id, 'SOCIAL', 1.10
FROM sdg_goal WHERE code='3';

INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Развитие компетенций', 'Обучение персонала, повышение квалификации', id, 'SOCIAL', 1.00
FROM sdg_goal WHERE code='4';

INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Равные возможности', 'Гендерное равенство и недискриминация', id, 'SOCIAL', 0.90
FROM sdg_goal WHERE code='5';

-- T -> SDG_9
INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Цифровая зрелость', 'Уровень цифровизации и инноваций', id, 'GOVERNANCE', 1.20
FROM sdg_goal WHERE code='9';

-- E2 -> SDG_12, SDG_13
INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Управление отходами', 'Утилизация, снижение отходов, переработка', id, 'ENVIRONMENTAL', 1.20
FROM sdg_goal WHERE code='12';

INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Снижение выбросов', 'Сокращение выбросов и климатические меры', id, 'ENVIRONMENTAL', 1.30
FROM sdg_goal WHERE code='13';

-- L -> SDG_16
INSERT INTO indicator (name, description, sdg_goal_id, block_type, base_weight)
SELECT 'Правовая прозрачность и комплаенс', 'Соблюдение норм, налоги, отчетность', id, 'GOVERNANCE', 1.30
FROM sdg_goal WHERE code='16';

-- ================
-- 4) PESTEL -> INDICATOR IMPACTS (чтобы SDG подтягивались)
-- ================
-- P (id=1)
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 1, id, 'OPPORTUNITY', 0.60 FROM indicator WHERE name='Партнерства и программы поддержки';
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 1, id, 'OPPORTUNITY', 0.50 FROM indicator WHERE name='Развитие занятости и МСБ';

-- E (id=2)
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 2, id, 'RISK', 0.80 FROM indicator WHERE name='Финансовая устойчивость';
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 2, id, 'RISK', 0.70 FROM indicator WHERE name='Энергоэффективность';

-- S (id=3)
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 3, id, 'RISK', 0.60 FROM indicator WHERE name='Охрана труда и здоровье';
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 3, id, 'OPPORTUNITY', 0.50 FROM indicator WHERE name='Развитие компетенций';
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 3, id, 'OPPORTUNITY', 0.40 FROM indicator WHERE name='Равные возможности';

-- T (id=4)
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 4, id, 'OPPORTUNITY', 0.70 FROM indicator WHERE name='Цифровая зрелость';

-- E2 (id=5)
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 5, id, 'RISK', 0.90 FROM indicator WHERE name='Управление отходами';
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 5, id, 'RISK', 0.85 FROM indicator WHERE name='Снижение выбросов';

-- L (id=6)
INSERT INTO pestel_indicator_impact (pestel_factor_id, indicator_id, impact_type, impact_strength)
SELECT 6, id, 'RISK', 0.85 FROM indicator WHERE name='Правовая прозрачность и комплаенс';

-- ================
-- 5) NEWS (18 новостей: 6 типов * 3)
-- ================
INSERT INTO news (source, title, content, published_at) VALUES
-- P (Political)
('gov.kz','Запущена новая программа грантов для МСБ','Государство расширяет поддержку предпринимателей...', NOW()),
('tengrinews.kz','Обновлены правила субсидирования процентных ставок','Меняются условия получения субсидий...', NOW()),
('informburo.kz','В регионах создают центры поддержки предпринимателей','Открываются новые инфраструктурные центры...', NOW()),

-- E (Economic)
('kapital.kz','Инфляция ускорилась: бизнес ожидает роста издержек','Рост цен влияет на себестоимость...', NOW()),
('kursiv.kz','Тарифы на электроэнергию повышаются для коммерческого сектора','Энергозатраты вырастут...', NOW()),
('forbes.kz','Ставки по кредитам для бизнеса остаются высокими','Доступ к финансам усложняется...', NOW()),

-- S (Social)
('tengrinews.kz','Обсуждается повышение минимальной зарплаты','Рост МЗП влияет на фонд оплаты труда...', NOW()),
('informburo.kz','Дефицит кадров усиливается в сервисном секторе','Компании конкурируют за работников...', NOW()),
('kapital.kz','Растет спрос на обучение сотрудников внутри компаний','Бизнес инвестирует в компетенции...', NOW()),

-- T (Technological)
('forbes.kz','Компании активнее внедряют автоматизацию в процессы','Автоматизация сокращает издержки...', NOW()),
('kursiv.kz','В Казахстане расширяют использование электронных счет-фактур','Цифровые инструменты становятся обязательными...', NOW()),
('kapital.kz','Рост кибератак заставляет бизнес усиливать защиту','Участились инциденты информационной безопасности...', NOW()),

-- E2 (Environmental)
('zakon.kz','Ужесточаются требования к утилизации отходов для предприятий','Новые правила по отходам...', NOW()),
('informburo.kz','Экологические штрафы увеличены за нарушения норм выбросов','Повышены санкции за экологические нарушения...', NOW()),
('tengrinews.kz','Государство стимулирует энергоэффективные проекты','Запускаются меры поддержки по снижению выбросов...', NOW()),

-- L (Legal)
('zakon.kz','Налоговые органы получат доступ к банковским данным','Усиление контроля за финансовыми операциями...', NOW()),
('informburo.kz','Изменения в налоговом кодексе затронут малый бизнес','Появятся новые требования по отчетности...', NOW()),
('kapital.kz','Ужесточаются проверки по соблюдению трудового законодательства','Контроль за оформлением сотрудников...', NOW());

-- ================
-- 6) NEWS -> PESTEL IMPACTS (каждая новость к своему фактору)
-- impact_delta: >0 THREAT, <0 OPPORTUNITY
-- ================
INSERT INTO news_pestel_impact (news_id, pestel_factor_id, impact_delta) VALUES
-- P news_id 1..3 -> factor 1 (P)
(1,1,-0.50),
(2,1,-0.40),
(3,1,-0.35),

-- E news_id 4..6 -> factor 2 (E)
(4,2,0.80),
(5,2,0.90),
(6,2,0.75),

-- S news_id 7..9 -> factor 3 (S)
(7,3,0.55),
(8,3,0.65),
(9,3,-0.45),

-- T news_id 10..12 -> factor 4 (T)
(10,4,-0.60),
(11,4,-0.50),
(12,4,0.70),

-- E2 news_id 13..15 -> factor 5 (E2)
(13,5,0.90),
(14,5,0.95),
(15,5,-0.50),

-- L news_id 16..18 -> factor 6 (L)
(16,6,0.85),
(17,6,0.80),
(18,6,0.70);

