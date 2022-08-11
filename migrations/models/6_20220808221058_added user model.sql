-- upgrade --
ALTER TABLE "contact" ADD "user_id" INT;
CREATE TABLE IF NOT EXISTS "user" (
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(1024) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_verified" BOOL NOT NULL  DEFAULT False,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" VARCHAR(2) NOT NULL  DEFAULT 'A',
    "date_joined" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");;
ALTER TABLE "contact" ADD CONSTRAINT "fk_contact_user_15dde9eb" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "contact" DROP CONSTRAINT "fk_contact_user_15dde9eb";
ALTER TABLE "contact" DROP COLUMN "user_id";
DROP TABLE IF EXISTS "user";
