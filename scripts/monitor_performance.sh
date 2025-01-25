#!/bin/bash

# Set variables
APP_URL="http://localhost:8000/health"  # Change this to your application's health endpoint
K8S_NAMESPACE="default"                   # Change this to your Kubernetes namespace if needed
DEPLOYMENT_NAME="gfms-core-app"          # Change this to your deployment name

# Function to check application health
check_health() {
    echo "Checking application health..."
    response=$(curl -s -o /dev/null -w "%{http_code}" $APP_URL)

    if [ "$response" -eq 200 ]; then
        echo "Application is healthy (HTTP Status: $response)"
    else
        echo "Application is not healthy (HTTP Status: $response)"
    fi
}

# Function to monitor Kubernetes deployment resource usage
monitor_k8s_resources() {
    echo "Monitoring Kubernetes resources for deployment: $DEPLOYMENT_NAME"
    kubectl top pods -n $K8S_NAMESPACE --selector=app=$DEPLOYMENT_NAME
}

# Function to log performance metrics
log_performance() {
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    echo "Performance metrics at $TIMESTAMP" >> performance.log
    echo "----------------------------------------" >> performance.log
    check_health >> performance.log
    monitor_k8s_resources >> performance.log
    echo "" >> performance.log
}

# Main script execution
log_performance

# Optional: Schedule this script to run at regular intervals using cron
# For example, to run every 5 minutes, add the following line to your crontab:
# */5 * * * * /path/to/monitor_performance.sh
