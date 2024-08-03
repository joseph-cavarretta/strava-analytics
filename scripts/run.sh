#!/bin/bash
docker run \
-p 8050:8050 \
--rm \
--volume ~/projects/strava-analytics/src/data:/data \
strava_app