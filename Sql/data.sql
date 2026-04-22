USE Solaire;
GO

IF COL_LENGTH('panneau', 'prixWeekend') IS NULL
BEGIN
	ALTER TABLE panneau ADD prixWeekend FLOAT NULL;
END
GO

-- Appareil de reference (idAppareil = 1)
INSERT INTO appareil (nom) VALUES
('TV'),
('Ventilateur'),
('Refrigerateur'),
('Lampe'),
('Routeur WiFi');
GO

-- Consommations
INSERT INTO consommation (idAppareil, heureDebut, heureFin, consommation) VALUES
(1, '08:00:00', '12:00:00', 55),   -- TV
(2, '10:00:00', '14:00:00', 75),   -- Ventilateur
(3, '06:00:00', '17:00:00', 120),  -- Refrigerateur
(4, '17:00:00', '19:00:00', 10),   -- Lampe
(1, '17:00:00', '19:00:00', 55),   -- TV
(5, '19:00:00', '06:00:00', 10),   -- Routeur WiFi
(3, '19:00:00', '06:00:00', 120),  -- Refrigerateur
(4, '19:00:00', '23:00:00', 10);   -- Lampe
GO

-- Tranches d'energie solaire
INSERT INTO energieSolaire (nom, pourcentage, heureDebut, heureFin, ref1) VALUES
('AM', 1.0, '06:00:00', '17:00:00', NULL),
('FA', 0.5, '17:00:00', '19:00:00', NULL),
('PM', 0.0, '19:00:00', '06:00:00', NULL);
GO

-- 1 batterie
INSERT INTO batterie (nom, rendement, capacite, chargeDebut, chargeFin) VALUES
('Batterie 12V', 0.9, 200, '19:00:00', '06:00:00');
GO

-- 1 panneau
INSERT INTO panneau (nom, rendement, puissanceA, puissanceB, energie, prixUnitaire, prixWeekend) VALUES
('Panneau 450W', 0.92, 450, 0, 4.5, 850000, NULL);
GO


