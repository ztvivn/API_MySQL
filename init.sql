CREATE TABLE organization_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    director_lastname VARCHAR(255) NOT NULL
);

CREATE TABLE correspondence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correspondence_type VARCHAR(255) NOT NULL,
    preparation_date DATE NOT NULL,
    organization_name VARCHAR(255) NOT NULL
);

