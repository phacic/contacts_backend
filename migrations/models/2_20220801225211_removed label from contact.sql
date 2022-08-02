-- upgrade --
ALTER TABLE "contact" DROP COLUMN "label";
-- downgrade --
ALTER TABLE "contact" ADD "label" VARCHAR(15) NOT NULL;
