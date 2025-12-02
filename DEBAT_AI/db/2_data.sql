-- Insertion des utilisateurs
INSERT INTO users (username) VALUES ('Alice') RETURNING id;

INSERT INTO users (username) VALUES ('Bob') RETURNING id;

-- Insertion d'un débat
INSERT INTO
    debates (topic)
VALUES (
        'L''IA va-t-elle remplacer les humains ?'
    )
RETURNING
    id;

-- Insertion des messages pour le débat
INSERT INTO
    messages (content, user_id, debate_id)
VALUES (
        'Je pense que l''IA est un outil puissant qui augmentera nos capacités, plutôt que de nous remplacer.',
        (
            SELECT id
            FROM users
            WHERE
                username = 'Alice'
        ),
        (
            SELECT id
            FROM debates
            WHERE
                topic = 'L''IA va-t-elle remplacer les humains ?'
        )
    ),
    (
        'Cependant, l''automatisation avancée pourrait bien rendre certains emplois obsolètes, créant des défis sociaux majeurs.',
        (
            SELECT id
            FROM users
            WHERE
                username = 'Bob'
        ),
        (
            SELECT id
            FROM debates
            WHERE
                topic = 'L''IA va-t-elle remplacer les humains ?'
        )
    ),
    (
        'Tout dépend de la façon dont nous gérons cette transition et investissons dans la formation.',
        (
            SELECT id
            FROM users
            WHERE
                username = 'Alice'
        ),
        (
            SELECT id
            FROM debates
            WHERE
                topic = 'L''IA va-t-elle remplacer les humains ?'
        )
    );