# EpiScope

District surveillance, forecasting and response planning for Bangladesh using Apache Spark and a linked D3 dashboard.

| Team member | Student ID | Focus |
|---|---|---|
| Dipton Dey | 0222420005101291 | Data engineering and quality |
| Shaishob Boidya | 0222220005101049 | Analytics and resource allocation |
| Manik Dey | 0222220005101096 | Dashboard and presentation |

**Repository:** https://github.com/SB-Abhi1/BDA-EpiScope

**Presentation:** https://drive.google.com/file/d/1imK_dGQrPre40pLm3VUMRmqRg-ZkajXz/view?usp=drive_link

Health encounters, facilities and stock feeds are synthetic. Public boundaries, weather and population inputs retain their documented provenance. Results support an educational prototype and do not establish operational surveillance accuracy.

## Dashboard

The bundled dashboard runs without Spark or a full data rebuild:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory dashboard
```

Open http://127.0.0.1:8000. Serve only the `dashboard` directory. All required browser assets are bundled locally.

## Environment and installation

Python 3.12, Java 17 and Spark 3.5.3 are used. Full-scale execution was evaluated in the recorded Linux environment; timings are in `docs/evidence/scaling.json`. The assignment targets a 16 GB laptop or suitable free-tier environment. A 4 GB Windows machine is suitable for the dashboard preview but may not complete the full pipeline. Native Windows end-to-end execution has not been verified.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_all.py --sf 1
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install -r requirements.txt
.\.venv312\Scripts\python.exe scripts/run_all.py --sf 1
```

Java must be on PATH. Native Windows Spark also requires matching Hadoop Windows helpers and `HADOOP_HOME`; these system dependencies are not bundled. Existing source downloads and generated data can be reused with:

```bash
python scripts/run_all.py --sf 1 --skip-sources --skip-generator
```

A small functional run uses `--sf 0.002`; it does not satisfy the full-volume requirement. To limit concurrency, set `SPARK_MASTER=local[1]` and an appropriate `SPARK_DRIVER_MEMORY` before launching. Reducing memory does not guarantee that a full-scale run will fit.

## Pipeline

1. Acquire and cache public reference inputs.
2. Generate seeded encounters, facilities and stock feeds.
3. Ingest bronze snapshots with checksums and lineage.
4. Validate, quarantine and de-identify records into silver.
5. Build weekly counts, reporting vintages, quality and stock marts.
6. Run reporting-aware detection, forecasting, evaluation and allocation.
7. Export privacy-filtered aggregates to the dashboard.

At scale factor 1, generation produces 25 million unique encounters plus deliberate resubmissions. Failed stages stop the orchestrator. Outputs in `data/` are local processing products; the repository contains public reference inputs and the published dashboard aggregates.

## Incremental processing

The input contract is documented in [DATA_CONTRACT.md](docs/DATA_CONTRACT.md). Keep the existing data lake and hashing salt. Place a new encounter drop outside `data/incoming/base` and run:

```bash
python -m pipeline.run --incoming /path/to/drop
python -m analytics.run
python -m serving.export
```

Repeating the same ingestion is a checksum no-op. Later-report corrections revise affected onset weeks. Year-partition replacement is staged but is not an atomic multi-partition transaction.

## Methods and limitations

- Detection: report-vintage CUSUM, seasonal z-score comparison and a facility-backfill guard.
- Forecasting: direct one-to-four-week ridge models evaluated at 52 rolling origins against a seasonal-naive baseline. The ridge model does not consistently outperform that baseline; interval coverage needs calibration.
- Demand: upper forecast bounds converted with explicit synthetic planning coefficients.
- Allocation: HiGHS linear programming under budget, equity, central-stock and transport constraints; comparison against a feasible population baseline. Five budgets and three equity settings are precomputed.
- Privacy: salted hashing before silver, aggregate-only exports, suppression of counts 1-4 and associated scores, and omission of exact parent totals.
- Dashboard: district map, case timeline, seasonal heatmap, allocation view and warning table, with coordinated filters and date brushing.

Demographic inputs use documented USCB projections calibrated to a BBS-labelled district-total layer; these are not observed BBS2022 age-sex counts. Formal usability testing, prospective real-world validation, stronger crash recovery and broader accessibility testing remain future work. Docker configuration is included; Docker execution was not independently verified.

## Verification and documents

```bash
python -m unittest discover -s tests -v
python scripts/integration_check.py
python scripts/build_documents.py
```

The integration check requires a populated local data lake. Document generation uses local results when present and otherwise the bundled published evidence; it does not imply that a new compute run occurred.

- [Technical report](docs/EpiScope_Technical_Report.pdf), including the policy brief, contribution matrix, reflections and requirement traceability.
- [Policy brief](docs/EpiScope_Policy_Brief.pdf).
- [Proposal](docs/proposal.md).
- [Requirement traceability](docs/requirements.csv).
- [Evaluation evidence](docs/evidence/).
- [Third-party notices](THIRD_PARTY_NOTICES.md) and [assistance disclosure](AI_USAGE.md).

The report cover contains the group number and external links. Contribution statistics correspond to actual Git history; signatures belong to the individual members.

## Presentation chapters

- 00:00 - Problem and stakeholders
- 01:20 - Architecture and data sources
- 02:21 - Pipeline execution and validation
- 04:00 - Detection and forecasting
- 06:07 - Resource demand and allocation
- 07:30 - Seasonal calendar
- 08:00 - Dashboard walkthrough
- 10:24 - Scenarios, privacy and quality
- 11:28 - Recommendations and limitations

## Repository structure

```text
generator/   Synthetic data generation
pipeline/    Ingestion, validation, quarantine and lake layers
analytics/   Detection, forecasting, evaluation and optimisation
serving/     Privacy-filtered dashboard exports
dashboard/   D3 application and published aggregate data
scripts/     Sources, orchestration, benchmarks and document generation
tests/       Invariant tests
data/reference/  Public reference inputs and provenance
docs/        Report, policy brief, proposal and evidence
```
