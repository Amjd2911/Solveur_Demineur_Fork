-- Insertion des utilisateurs
INSERT INTO users (username) VALUES ('Alice');
INSERT INTO users (username) VALUES ('Bob');

-- Insertion d'un débat
INSERT INTO debates (topic) VALUES ('L''IA va-t-elle remplacer les humains ?');

-- Insertion des messages AVEC la logique (Qui attaque qui)
INSERT INTO messages 
    (content, user_id, debate_id, arg_type, relation_type, target_id)
VALUES 
    (
        -- Message 1 (Alice) : Le début du débat (Racine)
        'Je pense que l''IA est un outil puissant qui augmentera nos capacités, plutôt que de nous remplacer.',
        (SELECT id FROM users WHERE username = 'Alice'),
        (SELECT id FROM debates WHERE topic = 'L''IA va-t-elle remplacer les humains ?'),
        'claim',   -- C'est une affirmation
        'none',    -- Ne répond à personne
        NULL       -- Pas de cible
    ),
    (
        -- Message 2 (Bob) : Il attaque Alice (Message 1)
        'Cependant, l''automatisation avancée pourrait bien rendre certains emplois obsolètes.',
        (SELECT id FROM users WHERE username = 'Bob'),
        (SELECT id FROM debates WHERE topic = 'L''IA va-t-elle remplacer les humains ?'),
        'claim',   -- C'est une affirmation
        'attack',  -- IL ATTAQUE
        1          -- Il vise le message ID 1
    ),
    (
        -- Message 3 (Alice) : Elle se défend contre Bob (Message 2)
        'Tout dépend de la façon dont nous gérons cette transition et investissons dans la formation.',
        (SELECT id FROM users WHERE username = 'Alice'),
        (SELECT id FROM debates WHERE topic = 'L''IA va-t-elle remplacer les humains ?'),
        'premise', -- C'est un argument de support
        'attack',  -- Elle attaque l'argument pessimiste de Bob
        2          -- Elle vise le message ID 2
    );