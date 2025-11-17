# 🔄 DAILY REFRESH - QUICK START GUIDE

## ⚡ How to Update Your Dashboard Daily

---

## 📋 What You Need

1. ✅ Your dashboard files (already have them!)
2. ✅ New `Consolidated.xlsx` file with updated data
3. ✅ Python installed on your computer

---

## 🚀 Three Ways to Refresh

### **METHOD 1: One-Click Update** ⭐ (EASIEST - RECOMMENDED)

#### **On Windows:**
1. Place your new `Consolidated.xlsx` in the same folder as the dashboard
2. **Double-click** `REFRESH_DASHBOARD.bat`
3. Wait 10 seconds
4. Done! ✅

#### **On Mac/Linux:**
1. Place your new `Consolidated.xlsx` in the same folder
2. **Double-click** `refresh_dashboard.sh` 
   (Or run: `./refresh_dashboard.sh` in terminal)
3. Wait 10 seconds
4. Done! ✅

---

### **METHOD 2: Command Line** (Manual)

```bash
# Step 1: Put new Consolidated.xlsx in folder
# Step 2: Run command

# Windows:
python refresh_dashboard.py

# Mac/Linux:
python3 refresh_dashboard.py
```

---

### **METHOD 3: Scheduled Automation** (Advanced)

Set it to run automatically every day at a specific time.

#### **Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task → Name it "Dashboard Refresh"
3. Trigger: Daily at 8:00 AM
4. Action: Start a Program
5. Program: `C:\path\to\REFRESH_DASHBOARD.bat`
6. Save and test

#### **Mac/Linux Cron Job:**
```bash
# Open cron editor
crontab -e

# Add this line (runs daily at 8:00 AM)
0 8 * * * /path/to/refresh_dashboard.sh

# Save and exit
```

---

## 📂 File Setup

Your folder should look like this:

```
📁 Your Dashboard Folder
├── 📊 Consolidated.xlsx          ← Place new file here daily
├── 🌐 procurement_dashboard.html  ← Your dashboard
├── 🐍 refresh_dashboard.py        ← Refresh script
├── 🖱️ REFRESH_DASHBOARD.bat      ← Windows one-click
├── 🖱️ refresh_dashboard.sh        ← Mac/Linux one-click
└── 📁 backup_20251110_143025/    ← Auto backups (created automatically)
```

---

## 🎬 Step-by-Step: Daily Update Process

### **Every Morning (Example):**

```
8:00 AM - You receive new Consolidated.xlsx via email
   ↓
8:01 AM - You save it to your dashboard folder
   ↓
8:02 AM - You double-click REFRESH_DASHBOARD.bat
   ↓
8:02 AM - Script runs for 10 seconds
   ↓
         ✅ Dashboard updated!
         ✅ UiPath files refreshed!
         ✅ Backup created automatically!
   ↓
8:03 AM - You open procurement_dashboard.html
   ↓
8:03 AM - See today's fresh data! 🎉
```

---

## 🖼️ What Happens During Refresh?

### **The Script Automatically:**

1. **📦 Creates Backup**
   - Saves old files to `backup_YYYYMMDD_HHMMSS/` folder
   - You can restore from backup if needed

2. **📊 Processes New Data**
   - Reads your new Consolidated.xlsx
   - Calculates all metrics (TAT, volumes, etc.)
   - Processes all 5 processes (PR, PO, POA, R31, R37)

3. **🔄 Updates Files**
   - ✅ procurement_dashboard.html (with new charts)
   - ✅ dashboard_data.json (complete metrics)
   - ✅ uipath_queue_data.json (bot queue)
   - ✅ uipath_metrics.json (KPIs)
   - ✅ uipath_poa_data.csv (31,000+ records)
   - ✅ uipath_r31_data.csv (21,000+ records)
   - ✅ uipath_r37_data.csv (21,000+ records)

4. **✅ Shows Summary**
   - Total records processed
   - Bot automation rate
   - Average TAT
   - SLA compliance

---

## 🎨 You'll See This Output:

```
================================================================================
                    PROCUREMENT DASHBOARD - DAILY REFRESH
================================================================================

ℹ️  Creating backup of existing files...
✅ Backup created in: backup_20251110_143025

================================================================================
                       📊 PROCESSING PROCUREMENT DATA
================================================================================

ℹ️  Reading file: Consolidated.xlsx
✅ File loaded successfully!
ℹ️  Found 5 sheets
ℹ️  Processing PR Create data...
✅ PR Create: 37,331 records processed
ℹ️  Processing PO Create data...
✅ PO Create: 26,583 records processed
ℹ️  Processing POA data...
✅ POA: 31,135 records | Avg TAT: 0.07 days
ℹ️  Processing Release 31 data...
✅ Release 31: 21,592 records | Avg TAT: 0.06 days
ℹ️  Processing Release 37 data...
✅ Release 37: 21,592 records | Avg TAT: 0.07 days

================================================================================
                   🤖 GENERATING UIPATH INTEGRATION FILES
================================================================================

ℹ️  Creating queue data...
✅ Queue data created
ℹ️  Creating metrics data...
✅ Metrics data created
ℹ️  Exporting CSV files...
✅ CSV files exported

================================================================================
                           📈 PROCESSING SUMMARY
================================================================================

Total Records Processed: 138,233
Bot Automation Rate: 99.99%
Average TAT: 0.07 days
SLA Compliance: 99.96%

================================================================================
                            🌐 UPDATING DASHBOARD HTML
================================================================================

ℹ️  Reading dashboard template...
ℹ️  Injecting new data...
ℹ️  Saving updated dashboard...
✅ Dashboard HTML updated successfully!

================================================================================
                              ✅ REFRESH COMPLETE
================================================================================

Your dashboard has been updated with fresh data!

What's been updated:
  ✅ Dashboard HTML with new visualizations
  ✅ JSON data files for UiPath integration
  ✅ CSV exports for bot processing
  ✅ Performance metrics and queue data

Backup location: backup_20251110_143025

Next step: Open 'procurement_dashboard.html' in your browser!
```

---

## 📊 Dashboard Updates Automatically

After refresh, your dashboard will show:

### **Updated Header:**
```
Dashboard generated: November 11, 2025, 8:02:15 AM  ← New timestamp!
```

### **Updated Numbers:**
All cards, charts, and metrics refresh with new data:
- Total PRs, POs, POAs
- TAT averages
- Bot automation rates
- High TAT alerts
- All visualizations

---

## 🔄 Daily Workflow Example

### **Monday Morning:**
```
1. Export Consolidated.xlsx from your system
2. Save to dashboard folder
3. Double-click REFRESH_DASHBOARD.bat
4. Open procurement_dashboard.html
5. Review yesterday's performance
6. Share dashboard link with team
```

### **Tuesday Morning:**
```
1. Export new Consolidated.xlsx (Tuesday data)
2. Replace Monday's file
3. Double-click REFRESH_DASHBOARD.bat
4. Dashboard now shows Tuesday's data
5. Monday's data automatically backed up
```

---

## ⚠️ Troubleshooting

### **Problem: "Python not found"**
**Solution:**
1. Install Python from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart computer
4. Try again

### **Problem: "Consolidated.xlsx not found"**
**Solution:**
1. Ensure the file is named exactly: `Consolidated.xlsx`
2. It must be in the same folder as the scripts
3. Check for typos in filename

### **Problem: "Script fails to run"**
**Solution:**
1. Check if you have pandas installed:
   ```
   pip install pandas openpyxl
   ```
2. Make sure Excel file isn't corrupted
3. Check backup folder - you can restore old version

### **Problem: "Dashboard looks blank"**
**Solution:**
1. Refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Check if dashboard_data.json has data
4. Restore from most recent backup

---

## 📁 Backup & Restore

### **Automatic Backups:**
Every time you refresh, old files are backed up to:
```
backup_20251110_080215/
backup_20251111_080345/
backup_20251112_080512/
```

### **To Restore from Backup:**
1. Go to the backup folder (e.g., `backup_20251110_080215/`)
2. Copy files back to main folder
3. Replace current files

---

## 🤖 UiPath Integration Still Works

After each refresh:
- ✅ All UiPath files update automatically
- ✅ Queue data reflects new pending items
- ✅ CSV files contain latest records
- ✅ Metrics show current performance
- ✅ Your bots see fresh data immediately

---

## 💡 Pro Tips

### **Tip 1: Morning Routine**
Set up daily reminder:
```
8:00 AM - Export data from SAP
8:05 AM - Run refresh script
8:10 AM - Review dashboard in team meeting
```

### **Tip 2: Keep Last 7 Days**
```
# Delete backups older than 7 days
# Windows: Manual deletion of old backup folders
# Linux/Mac: Add to cron:
find . -name "backup_*" -mtime +7 -exec rm -rf {} \;
```

### **Tip 3: Email Automation**
After refresh completes, automatically email the dashboard link to your team using a simple email script.

### **Tip 4: Version Control**
Keep the last few `Consolidated.xlsx` files:
```
Consolidated_2025-11-10.xlsx
Consolidated_2025-11-11.xlsx
Consolidated_2025-11-12.xlsx
```

---

## ✅ Checklist: First Time Setup

- [ ] Install Python 3.x
- [ ] Place all dashboard files in one folder
- [ ] Place Consolidated.xlsx in that folder
- [ ] Test run: Double-click REFRESH_DASHBOARD.bat
- [ ] Verify dashboard opens with data
- [ ] Check backup folder was created
- [ ] Bookmark dashboard HTML file
- [ ] Set calendar reminder for daily updates

---

## 🎯 Summary

| Task | Time | Difficulty |
|------|------|------------|
| Daily refresh | 10 seconds | ⭐ Easy |
| First setup | 5 minutes | ⭐⭐ Simple |
| Automation | 10 minutes | ⭐⭐⭐ Moderate |

**Total Time Investment:** 5-10 minutes to set up, then 10 seconds daily forever!

---

## 📞 Quick Reference

### **Windows Users:**
```
Double-click: REFRESH_DASHBOARD.bat
```

### **Mac/Linux Users:**
```
Double-click: refresh_dashboard.sh
```

### **Command Line:**
```bash
python refresh_dashboard.py
```

### **Files Updated:**
- ✅ procurement_dashboard.html
- ✅ dashboard_data.json
- ✅ uipath_queue_data.json
- ✅ uipath_metrics.json
- ✅ uipath_poa_data.csv
- ✅ uipath_r31_data.csv
- ✅ uipath_r37_data.csv

---

## 🎉 You're All Set!

Your dashboard now has **intelligent daily refresh** capabilities!

1. ✅ One-click updates
2. ✅ Automatic backups
3. ✅ UiPath integration refreshes
4. ✅ Error handling
5. ✅ Beautiful status output

**Just replace the Excel file and click the batch file - that's it!** 🚀

---

*Generated: November 10, 2025*
*Status: ✅ Ready to Use*
