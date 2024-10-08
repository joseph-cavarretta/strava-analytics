#!/bin/bash
docker run \
-p 8050:8050 \
--rm \
--volume ~/dev/strava-analytics/app/data:/data \
strava_app