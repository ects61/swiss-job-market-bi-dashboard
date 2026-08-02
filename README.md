# Swiss Job Market BI Dashboard

A BI project that pulls Swiss job postings from the Adzuna API, cleans and
structures the data with pandas, loads it into SQLite, and visualizes it
in Power BI — showing which skills, roles, and cantons are most in demand,
split by Working Student vs. Full-Time postings.

## Status
v1 complete — data pipeline, SQLite storage, and a 3-visual Power BI dashboard.

## Stack
Python (pandas, requests) → SQLite → Power BI

## Data Source
[Adzuna API](https://developer.adzuna.com/), Switzerland (`ch`) endpoint,
filtered with `what_or` to target data/tech/BI/automation-related roles.
Sample size: 500 postings (10 pages x 50 results).

## Key Findings
- Zurich, Vaud, and Geneva account for the largest share of relevant postings.
- ~29% of matched postings are working student / internship roles.
- Only ~1% of postings disclose salary information — consistent with
  Switzerland's generally low salary-transparency norms.

## Project Structure
\`\`\`
├── data/
│   ├── raw/          # raw API pulls (not committed)
│   └── processed/    # cleaned CSV/XLSX + jobs.db (not committed)
├── notebooks/         # exploration and pipeline notebook
├── powerbi/            # .pbix dashboard file
├── sql/                # (reserved for standalone SQL scripts)
├── src/                # (reserved for refactored pipeline scripts)
└── requirements.txt
\`\`\`

## Setup
1. Clone the repo, create a virtual environment, install dependencies:
   \`\`\`
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   \`\`\`
2. Register for a free Adzuna API key at developer.adzuna.com, create a
   `.env` file in the project root with:
   \`\`\`
   ADZUNA_APP_ID=your_id
   ADZUNA_APP_KEY=your_key
   \`\`\`
3. Run the notebook (`notebooks/01_explore_adzuna.ipynb`) to fetch and
   clean data into `data/processed/jobs.db`.
4. Open `powerbi/swissjobmarket_dashboard.pbix`, refresh the data
   source to point to your local `jobs.db`.

## Known Limitations
- **Company field noise:** Some top "companies" (e.g. Job-Room) are
  likely aggregator/public job portals, not individual employers —
  the raw `company` field from Adzuna isn't always the actual hiring firm.
- **Truncated descriptions:** Adzuna's API returns a shortened job
  description snippet, not the full text — skill detection (keyword
  matching on title + description) likely undercounts actual demand.
- **Skill extraction is keyword-based**, not NLP-driven — it catches
  exact substring matches only (e.g. won't catch "Pythonic" as "python"
  correctly distinguishing intent, or synonyms).
- Sample reflects a single pull date, not a time trend.

## Next Steps
- Refactor notebook logic into reusable functions under `/src`
- Add a skills-breakdown visual (requires Power Query unpivot on
  `skills_mentioned`)
- Expand to jobs.ch as a second data source