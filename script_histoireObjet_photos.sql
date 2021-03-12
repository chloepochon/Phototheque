PRAGMA encoding = 'UTF-8';
-- base SQLite des photographies réalisées en 2016 dans le cadre du projet "Histoire de l'objet, objet de l'Histoire" par Chloé Pochon.

CREATE TABLE IF NOT EXISTS user (
	user_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_nom	TINYTEXT NOT NULL,
	user_login	VARCHAR ( 45 ) NOT NULL,
	user_email	TINYTEXT NOT NULL,
	user_password	VARCHAR ( 100 ) NOT NULL
);

CREATE TABLE IF NOT EXISTS photo (
	photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
	photo_titre TEXT NOT NULL,
	photo_description TEXT NOT NULL,
	photo_auteur TEXT NOT NULL,
	photo_date TEXT NOT NULL,
	photo_tag TEXT NOT NULL,
	photo_orientation TEXT NOT NULL,
	photo_chemin TEXT NOT NULL,
	photo_fichier TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS authorship (
	authorship_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	authorship_user_id	integer NOT NULL,
	authorship_photo_id	integer NOT NULL,
	authorship_date	DATETIME DEFAULT current_timestamp,
	FOREIGN KEY(authorship_user_id) REFERENCES user(user_id),
	FOREIGN KEY(authorship_photo_id) REFERENCES photo(photo_id)
);

CREATE INDEX IF NOT EXISTS `fk_authorship_2_idx` ON `authorship` (
	`authorship_user_id`	ASC
);

CREATE INDEX IF NOT EXISTS `fk_authorship_1_idx` ON `authorship` (
	`authorship_photo_id`	ASC
);


INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Carnet de poèmes de Alexis Nouët', 'Carnet de poèmes écrits par Alexis Nouët lors de sa détention en Allemagne entre 1940 et 1945. Il lui servit également de cahier de vocabulaire.', 'Chloé Pochon', '2016', 'Seconde guerre mondiale', 'portrait', '<img src="/static/img/cahieranouet.jpg"/>', 'cahieranouet.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Etoile jaune', 'Etoile jaune telle que devaient la porter les personnes juives en France en vertu de la huitième ordonnance du 29 mai 1942.', 'Chloé Pochon', '2016', 'Shoah', 'portrait', '<img src="/static/img/etoile.jpg"/>', 'etoile.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Lettre de Martial Brigouleix', 'Lettre clandestine écrite par le brigadier et résistant Martial Brigouleix à son épouse, peu avant son exécution', 'Chloé Pochon', '2016', 'Résistance', 'paysage', '<img src="/static/img/lettrebrigouleix.jpg"/>', 'lettrebrigouleix.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Montre à gousset', 'Montre à gousset qui appartenait à un soldat tombé au front. La réparer fut le premier ouvrage du bijoutier qui la détient actuellement.', 'Chloé Pochon', '2016', 'Seconde guerre mondiale', 'paysage', '<img src="/static/img/montre.jpg"/>', 'montre.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Mouchoir de Marie-José Chombart de Lauwe', 'Ce mouchoir lui fut brodé pour un de ses anniversaires par des résistantes détenues, lors de sa détention au camp de Ravensbrück. Il porte son matricule et le triangle rouge, symbole des détenu.e.s politiques.',  'Chloé Pochon', '2016', 'Résistance', 'paysage', '<img src="/static/img/chombartdelauwe.jpg"/>', 'chombartdelauwe.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Carte de Birkenau', 'Carte écrite depuis le camp de Birkenau en juillet 1943. Destinée aux personnes peu avant leur assassinat pour obtenir les adresses des familles, elles devaient être écrites en allemand et au crayon bois. Son auteur, juif et résistant, parvint à en subtiliser une et à la faire parvenir à sa famille, cachée par le réseau Libération Sud. Il a lui aussi survécu.', 'Chloé Pochon', '2016', 'Shoah', 'paysage', '<img src="/static/img/cartebirkenau.jpg"/>', 'cartebirkenau.jpg'); 
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Tableau de Bertrand Herz', 'Le tableau La première communion de Gotlieb Herz a été peint à la fin du XIXe siècle. La famille Hez est arrêtée et le tableau spolié. Il était destiné au projet du Musée de Linz mais la fin de la guerre le met en échec. Il est retrouvé par Rose Valland, historienne et résistante, et rappatrié au Louvre où il est conservé jusqu en 2012, date à laquelle il fut remis à son propriétaire.', 'Chloé Pochon', '2016', 'Spoliation', 'paysage', '<img src="/static/img/tableau_communion.jpg"/>', 'tableau_communion.jpg'); 
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Bertrand Herz", "Bertrand Herz a 14 ans lorsqu il est arrêté et déporté avec son père au camp de Buchenwald. Survivant à la déportation et devenu orphelin, il est rappatrié au Lutétia. C est au cours d une recherche internet qu il retrouve la trace du tableau familial, spolié 75 ans auparavant. Il lui est remis en 2012 par la conservatrice du musée du Louvre.', 'Chloé Pochon', '2016', 'Spoliation', 'paysage', '<img src="/static/img/bertrandherz.jpg"/>', 'bertrandherz.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES ('Règle à calculs de Raphaël Esrail - face', 'Raphël Esrail est étudiant en ingénirie lorsqu il est déporté au camp d Auschwitz. Sauvé par les Américains lors d une "marche de la mort" et est logé dans une ancienne école des jeunesses hitlériennes. Alors que certains brûlent ces règles pour se réchauffer, lui décide d en rapporter une.', 'Chloé Pochon', '2016', 'Shoah', 'paysage', '<img src="/static/img/regleface.jpg"/>', 'regleface.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES('Règle à calculs de Raphaël Esrail - revers', 'Raphël Esrail est étudiant en ingénirie lorsqu il est déporté au camp d Auschwitz. Sauvé par les Américains lors d une "marche de la mort" et est logé dans une ancienne école des jeunesses hitlériennes. Alors que certains brûlent ces règles pour se réchauffer, lui décide d en rapporter une.', 'Chloé Pochon', '2016', 'Shoah', 'paysage', '<img src="/static/img/reglerevers.jpg"/>', 'reglerevers.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES( 'Boite de cigarettes Churchmans - 1', 'Ces boîtes étaient données à chaque soldat britannique avant leur embarcation pour l opération Overlord. Celle-ci n a jamais été ouverte.', 'Chloé Pochon', '2016', 'Seconde guerre mondiale', 'paysage', '<img src="/static/img/churchmandebout.jpg"/>', 'churchmandebout.jpg');
INSERT or IGNORE INTO photo (photo_titre, photo_description, photo_auteur, photo_date, photo_tag, photo_orientation, photo_chemin, photo_fichier) VALUES( 'Boite de cigarettes Churchmans - 2', 'Ces boîtes étaient données à chaque soldat britannique avant leur embarcation pour l opération Overlord. Celle-ci n a jamais été ouverte.', 'Chloé Pochon', '2016', 'Seconde guerre mondiale', 'paysage', '<img src="/static/img/churchmancouchee.jpg"/>', 'churchmancouchee.jpg');
INSERT INTO user (user_id, user_nom, user_login, user_email, user_password) VALUES (1, 'Administrator', 'admin', 'admin@histoireobjet.com', 'admin');
