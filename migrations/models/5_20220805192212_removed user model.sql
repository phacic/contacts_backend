-- upgrade --
ALTER TABLE "contact" DROP CONSTRAINT "fk_contact_user_15dde9eb";
ALTER TABLE "contact" DROP COLUMN "user_id";
DROP TABLE IF EXISTS "user";
-- downgrade --
ALTER TABLE "contact" ADD "user_id" INT NOT NULL;
ALTER TABLE "contact" ADD CONSTRAINT "fk_contact_user_15dde9eb" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
