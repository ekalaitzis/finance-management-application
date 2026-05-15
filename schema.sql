
CREATE TABLE member
(
    id                   INTEGER PRIMARY KEY,
    first_name           TEXT NOT NULL,
    last_name            TEXT NOT NULL,
    username             TEXT NOT NULL UNIQUE,
    password             TEXT NOT NULL
);


CREATE TABLE category
(
    id                  INTEGER PRIMARY KEY,
    category_name       TEXT NOT NULL,
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
