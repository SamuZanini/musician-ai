-- Script SQL para criar as tabelas do banco de dados
-- Database para aplicativo #Dô - Assistente de Prática Musical com Detecção de Áudio via ML

CREATE DATABASE IF NOT EXISTS musician_ai;
USE musician_ai;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),
    bio TEXT,
    favorite_instrument_id VARCHAR(36),
    subscription_plan VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de instrumentos
CREATE TABLE IF NOT EXISTS instruments (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT,
    faq_content JSON,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de compositores
CREATE TABLE IF NOT EXISTS composers (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    biography TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de partituras
CREATE TABLE IF NOT EXISTS sheet_music (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    composer_id VARCHAR(36) NOT NULL,
    instrument_id VARCHAR(36),
    description TEXT,
    image_url VARCHAR(500),
    file_url VARCHAR(500),
    difficulty VARCHAR(50),
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (composer_id) REFERENCES composers(id) ON DELETE CASCADE,
    FOREIGN KEY (instrument_id) REFERENCES instruments(id) ON DELETE SET NULL
);

-- Tabela de sessões de prática
CREATE TABLE IF NOT EXISTS practice_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    instrument_id VARCHAR(36) NOT NULL,
    duration_minutes INT NOT NULL DEFAULT 0,
    accuracy_score INT DEFAULT 0,
    notes_played INT DEFAULT 0,
    notes_correct INT DEFAULT 0,
    session_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (instrument_id) REFERENCES instruments(id) ON DELETE CASCADE
);

-- Tabela de estatísticas do usuário
CREATE TABLE IF NOT EXISTS user_statistics (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE NOT NULL,
    total_practice_time INT DEFAULT 0,
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    total_sessions INT DEFAULT 0,
    total_stars INT DEFAULT 0,
    last_practice_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de assinaturas
CREATE TABLE IF NOT EXISTS subscriptions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    plan_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    price DECIMAL(10, 2),
    billing_cycle VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Inserir instrumentos padrão
INSERT INTO instruments (id, name, type, description, faq_content) VALUES
('violin-001', 'Violino', 'string', 'Instrumento de cordas friccionadas', '{"faq": [{"question": "Como afinar?", "answer": "Use a afinação EADG de cima para baixo."}, {"question": "Qual é a melhor técnica de arco?", "answer": "Mantenha o arco perpendicular às cordas."}]}'),
('flute-001', 'Flauta', 'wind', 'Instrumento de sopro', '{"faq": [{"question": "Como começar?", "answer": "Aprenda a posição de embocadura correta."}, {"question": "Notas básicas", "answer": "Comece com dó, ré e mi."}]}'),
('trumpet-001', 'Trompete', 'wind', 'Instrumento de sopro de latão', '{"faq": [{"question": "Como produzir som?", "answer": "Use vibração de lábios na embocadura."}, {"question": "Cuidado com o instrumento", "answer": "Limpe sempre após o uso."}]}'),
('piano-001', 'Piano', 'keyboard', 'Instrumento de teclas com 88 notas', '{"faq": [{"question": "Posição das mãos", "answer": "Mantenha os pulsos retos e relaxados."}, {"question": "Técnica de dedos", "answer": "Use numeração: 1=polegar, 5=mindinho."}]}'),
('cello-001', 'Cello', 'string', 'Instrumento de cordas graves', '{"faq": [{"question": "Como segurar?", "answer": "Entre as pernas, apoiado no ombro."}, {"question": "Afinação", "answer": "CGDA de cima para baixo."}]}');

-- Inserir compositores
INSERT INTO composers (id, name, biography) VALUES
('chopin-001', 'Frédéric Chopin', 'Compositor e pianista polonês do século XIX, conhecido por suas obras para piano.'),
('bach-001', 'Johann Sebastian Bach', 'Compositor barroco alemão, mestre do contraponto e composição coral.'),
('beethoven-001', 'Ludwig van Beethoven', 'Compositor alemão que fez a transição do Clássico ao Romântico.'),
('paganini-001', 'Niccolò Paganini', 'Violinista e compositor italiano, revolucionou a técnica do violino.'),
('vivaldi-001', 'Antonio Vivaldi', 'Compositor veneziano, famoso pelas Quatro Estações.');

-- Inserir partituras
INSERT INTO sheet_music (id, title, composer_id, instrument_id, description, difficulty, is_premium) VALUES
('nocturne-001', 'Nocturne Op. 9 No. 2', 'chopin-001', 'piano-001', 'Uma das obras mais famosas de Chopin', 'intermediate', FALSE),
('prelude-001', 'Prelude in C Major', 'bach-001', 'piano-001', 'Primeira parte do WTC Book I', 'beginner', FALSE),
('moonlight-001', 'Sonata ao Luar', 'beethoven-001', 'piano-001', 'Sonata clássica para piano', 'advanced', TRUE),
('caprice-001', 'Caprice No. 24', 'paganini-001', 'violin-001', 'Obra desafiadora para violino', 'advanced', TRUE),
('four-seasons-001', 'As Quatro Estações', 'vivaldi-001', 'violin-001', 'Concertos para violino e orquestra', 'intermediate', FALSE);

-- Índices para melhor performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_favorite_instrument ON users(favorite_instrument_id);
CREATE INDEX idx_practice_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_practice_sessions_instrument_id ON practice_sessions(instrument_id);
CREATE INDEX idx_practice_sessions_date ON practice_sessions(session_date);
CREATE INDEX idx_sheet_music_composer ON sheet_music(composer_id);
CREATE INDEX idx_sheet_music_instrument ON sheet_music(instrument_id);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_user_statistics_user_id ON user_statistics(user_id);