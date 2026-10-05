-- Feature: UUID native type (MariaDB 10.7+)

-- OLD WAY: store UUIDs as CHAR(36) — 36 bytes, no validation, wrong sort order

CREATE TABLE IF NOT EXISTS sessions_old (
    id         INT    AUTO_INCREMENT PRIMARY KEY,
    session_id CHAR(36) NOT NULL,
    user_name  VARCHAR(100) NOT NULL
);

INSERT INTO sessions_old (session_id, user_name) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'alice'),
    ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'bob'),
    ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'carol');

-- CHAR(36) accepts anything — no validation
INSERT INTO sessions_old (session_id, user_name) VALUES
    ('not-a-uuid-at-all', 'mallory'); -- silently accepted

SELECT id, session_id, user_name FROM sessions_old;

-- NEW WAY: UUID — 16 bytes, validates format, correct sort order

CREATE TABLE IF NOT EXISTS sessions_new (
    id         INT  AUTO_INCREMENT PRIMARY KEY,
    session_id UUID NOT NULL DEFAULT UUID(),
    user_name  VARCHAR(100) NOT NULL
);

-- UUID() generates a valid v1 UUID automatically
INSERT INTO sessions_new (user_name) VALUES ('alice');
INSERT INTO sessions_new (user_name) VALUES ('bob');
INSERT INTO sessions_new (user_name) VALUES ('carol');

SELECT id, session_id, user_name FROM sessions_new;

-- UUID rejects invalid values at INSERT time
-- INSERT INTO sessions_new (session_id, user_name) VALUES ('not-a-uuid', 'mallory');
-- ERROR 1292 (22007): Incorrect uuid value: 'not-a-uuid'

-- UUID stores as 16 bytes vs CHAR(36) = 36 bytes — 2.25x smaller per row
SELECT
    16  AS uuid_bytes,
    36  AS char36_bytes,
    ROUND(36 / 16, 2) AS size_ratio;
