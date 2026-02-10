-- Suppression des tables si elles existent (pour repartir à neuf)
DROP TABLE IF EXISTS Scores;
DROP TABLE IF EXISTS Players;

-- 1. Création de la table Players 
CREATE TABLE Players (
    player_id INT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    registration_date DATE,
    country VARCHAR(100),
    level INT
);

-- 2. Création de la table Scores
CREATE TABLE Scores (
    score_id VARCHAR(20) PRIMARY KEY,
    player_id INT,
    game VARCHAR(100),
    score INT,
    duration_minutes INT,
    played_at DATETIME,
    platform VARCHAR(50),
    -- Clé étrangère vers la table Players
    CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES Players(player_id) ON DELETE CASCADE
);