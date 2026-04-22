-- Active: 1776292121099@@127.0.0.1@1433@model
CREATE DATABASE Solaire;
GO

USE Solaire;
GO

CREATE TABLE batterie (
    idBatterie INT IDENTITY(1,1) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    rendement FLOAT NOT NULL,
    capacite FLOAT,
    chargeDebut TIME,
    chargeFin TIME
);
GO

CREATE TABLE panneau (
    idPanneau INT IDENTITY(1,1) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    rendement FLOAT NOT NULL,
    puissanceA FLOAT,
    puissanceB FLOAT,
    energie FLOAT,
    prixUnitaire FLOAT,
    prixWeekend FLOAT NULL
);
GO

CREATE TABLE energieSolaire (
    idEnergie INT IDENTITY(1,1) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    pourcentage FLOAT NOT NULL,
    heureDebut TIME,
    heureFin TIME,
    ref1 VARCHAR(100)
);
GO

CREATE TABLE appareil (
    idAppareil INT IDENTITY(1,1) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);
GO

CREATE TABLE consommation (
    idConsommation INT IDENTITY(1,1) PRIMARY KEY,
    idAppareil INT,
    heureDebut TIME,
    heureFin TIME,
    consommation FLOAT
);
GO

CREATE TABLE prix (
    idPrix INT IDENTITY(1,1) PRIMARY KEY,
    prixOuvrable FLOAT,
    prixWeekend FLOAT,
    puissance FLOAT
);

CREATE TABLE augmentation (
    idAugmentation INT IDENTITY(1,1) PRIMARY KEY,
    pourcentageOuvrable FLOAT,
    pourcentageWeekend FLOAT,
    heureDebut TIME,
    heureFin TIME
);