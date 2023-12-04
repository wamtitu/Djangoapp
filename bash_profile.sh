#!/bin/bash

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Running on Windows with PowerShell
    $env:AZURE_TENANT_ID = "<tenant_id>"
    $env:AZURE_CLIENT_ID = "<client-id>"
    $env:AZURE_CLIENT_SECRET = "<client-secret>"
    $env:AZURE_SUBSCRIPTION_ID = "<subscription-id>"
    echo "Environment variables set successfully."

else
    # Assume running on Linux
    export AZURE_TENANT_ID="<tenant_id>"
    export AZURE_CLIENT_ID="<client-id>"
    export AZURE_CLIENT_SECRET="<client-secret>"
    export AZURE_SUBSCRIPTION_ID="<subscription-id>"
fi

# Print a message indicating successful execution
echo "Environment variables set successfully."
