# Epilepsy Intelligence Platform — API image
FROM python:3.12-slim

WORKDIR /app

# System deps kept minimal; scientific wheels install cleanly on slim.
COPY analysis/requirements.txt /app/analysis/requirements.txt
COPY api/requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir -r /app/analysis/requirements.txt \
 && pip install --no-cache-dir -r /app/api/requirements.txt

# App code + data artefacts needed at runtime.
COPY analysis /app/analysis
COPY data /app/data
COPY db /app/db
COPY api /app/api

# Materialise the SQLite DB + scenario/weight CSVs at build time.
RUN cd /app/analysis && python make_cohort.py && python build_scenarios.py \
 && cd /app && python db/build_sqlite.py

EXPOSE 8000
# EPI_API_KEY can be injected at run time to enable auth.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
