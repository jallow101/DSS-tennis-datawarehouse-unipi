-- Country Dimension
CREATE TABLE country (
    country_id VARCHAR(9) PRIMARY KEY,
    country_name VARCHAR(100),
    continent VARCHAR(50)
);

-- Player Dimension
CREATE TABLE player (
    player_id VARCHAR(20) PRIMARY KEY,
    player_name VARCHAR(100),
    hand CHAR(1),
    age INT,
    height INT,
    country_id VARCHAR(9),
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
    tourney_id VARCHAR(20) PRIMARY KEY,
    tourney_range VARCHAR(40),
    tourney_name VARCHAR(100),
    surface VARCHAR(20),
    draw_size INT,
    tourney_level CHAR(1),
    tourney_date_id INT,
    FOREIGN KEY (tourney_date_id) REFERENCES date(date_id)
);

-- Match Fact Table
CREATE TABLE match_fact (
    match_id VARCHAR(50) PRIMARY KEY,
    winner_id VARCHAR(20),
    loser_id VARCHAR(20),
    tourney_id VARCHAR(20),
    no_spectators INT,
    avg_ticket FLOAT,
    match_expense FLOAT,
    FOREIGN KEY (winner_id) REFERENCES player(player_id),
    FOREIGN KEY (loser_id) REFERENCES player(player_id),
    FOREIGN KEY (tourney_id) REFERENCES tourney(tourney_id)
);
