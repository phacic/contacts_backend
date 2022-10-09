-- upgrade --
ALTER TABLE "contacttag" ALTER COLUMN "tag" TYPE VARCHAR(50) USING "tag"::VARCHAR(50);
ALTER TABLE "phone" ALTER COLUMN "phone_number" TYPE VARCHAR(50) USING "phone_number"::VARCHAR(50);
-- downgrade --
ALTER TABLE "phone" ALTER COLUMN "phone_number" TYPE VARCHAR(15) USING "phone_number"::VARCHAR(15);
ALTER TABLE "contacttag" ALTER COLUMN "tag" TYPE VARCHAR(15) USING "tag"::VARCHAR(15);
