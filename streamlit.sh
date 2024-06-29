#!/bin/bash

# Define the command to run your Streamlit app
CMD="streamlit run app/streamlit_app.py"

# Define the log directory and file
LOGDIR="logs"
LOGFILE="${LOGDIR}/streamlit.log"

# Create the log directory if it does not exist
mkdir -p $LOGDIR

# Function to check if the command was successful
function check_command {
    "$@"
    status=$?
    if [ $status -ne 0 ]; then
        echo "error with $1" >&2
        echo "$(date) - Error with $1" >> $LOGFILE
    fi
    return $status
}

# Run the command and check if it was successful
check_command "$CMD"
