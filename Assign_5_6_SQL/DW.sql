-- Country Dimension
CREATE TABLE country (
    country_id int PRIMARY KEY,
    country_name VARCHAR(100),
    continent VARCHAR(50)
);

-- Player Dimension
CREATE TABLE player (
    player_id int PRIMARY KEY,
    player_name VARCHAR(100),
    hand CHAR(1),
    age INT,
    height INT,
    country_id int,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

-- Date Dimension
CREATE TABLE date (
    date_id INT PRIMARY KEY,
    date DATE,
    day INT,
    day_of_week VARCHAR(20),
    is_weekend BIT,
    week INT,
    month INT,
    quarter INT,
    year INT
);

-- Tournament Dimension
CREATE TABLE tourney (
    tourney_id int PRIMARY KEY,
    tourney_range VARCHAR(40),
    tourney_name VARCHAR(100),
    surface VARCHAR(20),
    draw_size INT,
    tourney_level VARCHAR(20),
    tourney_date_id INT,
    FOREIGN KEY (tourney_date_id) REFERENCES date(date_id)
);

-- Match Fact Table
CREATE TABLE match_fact (
    match_id int PRIMARY KEY,
    winner_id int,
    loser_id int,
    tourney_id int,
    no_spectators BIGINT,
    avg_ticket FLOAT,
    match_expense FLOAT,
    winner_rank_points INT,
    loser_rank_points INT,
    winner_rank INT,
    loser_rank INT,
    round VARCHAR(10),
    score VARCHAR(50),
    best_of TINYINT
    FOREIGN KEY (winner_id) REFERENCES player(player_id),
    FOREIGN KEY (loser_id) REFERENCES player(player_id),
    FOREIGN KEY (tourney_id) REFERENCES tourney(tourney_id)
);
