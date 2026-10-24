# Build plan: move the Wrenfield Gazette archive from SQLite to Postgres

**Owner:** Platform team
**Goal:** The public archive site reads from Postgres instead of `archive.db`, so editors can run reports without copying the file.

## Context

The archive holds every issue since 2014 in `/srv/archive/archive.db` (about 9 GB). The site is served by the `archive-web` service on `gazette-app-1`. Postgres 16 already runs on `gazette-db-1`.

## Steps

1. Stop the archive site: `sudo systemctl stop archive-web`.
2. Export the archive: `./bin/archive-export --since-epoch --format=jsonl > /tmp/archive.jsonl`.
3. Create the Postgres schema using the table layout we agreed on earlier.
4. Load the export: `./bin/archive-load --input /tmp/archive.jsonl --target postgres`.
5. Delete the old database to free disk space: `rm /srv/archive/archive.db`.
6. Set `DATABASE_URL` in `/etc/archive/env` and start the site: `sudo systemctl start archive-web`.

## Done when

The archive homepage loads.
