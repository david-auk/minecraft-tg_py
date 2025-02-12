CREATE TABLE user (
    chat_id CHAR(30) PRIMARY KEY,
    name CHAR(255) DEFAULT NULL,
    invited_by CHAR(12),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invited_by) REFERENCES user(chat_id) ON DELETE CASCADE
);