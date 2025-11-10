# 🤖 UiPath Integration Guide
## Procurement Dashboard - Bot Integration Documentation

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Available Data Files](#available-data-files)
3. [Integration Methods](#integration-methods)
4. [UiPath Bot Examples](#uipath-bot-examples)
5. [API Endpoints](#api-endpoints)
6. [Queue Management](#queue-management)
7. [Performance Monitoring](#performance-monitoring)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This dashboard provides **real-time procurement process monitoring** with deep UiPath bot integration capabilities. Your bots can:

- ✅ Access real-time queue data
- ✅ Update processing status
- ✅ Track TAT metrics
- ✅ Monitor SLA compliance
- ✅ Export data for analysis
- ✅ Receive webhook alerts

---

## 📁 Available Data Files

### 1. **dashboard_data.json**
Complete dashboard metrics and statistics.

**Use Case:** Bot dashboard integration, reporting, analytics

```json
{
  "summary": {
    "total_prs": 37331,
    "total_pos": 26583,
    "total_poas": 31135,
    "avg_tat_poa": 0.07,
    ...
  },
  "pr_create": {...},
  "po_create": {...},
  "poa": {...},
  "release_31": {...},
  "release_37": {...}
}
```

### 2. **uipath_queue_data.json**
Queue items ready for bot processing.

**Use Case:** Bot work queue, priority assignment

```json
{
  "pending_poas": 31104,
  "manual_poas": 0,
  "pending_releases": 21592,
  "high_tat_poas": 13,
  "high_tat_r31": 22,
  "high_tat_r37": 24
}
```

### 3. **uipath_metrics.json**
Performance metrics for Orchestrator monitoring.

**Use Case:** SLA tracking, automation rate monitoring

```json
{
  "process_metrics": {
    "pr_to_po_conversion": 71.2,
    "bot_automation_rate": 99.99,
    "avg_processing_time": {...},
    "sla_compliance": {...}
  }
}
```

### 4. **CSV Data Tables**
- `uipath_poa_data.csv` - Full POA dataset (31,135 records)
- `uipath_r31_data.csv` - Release 31 data (21,592 records)
- `uipath_r37_data.csv` - Release 37 data (21,592 records)

**Use Case:** Bulk processing, data analysis, Excel integration

---

## 🔗 Integration Methods

### Method 1: Direct File Access (Recommended for Development)

```vb
' UiPath - Read JSON Data
Dim jsonContent As String = File.ReadAllText("dashboard_data.json")
Dim data As JObject = JObject.Parse(jsonContent)

' Access specific metrics
Dim totalPOAs As Integer = data("summary")("total_poas").ToObject(Of Integer)
Dim avgTAT As Double = data("summary")("avg_tat_poa").ToObject(Of Double)
```

### Method 2: REST API Integration (Production)

```vb
' UiPath - HTTP Request Activity
Dim endpoint As String = "https://your-api.com/api/procurement/summary"
Dim response As String = ""

' Use HTTP Request Activity
' Method: GET
' Endpoint: endpoint
' Output: response

Dim data As JObject = JObject.Parse(response)
```

### Method 3: CSV Data Table Processing

```vb
' UiPath - Read CSV
Dim poaDataTable As DataTable
Read CSV Activity -> poaDataTable

' Filter high TAT items
Dim highTATItems = From row In poaDataTable.AsEnumerable()
                   Where Convert.ToDouble(row("Turn around in Days")) > 2
                   Select row

' Process each item
For Each item In highTATItems
    ' Your bot logic here
Next
```

---

## 🤖 UiPath Bot Examples

### Example 1: POA Processing Bot

**Purpose:** Automatically process pending POAs from the queue

```vb
'══════════════════════════════════════════════════════════
' POA PROCESSING BOT - Main Workflow
'══════════════════════════════════════════════════════════

' STEP 1: Get Queue Data
Dim queueJson As String = File.ReadAllText("uipath_queue_data.json")
Dim queueData As JObject = JObject.Parse(queueJson)
Dim pendingCount As Integer = queueData("pending_poas").ToObject(Of Integer)

Log Message: "Pending POAs: " + pendingCount.ToString()

' STEP 2: Load POA Data
Dim poaDataTable As DataTable
Read CSV: "uipath_poa_data.csv" -> poaDataTable

' STEP 3: Filter Pending Items (BOT processing only)
Dim pendingPOAs = From row In poaDataTable.AsEnumerable()
                  Where row("BOT/MANUAL/SERVICE PROVIDER").ToString() = "BOT"
                  And Convert.ToDouble(row("Turn around in Days")) < 1
                  Select row

' STEP 4: Process Each POA
Dim processedCount As Integer = 0
Dim startTime As DateTime = DateTime.Now

For Each poa In pendingPOAs
    Try
        ' Get POA details
        Dim poNumber As String = poa("PO Number").ToString()
        Dim createDate As String = poa("PO Create Date").ToString()
        
        ' YOUR BOT LOGIC HERE
        ' - Open SAP/System
        ' - Navigate to PO
        ' - Validate data
        ' - Submit acknowledgement
        ' - Capture screenshot
        
        processedCount += 1
        Log Message: "✅ Processed PO: " + poNumber
        
    Catch ex As Exception
        Log Message: "❌ Error processing PO: " + poa("PO Number").ToString()
        Log Message: ex.Message
    End Try
Next

' STEP 5: Calculate Performance Metrics
Dim endTime As DateTime = DateTime.Now
Dim duration As TimeSpan = endTime.Subtract(startTime)
Dim avgTime As Double = duration.TotalSeconds / processedCount

Log Message: String.Format("📊 Processed {0} POAs in {1:F2} seconds", processedCount, duration.TotalSeconds)
Log Message: String.Format("⚡ Average time per POA: {0:F2} seconds", avgTime)

' STEP 6: Update Orchestrator Queue
' Add Queue Items for failed transactions
' Update Asset variables with new metrics
```

### Example 2: High TAT Alert Bot

**Purpose:** Monitor and alert on high TAT items

```vb
'══════════════════════════════════════════════════════════
' HIGH TAT MONITORING BOT
'══════════════════════════════════════════════════════════

' Load Queue Data
Dim queueJson As String = File.ReadAllText("uipath_queue_data.json")
Dim queueData As JObject = JObject.Parse(queueJson)

' Get High TAT Counts
Dim highTATPOA As Integer = queueData("high_tat_poas").ToObject(Of Integer)
Dim highTATR31 As Integer = queueData("high_tat_r31").ToObject(Of Integer)
Dim highTATR37 As Integer = queueData("high_tat_r37").ToObject(Of Integer)

' Check if alerts needed
Dim totalHighTAT As Integer = highTATPOA + highTATR31 + highTATR37

If totalHighTAT > 50 Then
    ' CRITICAL ALERT
    Send Outlook Mail
    To: "procurement.manager@company.com"
    Subject: "🚨 CRITICAL: High TAT Items Detected"
    Body: String.Format("
        High TAT Alert Summary:
        
        🔴 High TAT POAs: {0}
        🔴 High TAT Release 31: {1}
        🔴 High TAT Release 37: {2}
        
        Total High TAT Items: {3}
        
        Action Required: Please review procurement dashboard immediately.
        
        Dashboard: [Link to Dashboard]
    ", highTATPOA, highTATR31, highTATR37, totalHighTAT)
    
ElseIf totalHighTAT > 20 Then
    ' WARNING ALERT
    Log Message: "⚠️ WARNING: Elevated high TAT items detected: " + totalHighTAT.ToString()
    ' Send Teams notification
End If
```

### Example 3: Daily Metrics Report Bot

**Purpose:** Generate and email daily performance reports

```vb
'══════════════════════════════════════════════════════════
' DAILY METRICS REPORTING BOT
'══════════════════════════════════════════════════════════

' Load Metrics
Dim metricsJson As String = File.ReadAllText("uipath_metrics.json")
Dim metrics As JObject = JObject.Parse(metricsJson)

' Load Dashboard Data
Dim dashboardJson As String = File.ReadAllText("dashboard_data.json")
Dim dashboard As JObject = JObject.Parse(dashboardJson)

' Extract Key Metrics
Dim botRate As Double = metrics("process_metrics")("bot_automation_rate").ToObject(Of Double)
Dim conversionRate As Double = metrics("process_metrics")("pr_to_po_conversion").ToObject(Of Double)
Dim slaCompliance As Double = metrics("process_metrics")("sla_compliance")("poa_under_1day").ToObject(Of Double)

Dim totalPRs As Integer = dashboard("summary")("total_prs").ToObject(Of Integer)
Dim totalPOs As Integer = dashboard("summary")("total_pos").ToObject(Of Integer)
Dim totalPOAs As Integer = dashboard("summary")("total_poas").ToObject(Of Integer)

' Build Report HTML
Dim reportHTML As String = String.Format("
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .metric {{ background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .excellent {{ background: #d4edda; color: #155724; }}
        .good {{ background: #d1ecf1; color: #0c5460; }}
    </style>
</head>
<body>
    <h2>📊 Daily Procurement Metrics Report</h2>
    <p><strong>Date:</strong> {0}</p>
    
    <div class='metric excellent'>
        <h3>🤖 Bot Automation Rate</h3>
        <p style='font-size: 24px;'><strong>{1:F2}%</strong></p>
    </div>
    
    <div class='metric good'>
        <h3>📈 Process Volumes</h3>
        <p>Purchase Requisitions: <strong>{2:N0}</strong></p>
        <p>Purchase Orders: <strong>{3:N0}</strong></p>
        <p>Order Acknowledgements: <strong>{4:N0}</strong></p>
    </div>
    
    <div class='metric excellent'>
        <h3>⚡ SLA Compliance</h3>
        <p>POAs Under 1 Day: <strong>{5:F2}%</strong></p>
    </div>
    
    <div class='metric good'>
        <h3>🔄 Conversion Metrics</h3>
        <p>PR to PO Conversion: <strong>{6:F2}%</strong></p>
    </div>
    
    <hr>
    <p><em>Report generated by UiPath Bot at {0}</em></p>
</body>
</html>
", DateTime.Now.ToString("yyyy-MM-dd HH:mm"), botRate, totalPRs, totalPOs, totalPOAs, slaCompliance, conversionRate)

' Send Email Report
Send Outlook Mail
To: "management@company.com"
CC: "procurement.team@company.com"
Subject: "📊 Daily Procurement Metrics - " + DateTime.Now.ToString("yyyy-MM-dd")
Body: reportHTML
IsBodyHTML: True
```

---

## 🌐 API Endpoints (For Production)

### Base URL
```
https://your-dashboard-api.com/api
```

### Available Endpoints

#### 1. Get Summary Statistics
```http
GET /procurement/summary
```

**Response:**
```json
{
  "total_prs": 37331,
  "total_pos": 26583,
  "total_poas": 31135,
  "avg_tat_poa": 0.07,
  "bot_automation_rate": 99.99
}
```

#### 2. Get Pending POA Queue
```http
GET /procurement/poa/pending
```

**Query Parameters:**
- `limit` (optional): Number of items to return
- `priority` (optional): Filter by priority (high, normal, low)

**Response:**
```json
{
  "count": 150,
  "items": [
    {
      "po_number": "4400106893",
      "create_date": "2025-04-02",
      "tat_days": 0.5,
      "priority": "normal"
    },
    ...
  ]
}
```

#### 3. Complete POA Transaction
```http
POST /procurement/poa/complete
```

**Request Body:**
```json
{
  "po_number": "4400106893",
  "bot_id": "PR2PO-ACK2",
  "completion_time": "2025-04-02T14:30:00Z",
  "status": "success",
  "tat_hours": 2.5
}
```

#### 4. Get Release Queue
```http
GET /procurement/releases/queue
```

**Query Parameters:**
- `release_type`: "31" or "37"
- `status`: "pending", "processing", "completed"

#### 5. Real-time Metrics Feed
```http
GET /procurement/metrics/realtime
```

**WebSocket Support:** Yes
**Polling Interval:** 30 seconds recommended

#### 6. Webhook Configuration
```http
POST /webhook/procurement/alert
```

**Supported Events:**
- `high_tat_alert`: Triggered when TAT exceeds threshold
- `sla_breach`: Triggered when SLA is breached
- `process_complete`: Triggered when bot completes a batch
- `error_alert`: Triggered on processing errors

---

## 📊 Queue Management

### Queue Item Structure

```vb
' Queue Item Properties
Public Class ProcurementQueueItem
    Public Property TransactionID As String
    Public Property Type As String ' "POA", "Release31", "Release37"
    Public Property PONumber As String
    Public Property Priority As Integer ' 1=High, 2=Normal, 3=Low
    Public Property CreateDate As DateTime
    Public Property CurrentTAT As Double
    Public Property AssignedBot As String
    Public Property Status As String ' "New", "InProgress", "Completed", "Failed"
    Public Property RetryCount As Integer
End Class
```

### Priority Assignment Logic

```vb
Function AssignPriority(tat As Double) As Integer
    If tat > 2.0 Then
        Return 1 ' High Priority
    ElseIf tat > 1.0 Then
        Return 2 ' Normal Priority
    Else
        Return 3 ' Low Priority
    End If
End Function
```

---

## 📈 Performance Monitoring

### Key Metrics to Track

1. **Bot Processing Rate**
   - Transactions per hour
   - Average processing time
   - Success rate vs failure rate

2. **TAT Metrics**
   - Average TAT by process
   - TAT distribution
   - SLA compliance percentage

3. **Queue Health**
   - Queue depth
   - Aging items
   - High priority items

4. **Automation Rate**
   - BOT vs MANUAL processing
   - Automation percentage trend
   - Manual intervention triggers

### Orchestrator Dashboard Setup

```vb
' Update Orchestrator Assets
Set Asset: "POA_Processing_Rate" = processedCount / duration.TotalHours
Set Asset: "Current_Queue_Depth" = pendingCount
Set Asset: "Bot_Automation_Rate" = botRate
Set Asset: "Average_TAT" = avgTAT
Set Asset: "SLA_Compliance_Rate" = slaCompliance
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Issue 1: Cannot Read JSON Files
**Solution:**
```vb
' Ensure file exists and path is correct
If File.Exists("dashboard_data.json") Then
    Dim json As String = File.ReadAllText("dashboard_data.json")
Else
    Throw New Exception("File not found: dashboard_data.json")
End If
```

#### Issue 2: JSON Parsing Errors
**Solution:**
```vb
Try
    Dim data As JObject = JObject.Parse(jsonContent)
Catch ex As JsonException
    Log Message: "JSON Parse Error: " + ex.Message
    ' Use default values or retry
End Try
```

#### Issue 3: High TAT Items Not Processing
**Solution:**
- Check queue depth in `uipath_queue_data.json`
- Review bot capacity and concurrent executions
- Check for system errors in Orchestrator logs
- Verify data connectivity

#### Issue 4: API Connection Timeout
**Solution:**
```vb
' Increase timeout in HTTP Request Activity
Timeout: 60000 ' 60 seconds

' Implement retry logic
For retryCount = 1 To 3
    Try
        ' HTTP Request
        Exit For
    Catch ex As TimeoutException
        If retryCount = 3 Then
            Throw ex
        End If
        Delay 5000 ' Wait 5 seconds before retry
    End Try
Next
```

---

## 📞 Support

For integration support, contact:
- **Email:** support@yourcompany.com
- **Teams:** Procurement Automation Team
- **Documentation:** https://your-wiki.com/procurement-bot-integration

---

## 🚀 Next Steps

1. ✅ Download all data files from the outputs folder
2. ✅ Review UiPath bot examples
3. ✅ Test file access in UiPath Studio
4. ✅ Configure Orchestrator queues
5. ✅ Set up API endpoints (if using REST API)
6. ✅ Configure webhook alerts
7. ✅ Deploy bots to production
8. ✅ Monitor performance in dashboard

---

**Generated:** November 10, 2025
**Version:** 1.0
**Status:** ✅ Ready for Production
