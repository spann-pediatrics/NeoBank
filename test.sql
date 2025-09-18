SELECT version();


-- inspect tables --
SELECT * FROM subjects LIMIT 5;

SELECT * FROM samples LIMIT 5;

SELECT * FROM milk LIMIT 5;

SELECT * FROM hmo_wide LIMIT 5;

SELECT * FROM hmo_long LIMIT 5;


---------- Cohort Overview ----------

-- number of unique subjects --
SELECT 
    Count(DISTINCT "Subject ID") AS total_subjects
FROM subjects;

-- number of unique samples --
SELECT Count(*) as n_samples FROM samples;

-- number of samples per subject --
SELECT "Subject ID", Count(*) as n_samples
FROM samples
GROUP BY "Subject ID"
ORDER BY n_samples DESC;

-- number of aliquots per sample --
SELECT "sample_unique_id", "Aliquots_num"
FROM samples
ORDER BY "Aliquots_num" DESC;

-- number of aliquots per subject --
SELECT "Subject ID", 
    SUM("Aliquots_num") as n_aliquots
FROM samples
GROUP BY "Subject ID"
ORDER BY n_aliquots DESC;



---- Infant Summary Stats ----

WITH birth_calc AS (
    SELECT 
        "Subject ID",
        MIN(("CGA" - ("DOL"/7))::int) AS ga_at_birth_weeks,   -- GA at birth per subject
        MIN("CGA")::int AS cga_first_sample                  -- earliest CGA observed per subject
    FROM subjects
    WHERE "DOL" IS NOT NULL
    GROUP BY "Subject ID"
),
duration AS (
    SELECT 
        "Subject ID",
        MIN("DOL") AS first_dol,
        MAX("DOL") AS last_dol,
        (MAX("DOL") - MIN("DOL")) AS length_of_days
    FROM subjects
    GROUP BY "Subject ID"
)
SELECT 
    b."Subject ID",
    b.ga_at_birth_weeks,
    b.cga_first_sample,
    b.cga_first_sample - b.ga_at_birth_weeks AS time_between_birth_and_first_sample_weeks,
    d.first_dol,
    d.last_dol,
    d.length_of_days
FROM birth_calc b
JOIN duration d ON b."Subject ID" = d."Subject ID"
ORDER BY b.ga_at_birth_weeks, b."Subject ID";




---- TPN per Subject ----

SELECT






