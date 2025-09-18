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
        MIN(("CGA" - ("DOL"/7))::int) AS ga_at_birth_weeks,
        MIN("CGA")::int AS cga_first_sample
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
),
first_mbm AS (
    SELECT 
        "Subject ID",
        MIN("DOL") AS first_mbm_day
    FROM milk
    WHERE "MBM/DMB?" LIKE 'MBM%'
    GROUP BY "Subject ID"
)
SELECT 
    b."Subject ID",
    b.ga_at_birth_weeks,
    b.cga_first_sample,
    b.cga_first_sample - b.ga_at_birth_weeks AS time_between_birth_and_first_sample_weeks,
    d.first_dol,
    d.last_dol,
    d.length_of_days,
    COALESCE(f.first_mbm_day::text, 'Did not receive MOM') AS first_mbm_day,
    CASE
        WHEN f.first_mbm_day IS NOT NULL 
        THEN (f.first_mbm_day - d.first_dol)
        ELSE NULL
    END AS time_to_mom_days
FROM birth_calc b
JOIN duration d 
  ON b."Subject ID" = d."Subject ID"
LEFT JOIN first_mbm f 
  ON b."Subject ID" = f."Subject ID"
ORDER BY b."Subject ID";





---- TPN per Subject ----

--- count of subjects who recieved TPN --
SELECT 
    COUNT(DISTINCT "Subject ID") AS n_subjects_on_TPN
FROM milk
WHERE "TPN Y/N?" = 'Y';


-- 

WITH tpn_usage AS (
    SELECT 
        m."Subject ID",
        m."DOL",
        m."CGA"
    FROM milk m
    WHERE m."TPN Y/N?" = 'Y'
)
SELECT 
    "Subject ID",
    MIN("DOL") AS first_tpn_dol,
    MAX("DOL") AS last_tpn_dol,
    (MAX("DOL") - MIN("DOL")) AS tpn_duration_days,
    MIN("CGA") AS first_tpn_cga,
    MAX("CGA") AS last_tpn_cga,
    (MAX("CGA") - MIN("CGA")) AS tpn_duration_weeks
FROM tpn_usage
GROUP BY "Subject ID"
ORDER BY tpn_duration_days DESC;




--- GROWTH metrics ----

-- First values
WITH first_vals AS (
    SELECT DISTINCT ON ("Subject ID")
        "Subject ID", "DOL", "Current Weight", "Current Height", "Current HC"
    FROM subjects
    WHERE "DOL" IS NOT NULL
    ORDER BY "Subject ID", "DOL" ASC
),
last_vals AS (
    SELECT DISTINCT ON ("Subject ID")
        "Subject ID", "DOL", "Current Weight", "Current Height", "Current HC"
    FROM subjects
    WHERE "DOL" IS NOT NULL
    ORDER BY "Subject ID", "DOL" DESC
)
SELECT 
    f."Subject ID",
    f."DOL" AS first_dol,
    l."DOL" AS last_dol,
    f."Current Weight" AS weight_first,
    l."Current Weight" AS weight_last,
    (l."Current Weight" - f."Current Weight") AS weight_gain,
    f."Current Height" AS height_first,
    l."Current Height" AS height_last,
    (l."Current Height" - f."Current Height") AS height_gain,
    f."Current HC" AS hc_first,
    l."Current HC" AS hc_last,
    (l."Current HC" - f."Current HC") AS hc_gain
FROM first_vals f
JOIN last_vals l ON f."Subject ID" = l."Subject ID"
ORDER BY weight_gain DESC;



SELECT 
    s."Subject ID",
    s."DOL",
    s."CGA",
    s."Current Weight",
    (s."Current Weight" - r.mean) / r.sd AS weight_z
FROM samples s
JOIN growth_refs r
  ON s."CGA" = r.GA_weeks
 AND s."Sex" = r.sex
 AND r.parameter = 'weight';



--- growth z-scores = observed value - reference mean / reference SD ---    

