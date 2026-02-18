-- =============================================
-- Fake data for gnews_api (Django models)
-- Run AFTER: py manage.py migrate
-- =============================================

-- 1. Sources
INSERT INTO sources (id, name, type, url, fetch_interval, is_active, created_at, updated_at) VALUES
(1, 'IGN', 'rss', 'https://www.ign.com/rss/articles', 15, 1, NOW(), NOW()),
(2, 'Kotaku', 'rss', 'https://kotaku.com/rss', 30, 1, NOW(), NOW()),
(3, 'GameSpot', 'api', 'https://api.gamespot.com/articles/', 20, 1, NOW(), NOW()),
(4, 'PC Gamer', 'scraper', 'https://www.pcgamer.com/news/', 45, 1, NOW(), NOW()),
(5, 'Eurogamer', 'rss', 'https://www.eurogamer.net/feed', 30, 0, NOW(), NOW());

-- 2. Categories
INSERT INTO categories (id, name, slug, parent_id, created_at, updated_at) VALUES
(1, 'Actualites', 'actualites', NULL, NOW(), NOW()),
(2, 'Reviews', 'reviews', NULL, NOW(), NOW()),
(3, 'Guides', 'guides', NULL, NOW(), NOW()),
(4, 'Esports', 'esports', NULL, NOW(), NOW()),
(5, 'Hardware', 'hardware', NULL, NOW(), NOW()),
(6, 'PS5', 'ps5', 1, NOW(), NOW()),
(7, 'Xbox', 'xbox', 1, NOW(), NOW()),
(8, 'PC', 'pc', 1, NOW(), NOW()),
(9, 'Nintendo', 'nintendo', 1, NOW(), NOW()),
(10, 'Indie', 'indie', 2, NOW(), NOW());

-- 3. Tags
INSERT INTO tags (id, name, slug, type, created_at, updated_at) VALUES
(1, 'GTA 6', 'gta-6', 'game', NOW(), NOW()),
(2, 'Elden Ring', 'elden-ring', 'game', NOW(), NOW()),
(3, 'Zelda', 'zelda', 'game', NOW(), NOW()),
(4, 'PlayStation 5', 'playstation-5', 'platform', NOW(), NOW()),
(5, 'Xbox Series X', 'xbox-series-x', 'platform', NOW(), NOW()),
(6, 'Nintendo Switch 2', 'nintendo-switch-2', 'platform', NOW(), NOW()),
(7, 'PC', 'pc', 'platform', NOW(), NOW()),
(8, 'RPG', 'rpg', 'genre', NOW(), NOW()),
(9, 'FPS', 'fps', 'genre', NOW(), NOW()),
(10, 'Action', 'action', 'genre', NOW(), NOW()),
(11, 'Open World', 'open-world', 'genre', NOW(), NOW()),
(12, 'Mise a jour', 'mise-a-jour', 'general', NOW(), NOW()),
(13, 'Sortie', 'sortie', 'general', NOW(), NOW()),
(14, 'Rumeur', 'rumeur', 'general', NOW(), NOW()),
(15, 'Trailer', 'trailer', 'general', NOW(), NOW());

-- 4. Media
INSERT INTO media (id, url, alt_text, caption, credit, created_at, updated_at) VALUES
(1, 'https://images.example.com/gta6-trailer.jpg', 'GTA 6 screenshot officiel', 'Vice City dans GTA 6', 'Rockstar Games', NOW(), NOW()),
(2, 'https://images.example.com/elden-ring-dlc.jpg', 'Elden Ring DLC artwork', 'Nouveau DLC Shadow of the Erdtree', 'FromSoftware', NOW(), NOW()),
(3, 'https://images.example.com/switch2-reveal.jpg', 'Nintendo Switch 2', 'La nouvelle console Nintendo', 'Nintendo', NOW(), NOW()),
(4, 'https://images.example.com/ps5-pro.jpg', 'PS5 Pro design', 'Le nouveau design de la PS5 Pro', 'Sony', NOW(), NOW()),
(5, 'https://images.example.com/starfield-update.jpg', 'Starfield mise a jour', 'Nouvelle mise a jour de Starfield', 'Bethesda', NOW(), NOW()),
(6, 'https://images.example.com/zelda-totk.jpg', 'Zelda Tears of the Kingdom', 'Screenshot du jeu', 'Nintendo', NOW(), NOW()),
(7, 'https://images.example.com/cyberpunk-sequel.jpg', 'Cyberpunk 2 annonce', 'Premier artwork du sequel', 'CD Projekt Red', NOW(), NOW()),
(8, 'https://images.example.com/esports-worlds.jpg', 'League of Legends Worlds', 'Finale des Worlds 2026', 'Riot Games', NOW(), NOW());

-- 5. Raw News
INSERT INTO raw_news (id, source_id, title, url, content, status, raw_data, created_at, updated_at) VALUES
(1, 1, 'GTA 6 Release Date Confirmed for Fall 2025', 'https://www.ign.com/articles/gta-6-release-date', 'Rockstar Games has officially confirmed that Grand Theft Auto VI will launch in Fall 2025...', 'traite', '{"author": "John Smith", "published": "2025-12-01"}', NOW(), NOW()),
(2, 2, 'Elden Ring Nightreign impressions', 'https://kotaku.com/elden-ring-nightreign', 'The new standalone Elden Ring multiplayer experience is shaping up nicely...', 'traite', '{"author": "Jane Doe", "published": "2025-11-28"}', NOW(), NOW()),
(3, 3, 'Nintendo Switch 2 Specs Leaked', 'https://www.gamespot.com/articles/switch-2-specs', 'According to reliable sources, the Nintendo Switch 2 will feature an NVIDIA T239 processor...', 'traite', '{"author": "Mike R.", "published": "2025-12-05"}', NOW(), NOW()),
(4, 1, 'PS5 Pro Sales Exceed Expectations', 'https://www.ign.com/articles/ps5-pro-sales', 'Sony reports that PS5 Pro has sold over 5 million units in its first quarter...', 'nouveau', '{"author": "Sarah K.", "published": "2025-12-10"}', NOW(), NOW()),
(5, 4, 'Best PC Gaming Deals This Week', 'https://www.pcgamer.com/deals-of-the-week', 'Here are the best deals on PC games and hardware this week...', 'ignore', '{"author": "Tom B.", "published": "2025-12-12"}', NOW(), NOW()),
(6, 2, 'Cyberpunk 2 Officially Announced', 'https://kotaku.com/cyberpunk-2-announced', 'CD Projekt Red has officially announced the sequel to Cyberpunk 2077...', 'traite', '{"author": "Alex P.", "published": "2025-12-15"}', NOW(), NOW()),
(7, 3, 'Starfield Major Update Adds Vehicles', 'https://www.gamespot.com/articles/starfield-vehicles', 'Bethesda releases massive update for Starfield adding ground vehicles...', 'nouveau', '{"author": "Lisa M.", "published": "2025-12-18"}', NOW(), NOW()),
(8, 5, 'League of Legends Worlds 2026 Location Revealed', 'https://www.eurogamer.net/lol-worlds-2026', 'Riot Games announces that Worlds 2026 will take place in Paris, France...', 'traite', '{"author": "Chris L.", "published": "2025-12-20"}', NOW(), NOW());

-- 6. Articles
INSERT INTO articles (id, source_id, raw_news_id, category_id, title, slug, content, meta_title, meta_description, featured_image, status, is_featured, is_breaking, view_count, validation_notes, published_at, created_at, updated_at) VALUES
(1, 1, 1, 1,
 'GTA 6 : Rockstar confirme la date de sortie pour automne 2025',
 'gta-6-date-sortie-automne-2025',
 'Rockstar Games a officiellement confirme que Grand Theft Auto VI sortira a l''automne 2025. Le jeu se deroulera a Vice City et promet une experience open-world revolutionnaire. Les fans attendaient cette annonce depuis des annees, et les premieres images montrent un niveau de detail impressionnant.\n\nLe jeu sera disponible sur PS5 et Xbox Series X|S au lancement, avec une version PC prevue pour 2026.',
 'GTA 6 Date de Sortie - Automne 2025 Confirme',
 'Rockstar Games confirme officiellement la date de sortie de GTA 6 pour automne 2025 sur PS5 et Xbox.',
 'https://images.example.com/gta6-trailer.jpg',
 'publie', 1, 1, 45230, NULL,
 '2025-12-01 14:00:00', NOW(), NOW()),

(2, 2, 2, 2,
 'Elden Ring Nightreign : nos impressions apres 10 heures de jeu',
 'elden-ring-nightreign-impressions',
 'Nous avons pu tester Elden Ring Nightreign pendant plus de 10 heures et le resultat est tres prometteur. Ce standalone multijoueur reprend les bases de combat d''Elden Ring tout en ajoutant une dimension cooperative inedite.\n\nLe systeme de classes a ete repense et chaque session offre une experience unique grace a la generation procedurale des donjons.',
 'Test Elden Ring Nightreign - Nos Premieres Impressions',
 'Decouvrez nos impressions sur Elden Ring Nightreign apres 10 heures de jeu. Un standalone multijoueur prometteur.',
 'https://images.example.com/elden-ring-dlc.jpg',
 'publie', 1, 0, 32100, NULL,
 '2025-11-28 10:30:00', NOW(), NOW()),

(3, 3, 3, 1,
 'Nintendo Switch 2 : les specifications techniques fuitent en ligne',
 'nintendo-switch-2-specifications-fuite',
 'Les specifications techniques de la Nintendo Switch 2 auraient fuite en ligne. Selon des sources fiables, la console embarquerait un processeur NVIDIA T239 avec 12 Go de RAM.\n\nLa console serait retrocompatible avec les jeux Switch originaux et supporterait le ray tracing. Nintendo n''a pas encore commente ces fuites.',
 'Nintendo Switch 2 Specs - Fuite des Caracteristiques',
 'Les specifications de la Nintendo Switch 2 fuitent : processeur NVIDIA T239, 12 Go RAM et ray tracing.',
 'https://images.example.com/switch2-reveal.jpg',
 'publie', 0, 1, 28750, NULL,
 '2025-12-05 16:00:00', NOW(), NOW()),

(4, 1, 4, 1,
 'PS5 Pro : les ventes depassent les attentes de Sony',
 'ps5-pro-ventes-depassent-attentes',
 'Sony annonce que la PS5 Pro a depasse les 5 millions d''unites vendues au cours de son premier trimestre. Ce chiffre depasse largement les previsions initiales de l''entreprise.\n\nLa console premium a beneficie d''un catalogue de jeux optimises impressionnant au lancement.',
 'PS5 Pro Ventes - 5 Millions Premier Trimestre',
 'La PS5 Pro depasse les 5 millions de ventes en un trimestre, depassant les attentes de Sony.',
 'https://images.example.com/ps5-pro.jpg',
 'en_revision', 0, 0, 890, 'Verifier les chiffres de ventes aupres de sources officielles.',
 NULL, NOW(), NOW()),

(5, 2, 6, 1,
 'Cyberpunk 2 officiellement annonce par CD Projekt Red',
 'cyberpunk-2-annonce-officiel',
 'CD Projekt Red a officiellement annonce le successeur de Cyberpunk 2077. Le jeu, provisoirement appele Project Orion, sera developpe par le nouveau studio americain de CDPR a Boston.\n\nLe jeu utilisera l''Unreal Engine 5 et promet de repousser les limites du genre RPG en monde ouvert. Aucune date de sortie n''a ete communiquee.',
 'Cyberpunk 2 Annonce - CD Projekt Red',
 'CD Projekt Red annonce officiellement Cyberpunk 2, le successeur de Cyberpunk 2077, developpe sur Unreal Engine 5.',
 'https://images.example.com/cyberpunk-sequel.jpg',
 'brouillon_ia', 0, 0, 0, NULL,
 NULL, NOW(), NOW()),

(6, 3, 7, 1,
 'Starfield : une mise a jour majeure ajoute enfin les vehicules',
 'starfield-mise-a-jour-vehicules',
 'Bethesda vient de deployer une mise a jour massive pour Starfield qui ajoute enfin les vehicules terrestres tant attendus par la communaute.\n\nLes joueurs peuvent desormais explorer les planetes a bord de rovers personnalisables. La mise a jour inclut egalement de nouvelles quetes et ameliorations de performances.',
 'Starfield Update Vehicules - Mise a Jour Majeure',
 'Starfield recoit une mise a jour majeure ajoutant des vehicules terrestres, de nouvelles quetes et des optimisations.',
 'https://images.example.com/starfield-update.jpg',
 'publie', 0, 0, 15400, NULL,
 '2025-12-18 09:00:00', NOW(), NOW()),

(7, 5, 8, 4,
 'League of Legends Worlds 2026 : la finale se tiendra a Paris',
 'lol-worlds-2026-paris',
 'Riot Games a annonce que la finale des Worlds 2026 de League of Legends se tiendra a Paris, au Stade de France. C''est la premiere fois que l''evenement revient en France depuis 2019.\n\nLes billets seront mis en vente au printemps 2026. L''evenement est prevu pour novembre 2026.',
 'LoL Worlds 2026 Paris - Stade de France',
 'La finale des Worlds 2026 de League of Legends aura lieu au Stade de France a Paris.',
 'https://images.example.com/esports-worlds.jpg',
 'publie', 1, 0, 21300, NULL,
 '2025-12-20 18:00:00', NOW(), NOW()),

(8, NULL, NULL, 3,
 'Guide : les meilleurs builds pour Elden Ring Nightreign',
 'guide-meilleurs-builds-elden-ring-nightreign',
 'Decouvrez notre selection des meilleurs builds pour bien debuter dans Elden Ring Nightreign. Que vous preferiez le corps a corps, la magie ou un style hybride, nous avons le build qu''il vous faut.\n\n1. Le Chevalier Sanglant (Force/Endurance)\n2. Le Mage des Etoiles (Intelligence/Esprit)\n3. L''Assassin Nocturne (Dexterite/Arcane)',
 'Meilleurs Builds Elden Ring Nightreign',
 'Guide complet des meilleurs builds pour Elden Ring Nightreign : guerrier, mage et assassin.',
 'https://images.example.com/elden-ring-dlc.jpg',
 'publie', 0, 0, 8900, NULL,
 '2025-12-22 12:00:00', NOW(), NOW());

-- 7. Article Tags (many-to-many)
INSERT INTO article_tags (article_id, tag_id, created_at) VALUES
(1, 1, NOW()),   -- GTA 6 -> GTA 6
(1, 4, NOW()),   -- GTA 6 -> PlayStation 5
(1, 5, NOW()),   -- GTA 6 -> Xbox Series X
(1, 11, NOW()),  -- GTA 6 -> Open World
(1, 10, NOW()),  -- GTA 6 -> Action
(1, 13, NOW()),  -- GTA 6 -> Sortie
(2, 2, NOW()),   -- Elden Ring -> Elden Ring
(2, 8, NOW()),   -- Elden Ring -> RPG
(2, 10, NOW()),  -- Elden Ring -> Action
(3, 6, NOW()),   -- Switch 2 -> Nintendo Switch 2
(3, 14, NOW()),  -- Switch 2 -> Rumeur
(4, 4, NOW()),   -- PS5 Pro -> PlayStation 5
(5, 7, NOW()),   -- Cyberpunk 2 -> PC
(5, 8, NOW()),   -- Cyberpunk 2 -> RPG
(5, 11, NOW()),  -- Cyberpunk 2 -> Open World
(6, 7, NOW()),   -- Starfield -> PC
(6, 5, NOW()),   -- Starfield -> Xbox Series X
(6, 11, NOW()),  -- Starfield -> Open World
(6, 12, NOW()),  -- Starfield -> Mise a jour
(7, 15, NOW()),  -- LoL Worlds -> Trailer (event)
(8, 2, NOW()),   -- Guide Elden Ring -> Elden Ring
(8, 8, NOW()),   -- Guide Elden Ring -> RPG
(8, 10, NOW());  -- Guide Elden Ring -> Action

-- 8. Article Media (many-to-many)
INSERT INTO article_media (article_id, media_id, order_position, created_at) VALUES
(1, 1, 0, NOW()),
(2, 2, 0, NOW()),
(3, 3, 0, NOW()),
(4, 4, 0, NOW()),
(5, 7, 0, NOW()),
(6, 5, 0, NOW()),
(7, 8, 0, NOW()),
(8, 2, 0, NOW());
