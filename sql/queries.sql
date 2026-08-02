-- Job count by canton
SELECT canton, COUNT(*) as job_count
FROM jobs
GROUP BY canton
ORDER BY job_count DESC;

-- Skills mentioned in working-student roles
SELECT skills_mentioned, COUNT(*) as job_count
FROM jobs
WHERE is_student_role = 1 AND skills_mentioned IS NOT NULL
GROUP BY skills_mentioned
ORDER BY job_count DESC;