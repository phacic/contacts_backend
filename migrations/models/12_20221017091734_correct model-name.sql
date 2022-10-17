-- upgrade --
CREATE TABLE IF NOT EXISTS "socialmedia" (
    "label" VARCHAR(25) NOT NULL,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "url" VARCHAR(255) NOT NULL,
    "contact_id" INT NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "socialmedia" IS 'social media links for the contact';;
DROP TABLE IF EXISTS "socialmedial";
-- downgrade --
DROP TABLE IF EXISTS "socialmedia";
