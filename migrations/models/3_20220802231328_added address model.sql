-- upgrade --
ALTER TABLE "contacttag" DROP CONSTRAINT "fk_contactt_contact_eedbe134";
CREATE TABLE IF NOT EXISTS "address" (
    "label" VARCHAR(15) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "location" TEXT NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "address" IS 'address associated with Contact';;
ALTER TABLE "contacttag" DROP COLUMN "contact_id";
CREATE TABLE "contact_contacttag" ("contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE,"contacttag_id" INT NOT NULL REFERENCES "contacttag" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "contact_contacttag";
ALTER TABLE "contacttag" ADD "contact_id" INT NOT NULL;
DROP TABLE IF EXISTS "address";
ALTER TABLE "contacttag" ADD CONSTRAINT "fk_contactt_contact_eedbe134" FOREIGN KEY ("contact_id") REFERENCES "contact" ("id") ON DELETE CASCADE;
