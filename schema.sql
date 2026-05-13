---------------------------------------
--  Dropping existing Database Tables  --
---------------------------------------
DROP TYPE IF EXISTS transaction_type_enum CASCADE;
DROP TABLE IF EXISTS family CASCADE;
DROP TABLE IF EXISTS user CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;


-- -- Drop sequences if they exist
DROP SEQUENCE IF EXISTS family_seq;
DROP SEQUENCE IF EXISTS user_seq;
DROP SEQUENCE IF EXISTS category_seq;
DROP SEQUENCE IF EXISTS transactions_seq;

---------------------------------------
--  Creation of Tables  --
---------------------------------------

-- Create transaction type enum
CREATE TYPE transaction_type_enum AS ENUM (
    'INCOME',
    'EXPENSE'
    );

CREATE TABLE family (
    id SERIAL PRIMARY KEY,
    family_name VARCHAR(255) NOT NULL                   
);

COMMENT ON TABLE family IS 'Table to store families';
COMMENT ON COLUMN family.family_name IS 'Name of the family';

CREATE TABLE member
(
    id                   SERIAL PRIMARY KEY,
    family_id            INTEGER,
    first_name           VARCHAR(255) NOT NULL,
    last_name            VARCHAR(255) NOT NULL,
    email                VARCHAR(255) NOT NULL UNIQUE,
    password             VARCHAR(255),
    CONSTRAINT fk_family
        FOREIGN KEY (family_id)
            REFERENCES family(id)
            ON DELETE CASCADE
);

COMMENT ON TABLE member IS 'Table to store personal and contact details of the family member.';
COMMENT ON COLUMN member.family_id IS 'Foreign key reference to the family';
COMMENT ON COLUMN member.first_name IS 'First name of the person';
COMMENT ON COLUMN member.last_name IS 'Last name of the person';
COMMENT ON COLUMN member.email IS 'Email address of the person';
COMMENT ON COLUMN member.password IS 'Password of the person';


CREATE TABLE category
(
    id                  SERIAL PRIMARY KEY,
    category_name       VARCHAR(255) NOT NULL,
    member_id             INTEGER NOT NULL,
    CONSTRAINT fk_member
        FOREIGN KEY (member_id)
            REFERENCES member (id)
            ON DELETE CASCADE
);

COMMENT ON TABLE category IS 'Table to categorize the type of income/expense';
COMMENT ON COLUMN category.category_name IS 'Name of the category';

CREATE TABLE transactions
(
    id                  SERIAL PRIMARY KEY,
    transaction_name    VARCHAR(255)NOT NULL,
    transaction_type    transaction_type_enum NOT NULL,
    amount              DOUBLE NOT NULL,
    date                Date NOT NULL,
    category_id         INTEGER NOT NULL,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
            REFERENCES category (id)
            ON DELETE CASCADE
);

COMMENT ON TABLE transactions IS 'Table to store detail transactions';
COMMENT ON COLUMN transactions.transaction_name IS 'Name of the transaction';
COMMENT ON COLUMN transactions.transaction_type IS 'The transaction type is either income or expense';
COMMENT ON COLUMN transactions.amount IS 'The amount of the transaction';
