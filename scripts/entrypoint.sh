#!/bin/bash

# entry point for the uvicorn server
port="$1"
uvicorn src.server:app --host "0.0.0.0" --port "$port" --reload