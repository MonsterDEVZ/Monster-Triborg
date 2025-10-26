#!/bin/bash
export PYTHONPATH=/app:$PYTHONPATH
exec /opt/venv/bin/python3 apps/bot/main.py
