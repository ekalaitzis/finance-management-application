---------------------------------------
--  Dropping existing Database Tables  --
---------------------------------------
DROP TYPE IF EXISTS transactions;
DROP TABLE IF EXISTS family;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS transactions;

---------------------------------------
--  Creation of Tables  --
---------------------------------------

-- Create transaction type enum

CREATE TABLE family (
    id INTEGER PRIMARY KEY,
    family_name TEXT NOT NULL                   
);

CREATE TABLE member
(
    id                   INTEGER PRIMARY KEY,
    family_id            INTEGER NOT NULL,
    first_name           TEXT NOT NULL,
    last_name            TEXT NOT NULL,
    email                TEXT NOT NULL UNIQUE,
    password             TEXT NOT NULL,
        FOREIGN KEY (family_id)
            REFERENCES family(id)
            ON DELETE CASCADE
);


CREATE TABLE category
(
    id                  INTEGER PRIMARY KEY,
    category_name       TEXT UNIQUE NOT NULL,
    member_id           INTEGER NOT NULL,
    CONSTRAINT fk_member
        FOREIGN KEY (member_id)
            REFERENCES member (id)
            ON DELETE CASCADE
);

CREATE TABLE transactions
(
    id                  INTEGER PRIMARY KEY,
    transaction_name    TEXT NOT NULL,
    transaction_type    TEXT NOT NULL CHECK(transaction_type IN ('INCOME', 'EXPENSE')),
    amount              REAL NOT NULL CHECK(amount >= 0),
    date                TEXT NOT NULL,
    category_id         INTEGER NOT NULL,
        FOREIGN KEY (category_id)
            REFERENCES category (id)
            ON DELETE CASCADE
);
