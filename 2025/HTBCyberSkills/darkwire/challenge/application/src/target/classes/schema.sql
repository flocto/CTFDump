CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'ROLE_EMPLOYEE'
);


CREATE TABLE reports (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'PENDING',
    description TEXT,
    uploaded_at TIMESTAMP,
    user_id BIGINT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE package (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    version VARCHAR(50),
    type VARCHAR(50),
    description TEXT,
    filename VARCHAR(255),
    status VARCHAR(50),
    uploaded_at TIMESTAMP,
    uploaded_by BIGINT,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);
