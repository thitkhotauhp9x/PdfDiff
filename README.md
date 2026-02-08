# How to run

```bash
docker compose up --build
docker compose run pdftools pdfdiff
```

# How to build
```bash
poetry build
docker compose up --build
docker compose run pdftools pdfdiff
```

# How to run without Docker

```bash
poetry run pdfdiff
```
