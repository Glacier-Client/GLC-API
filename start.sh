##!/bin/bash
echo Starting Server!

uvicorn main:app --reload --host 10.5.56.10 --port 8083
