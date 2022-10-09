-- upgrade --
ALTER TABLE "phone" ALTER COLUMN "phone_number" TYPE VARCHAR(30) USING "phone_number"::VARCHAR(30);
-- downgrade --
ALTER TABLE "phone" ALTER COLUMN "phone_number" TYPE VARCHAR(15) USING "phone_number"::VARCHAR(15);
