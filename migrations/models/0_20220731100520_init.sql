-- upgrade --
CREATE TABLE IF NOT EXISTS "contact" (
    "label" VARCHAR(15) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(60),
    "middle_name" VARCHAR(60),
    "last_name" VARCHAR(60),
    "company" VARCHAR(120),
    "address" TEXT,
    "note" TEXT,
    "website" VARCHAR(120),
    "spouse" VARCHAR(120) NOT NULL,
    "nickname" VARCHAR(60) NOT NULL,
    "is_favorite" BOOL NOT NULL  DEFAULT False,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "status" VARCHAR(2) NOT NULL
);
COMMENT ON TABLE "contact" IS 'contact model for a person contact';
CREATE TABLE IF NOT EXISTS "contacttag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "tag" VARCHAR(15) NOT NULL
);
COMMENT ON TABLE "contacttag" IS 'model for tags, for contacts, as a way of grouping contacts';
CREATE TABLE IF NOT EXISTS "email" (
    "label" VARCHAR(15) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "email_address" VARCHAR(120) NOT NULL
);
COMMENT ON TABLE "email" IS 'model for email addresses associated with a contact';
CREATE TABLE IF NOT EXISTS "phone" (
    "label" VARCHAR(15) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "phone_number" VARCHAR(15) NOT NULL
);
COMMENT ON TABLE "phone" IS 'model for phone numbers associated with a contact';
CREATE TABLE IF NOT EXISTS "significantdate" (
    "label" VARCHAR(15) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "date" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "significantdate" IS 'birthday, anniversary, e.t.c, associated with a contact';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "fullname" VARCHAR(120),
    "username" VARCHAR(30) NOT NULL,
    "email" VARCHAR(120) NOT NULL,
    "password" VARCHAR(90) NOT NULL
);
COMMENT ON TABLE "user" IS '(make-shift) User model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
