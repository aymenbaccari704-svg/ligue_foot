DROP TABLE IF EXISTS MATCHS;
DROP TABLE IF EXISTS EQUIPES;

CREATE TABLE EQUIPES(
    equipe_id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(20),
    ville VARCHAR(20)
);

CREATE TABLE MATCHS(
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    equipe_domicile VARCHAR(20),
    equipe_exterieur VARCHAR(20),
    score_domicile INT,
    score_exterieur INT
);

