-- Briefly PostgreSQL bootstrap script
-- Run automatically on first container startup via docker-entrypoint-initdb.d
-- In production, use Alembic migrations instead.

-- ── Enable extensions ──────────────────────────────────────────────────────
-- TODO: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- TODO: CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── users ──────────────────────────────────────────────────────────────────
-- TODO: CREATE TABLE users (
--     id                  SERIAL PRIMARY KEY,
--     email               VARCHAR(255) UNIQUE NOT NULL,
--     hashed_password     VARCHAR(255) NOT NULL,
--     full_name           VARCHAR(255),
--     is_active           BOOLEAN NOT NULL DEFAULT TRUE,
--     reset_token         VARCHAR(255),
--     reset_token_expires TIMESTAMPTZ,
--     created_at          TIMESTAMPTZ DEFAULT NOW(),
--     updated_at          TIMESTAMPTZ
-- );

-- ── news ───────────────────────────────────────────────────────────────────
-- TODO: CREATE TABLE news (
--     id           SERIAL PRIMARY KEY,
--     url_hash     CHAR(64) UNIQUE NOT NULL,
--     title        VARCHAR(512) NOT NULL,
--     description  TEXT,
--     content      TEXT,
--     url          TEXT NOT NULL,
--     source       VARCHAR(255),
--     category     VARCHAR(50) NOT NULL,
--     published_at TIMESTAMPTZ,
--     summary      TEXT,
--     embedding    JSONB,
--     created_at   TIMESTAMPTZ DEFAULT NOW()
-- );
-- TODO: CREATE INDEX idx_news_category ON news(category);
-- TODO: CREATE INDEX idx_news_published ON news(published_at DESC);

-- ── survey_preferences ─────────────────────────────────────────────────────
-- TODO: CREATE TABLE survey_preferences (
--     id                SERIAL PRIMARY KEY,
--     user_id           INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     categories        JSONB NOT NULL DEFAULT '[]',
--     frequency         VARCHAR(50),
--     preferred_sources JSONB DEFAULT '[]',
--     interest_vector   JSONB DEFAULT '{}',
--     survey_completed  SMALLINT NOT NULL DEFAULT 0,
--     created_at        TIMESTAMPTZ DEFAULT NOW(),
--     updated_at        TIMESTAMPTZ
-- );

-- ── user_interactions ──────────────────────────────────────────────────────
-- TODO: CREATE TABLE user_interactions (
--     id           SERIAL PRIMARY KEY,
--     user_id      INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     article_id   INT NOT NULL REFERENCES news(id) ON DELETE CASCADE,
--     action       VARCHAR(30) NOT NULL,
--     read_time    FLOAT,
--     scroll_depth FLOAT,
--     created_at   TIMESTAMPTZ DEFAULT NOW()
-- );
-- TODO: CREATE INDEX idx_interactions_user    ON user_interactions(user_id);
-- TODO: CREATE INDEX idx_interactions_article ON user_interactions(article_id);

SELECT 'Briefly DB bootstrap loaded.' AS status;
