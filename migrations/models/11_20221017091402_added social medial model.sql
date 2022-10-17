-- upgrade --
CREATE TABLE IF NOT EXISTS "socialmedial" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "url" VARCHAR(255) NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "socialmedial" IS 'social media links for the contact';
-- downgrade --
DROP TABLE IF EXISTS "socialmedial";
