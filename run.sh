#!/usr/bin/env bash

if [ -n "$REPORT_OUTPUT_DIR" ]; then
    timestamp=$(date +%Y%m%d%H%M%S)
    output_dir="$REPORT_OUTPUT_DIR/$timestamp"
    mkdir -p "$output_dir"
    
    echo "Running as master node"
    locust -f "src/$LOCUST_FILE" \
    --host $LOCUST_HOST \
    --users $LOCUST_USERS \
    --spawn-rate $LOCUST_SPAWN_RATE \
    --run-time $LOCUST_RUN_TIME \
    --headless \
    --csv $output_dir/simod-http \
    --logfile $output_dir/locust.log \
    --loglevel INFO \
    --html $output_dir/report.html \
    --autostart \
    --autoquit 1 \
    --master
    
else
    echo "Running as worker node"
    locust -f src/$LOCUST_FILE \
    --worker \
    --master-host=$LOCUST_MASTER_NODE_HOST
fi
