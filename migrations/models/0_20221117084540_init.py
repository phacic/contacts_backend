from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "contacttag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "tag" VARCHAR(50) NOT NULL
);
COMMENT ON TABLE "contacttag" IS 'model for tags, for contacts, as a way of grouping contacts';
CREATE TABLE IF NOT EXISTS "user" (
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(1024) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_verified" BOOL NOT NULL  DEFAULT False,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "full_name" VARCHAR(150),
    "status" VARCHAR(2) NOT NULL  DEFAULT 'A',
    "date_joined" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
CREATE TABLE IF NOT EXISTS "contact" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(60),
    "middle_name" VARCHAR(60),
    "last_name" VARCHAR(60),
    "company" VARCHAR(120),
    "note" TEXT,
    "website" VARCHAR(120),
    "spouse" VARCHAR(120),
    "nickname" VARCHAR(60),
    "is_favorite" BOOL NOT NULL  DEFAULT False,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "status" VARCHAR(2) NOT NULL  DEFAULT 'A',
    "user_id" INT REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "contact" IS 'contact model for a person contact';
CREATE TABLE IF NOT EXISTS "address" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "location" TEXT NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "address" IS 'address associated with Contact';
CREATE TABLE IF NOT EXISTS "email" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "email_address" VARCHAR(120) NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "email" IS 'model for email addresses associated with a contact';
CREATE TABLE IF NOT EXISTS "phone" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "phone_number" VARCHAR(50) NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "phone" IS 'model for phone numbers associated with a contact';
CREATE TABLE IF NOT EXISTS "significantdate" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "date" TIMESTAMPTZ NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "significantdate" IS 'birthday, anniversary, e.t.c, associated with a contact';
CREATE TABLE IF NOT EXISTS "socialmedia" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "url" VARCHAR(255) NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "socialmedia" IS 'social media links for the contact';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "contact_contacttag" (
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE,
    "contacttag_id" INT NOT NULL REFERENCES "contacttag" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
