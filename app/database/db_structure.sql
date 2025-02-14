CREATE TABLE user (
    chat_id BIGINT(30) PRIMARY KEY,
    full_name CHAR(255) DEFAULT NULL,
    user_name CHAR(255) DEFAULT NULL,
    invited_by BIGINT(30) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invited_by) REFERENCES user(chat_id) ON DELETE CASCADE
);

CREATE TABLE servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    version VARCHAR(10) NOT NULL,
    server_path VARCHAR(255) NOT NULL
);

CREATE TABLE server_properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT,
    property_name VARCHAR(255) NOT NULL,
    property_value TEXT NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

CREATE TABLE java_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT,
    server_file VARCHAR(255) NOT NULL,
    min_ram INT NOT NULL,
    max_ram INT NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);