CREATE DATABASE Solaire;
USE Solaire;
CREATE TABLE batterie(
    idBatterie INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    rendement DOUBLE NOT NULL,
    capacite DOUBLE,
    chargeDebut TIME,
    chargeFin TIME
);
CREATE TABLE panneau(
    idPanneau INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    rendement DOUBLE NOT NULL,
    puissanceA DOUBLE,
    puissanceB DOUBLE,
    energie DOUBLE,
    prixUnitaire DOUBLE
);
CREATE TABLE energieSolaire(
    idEnergie INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    pourcentage DOUBLE NOT NULL,
    heureDebut TIME,
    heureFin TIME,
    ref1 VARCHAR(100)
);
CREATE TABLE appareil(
    idAppareil INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL
);
CREATE TABLE consommation(
    idConsommation INT PRIMARY KEY AUTO_INCREMENT,
    idAppareil INT,
    heureDebut TIME,
    heureFin TIME,
    consommation DOUBLE
);