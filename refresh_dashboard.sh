#!/bin/bash
# ================================================================
# PROCUREMENT DASHBOARD - ONE-CLICK REFRESH (MAC/LINUX)
# ================================================================

echo ""
echo "======================================================================"
echo "   PROCUREMENT DASHBOARD - DAILY REFRESH"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

# Check if Consolidated.xlsx exists
if [ ! -f "Consolidated.xlsx" ]; then
    echo "❌ ERROR: Consolidated.xlsx not found!"
    echo ""
    echo "Please place your Consolidated.xlsx file in this folder:"
    echo "$(pwd)"
    echo ""
    exit 1
fi

echo "✅ Found: Consolidated.xlsx"
echo ""
echo "Starting refresh process..."
echo ""

# Run the refresh script
python3 refresh_dashboard.py

echo ""
echo "======================================================================"
echo "Refresh complete!"
echo ""
