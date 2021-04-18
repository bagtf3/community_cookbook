DROP TABLE IF EXISTS recipes;

CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_name TEXT NOT NULL,
    image_url TEXT
);

INSERT INTO recipes (id, username, recipe_name, image_url)
VALUES
    (1, "admin", "Chocolate Cake", "/static/images/chocolate-cake-3.jpg"),
    (2, "admin", "Roasted Carrots", "/static/images/carrots.jpg"),
    (3, "crazy4cabbage", "Cabbage Rolls", "/static/images/Cabbage_Rolls.jpg");

DROP TABLE IF EXISTS ingredients;

CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER,
    recipe_id INTEGER NOT NULL,
    recipe_name TEXT NOT NULL,
    ingredient TEXT NOT NULL,
    amount TEXT NOT NULL,
    PRIMARY KEY (id, recipe_name)
);

INSERT INTO ingredients (recipe_name, recipe_id, ingredient, amount)
VALUES
    ("Chocolate Cake", 1, "flour", "1 cup"),
    ("Chocolate Cake", 1, "sugar", "1/4 cup"),
    ("Chocolate Cake", 1, "eggs", "2"),
    ("Chocolate Cake", 1, "Chocolate Powder", "1/2 cup"),
    ("Chocolate Cake", 1, "butter", "1/2 stick"),
    ("Roasted Carrots", 2, "carrots", "1/2 pound"),
    ("Roasted Carrots", 2, "butter", "2 tsp"),
    ("Roasted Carrots", 2, "garlic", "1 pinch"),
    ("Roasted Carrots", 2, "salt", "1 pinch"),
    ("Cabbage Rolls", 3, "cabbage", "1 pound"),
    ("Cabbage Rolls", 3, "meat (your choice)", "1/2 pound"),
    ("Cabbage Rolls", 3, "rice", "2 cups"),
    ("Cabbage Rolls", 3, "seasoning", "to flavor");


DROP TABLE IF EXISTS instructions;

CREATE TABLE IF NOT EXISTS instructions (
    id INTEGER,
    step_number INTEGER,
    recipe_name TEXT NOT NULL,
    recipe_id INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    PRIMARY KEY (id, recipe_name)
);

INSERT INTO instructions (step_number, recipe_name, recipe_id, instruction)
VALUES
    (1, "Chocolate Cake", 1, "Mix dry ingredients in a small bowl"),
    (2, "Chocolate Cake", 1, "Melt butter and add wet ingredients."),
    (3, "Chocolate Cake", 1, "Stir together"),
    (4, "Chocolate Cake", 1, "bake 350 F for 35 minutes."),
    (1, "Roasted Carrots", 2, "Peel carrots and coat in melted butter, garlic and salt"),
    (2, "Roasted Carrots", 2, "Roast in over at 400 F for 20 minutes."),
    (1, "Cabbage Rolls", 3, "Steam rice and cabbage leaves until soft."),
    (2, "Cabbage Rolls", 3, "Cook the meat with added seasoning"),
    (3, "Cabbage Rolls", 3, "Wrap the meat tightly in the roll"),
    (4, "Cabbage Rolls", 3, "Sear in a hot pan until brown."),
    (5, "Cabbage Rolls", 3, "Serve on bed of rice.");


DROP TABLE IF EXISTS reviews;

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER,
    recipe_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    reviewer TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, recipe_id)
);

INSERT INTO reviews (recipe_id, review_text, rating, reviewer)
VALUES
    (1, "the best chocolate cake I have EVER had!", 5.0, "cakelover55"),
    (1, "pretty good but my aunt's is better", 3.5, "MaryJonesFamily"),
    (2, "These carrots are so soft, but would like more flavor", 4.0, "anonymous user"),
    (2, "carrots. gross.", 0.5, "picky_eater_for_life"),
    (3, "This Tastes Just like Home!", 5.0, "SandyCaruthers"),
    (3, "These rolls are OK but need more flavor", 3.0, "CaptainCook445");
