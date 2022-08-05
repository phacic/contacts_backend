-- upgrade --
ALTER TABLE "contact" DROP COLUMN "address";
ALTER TABLE "contact" ALTER COLUMN "spouse" DROP NOT NULL;
ALTER TABLE "contact" ALTER COLUMN "status" SET DEFAULT 'A';
ALTER TABLE "contact" ALTER COLUMN "nickname" DROP NOT NULL;
-- downgrade --
ALTER TABLE "contact" ADD "address" TEXT;
ALTER TABLE "contact" ALTER COLUMN "spouse" SET NOT NULL;
ALTER TABLE "contact" ALTER COLUMN "status" DROP DEFAULT;
ALTER TABLE "contact" ALTER COLUMN "nickname" SET NOT NULL;
