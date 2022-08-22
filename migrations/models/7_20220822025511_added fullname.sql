-- upgrade --
ALTER TABLE "user" ADD "full_name" VARCHAR(150);
-- downgrade --
ALTER TABLE "user" DROP COLUMN "full_name";
