-- =====================================================================
-- schema.sql — Epilepsy Intelligence Platform relational schema (PostgreSQL)
-- ---------------------------------------------------------------------
-- Turns the file-based assessment model (markdown forms + CSV cohort +
-- scenario catalogue) into a normalised relational database suitable for
-- an EMR-backed deployment. Mirrors the artefacts in the repo:
--   * 9 roles, 71 sections, 782 enterprise questionnaire items
--   * 4-level severity model + weighted scoring
--   * 57-scenario seizure/epilepsy catalogue
-- Every table is commented with its purpose; foreign keys enforce the
-- role -> section -> question -> answer -> score lineage.
-- =====================================================================

-- ---- Reference: 4-level severity ladder ----
CREATE TABLE severity_level (
    level        SMALLINT PRIMARY KEY CHECK (level BETWEEN 1 AND 4),
    name         TEXT NOT NULL,            -- Mild / Moderate / Severe / Refractory-Status
    description  TEXT
);

-- ---- Roles (Neurologist, EEG Technician, ... Occupational Therapist) ----
CREATE TABLE role (
    role_id      SERIAL PRIMARY KEY,
    code         TEXT UNIQUE NOT NULL,     -- e.g. 'neurologist'
    name         TEXT NOT NULL,            -- 'Neurologist'
    id_prefix    TEXT NOT NULL,            -- 'NEU'
    domain_weight NUMERIC(4,3) NOT NULL DEFAULT 0.0  -- weight in composite score (sums to 1.0)
);

-- ---- Assessment sections (one per numbered markdown file) ----
CREATE TABLE section (
    section_id   SERIAL PRIMARY KEY,
    role_id      INT NOT NULL REFERENCES role(role_id),
    code         TEXT NOT NULL,            -- '03-seizure-history'
    ordinal      SMALLINT NOT NULL,
    title        TEXT NOT NULL,
    UNIQUE (role_id, code)
);

-- ---- Enterprise questionnaire items (the 782 questions) ----
CREATE TABLE question (
    question_id   SERIAL PRIMARY KEY,
    section_id    INT NOT NULL REFERENCES section(section_id),
    ext_id        TEXT UNIQUE NOT NULL,    -- 'NEU-0301'
    text          TEXT NOT NULL,           -- patient-facing question
    response_type TEXT NOT NULL,           -- Text/Number/Date/Yes-No/Dropdown[...]/...
    validation    TEXT,                    -- range/format/allowed set
    ai_feature    TEXT,                    -- snake_case derived feature name
    item_weight   NUMERIC(4,2) NOT NULL DEFAULT 1.0
);

-- ---- Patients ----
CREATE TABLE patient (
    patient_id   TEXT PRIMARY KEY,         -- 'EP001'
    study_id     TEXT UNIQUE,              -- 'DBA-EP-001' (de-identified)
    age          SMALLINT CHECK (age BETWEEN 0 AND 120),
    sex          TEXT CHECK (sex IN ('M','F','Intersex')),
    focus_side   TEXT,                     -- 'Left' / 'Right'
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---- Seizure / epilepsy scenario catalogue (57 rows) ----
CREATE TABLE scenario (
    scenario_id     TEXT PRIMARY KEY,      -- 'SZ-F02'
    category        TEXT NOT NULL,         -- Seizure Type / Syndrome / Clinical / Severity
    name            TEXT NOT NULL,
    onset           TEXT,
    awareness       TEXT,
    ilae_class      TEXT,
    severity_level  SMALLINT REFERENCES severity_level(level),
    clinical_weight NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    key_features    TEXT
);

-- ---- A completed assessment (one role filling one patient's form) ----
CREATE TABLE assessment (
    assessment_id  BIGSERIAL PRIMARY KEY,
    patient_id     TEXT NOT NULL REFERENCES patient(patient_id),
    role_id        INT NOT NULL REFERENCES role(role_id),
    performed_by   TEXT,                   -- clinician identity (accountability)
    performed_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---- Individual answers, each scored to a severity level ----
CREATE TABLE answer (
    answer_id      BIGSERIAL PRIMARY KEY,
    assessment_id  BIGINT NOT NULL REFERENCES assessment(assessment_id) ON DELETE CASCADE,
    question_id    INT NOT NULL REFERENCES question(question_id),
    raw_value      TEXT,                   -- the captured response
    severity_level SMALLINT REFERENCES severity_level(level),  -- mapped 1..4
    UNIQUE (assessment_id, question_id)
);

-- ---- Derived scores: section -> role -> patient composite ----
CREATE TABLE section_score (
    id            BIGSERIAL PRIMARY KEY,
    assessment_id BIGINT NOT NULL REFERENCES assessment(assessment_id) ON DELETE CASCADE,
    section_id    INT NOT NULL REFERENCES section(section_id),
    score         NUMERIC(4,2) NOT NULL,   -- weighted mean of item levels
    band          SMALLINT REFERENCES severity_level(level)
);

CREATE TABLE patient_score (
    id             BIGSERIAL PRIMARY KEY,
    patient_id     TEXT NOT NULL REFERENCES patient(patient_id),
    composite_score NUMERIC(4,2) NOT NULL, -- Σ(role_score · domain_weight)
    band           SMALLINT REFERENCES severity_level(level),
    computed_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---- Governance / accountability audit log (every RAI-relevant event) ----
CREATE TABLE audit_log (
    id           BIGSERIAL PRIMARY KEY,
    actor        TEXT,                     -- who
    action       TEXT NOT NULL,            -- what
    entity       TEXT,                     -- table/record
    detail       JSONB,                    -- model/prompt/dataset version, confidence
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---- Indexes for the common access paths ----
CREATE INDEX idx_section_role      ON section(role_id);
CREATE INDEX idx_question_section  ON question(section_id);
CREATE INDEX idx_answer_assessment ON answer(assessment_id);
CREATE INDEX idx_assessment_patient ON assessment(patient_id);
CREATE INDEX idx_scenario_category ON scenario(category);

-- ---- Seed the severity ladder ----
INSERT INTO severity_level (level, name, description) VALUES
 (1,'Mild','Well-controlled; rare/absent seizures; no restriction'),
 (2,'Moderate','~Monthly seizures; minor impact; mild QoL reduction'),
 (3,'Severe','Several/month; breakthrough despite adherence; restrictions (EP001)'),
 (4,'Refractory/Status','Seizures ~every 5 min / drug-resistant; operational emergency');
