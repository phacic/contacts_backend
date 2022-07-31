-- upgrade --
ALTER TABLE "contact" ADD "user_id" INT NOT NULL;
ALTER TABLE "contacttag" ADD "contact_id" INT NOT NULL;
ALTER TABLE "email" ADD "contact_id" INT NOT NULL;
ALTER TABLE "phone" ADD "contact_id" INT NOT NULL;
ALTER TABLE "significantdate" ADD "contact_id" INT NOT NULL;
ALTER TABLE "contact" ADD CONSTRAINT "fk_contact_user_15dde9eb" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
ALTER TABLE "contacttag" ADD CONSTRAINT "fk_contactt_contact_eedbe134" FOREIGN KEY ("contact_id") REFERENCES "contact" ("id") ON DELETE CASCADE;
ALTER TABLE "email" ADD CONSTRAINT "fk_email_contact_78406f97" FOREIGN KEY ("contact_id") REFERENCES "contact" ("id") ON DELETE CASCADE;
ALTER TABLE "phone" ADD CONSTRAINT "fk_phone_contact_cdc3ac65" FOREIGN KEY ("contact_id") REFERENCES "contact" ("id") ON DELETE CASCADE;
ALTER TABLE "significantdate" ADD CONSTRAINT "fk_signific_contact_517fb935" FOREIGN KEY ("contact_id") REFERENCES "contact" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "significantdate" DROP CONSTRAINT "fk_signific_contact_517fb935";
ALTER TABLE "contacttag" DROP CONSTRAINT "fk_contactt_contact_eedbe134";
ALTER TABLE "contact" DROP CONSTRAINT "fk_contact_user_15dde9eb";
ALTER TABLE "phone" DROP CONSTRAINT "fk_phone_contact_cdc3ac65";
ALTER TABLE "email" DROP CONSTRAINT "fk_email_contact_78406f97";
ALTER TABLE "email" DROP COLUMN "contact_id";
ALTER TABLE "phone" DROP COLUMN "contact_id";
ALTER TABLE "contact" DROP COLUMN "user_id";
ALTER TABLE "contacttag" DROP COLUMN "contact_id";
ALTER TABLE "significantdate" DROP COLUMN "contact_id";
