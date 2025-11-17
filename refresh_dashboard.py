#!/usr/bin/env python3
"""
🔄 PROCUREMENT DASHBOARD - DAILY REFRESH SCRIPT
================================================

This script automatically updates your dashboard with new data.

USAGE:
    1. Place new Consolidated.xlsx in the same folder as this script
    2. Run: python refresh_dashboard.py
    3. Done! Dashboard is updated with fresh data

The script will:
    ✅ Process all 5 procurement processes
    ✅ Calculate TAT metrics
    ✅ Generate UiPath integration files
    ✅ Update the dashboard HTML
    ✅ Create backup of old data
"""

import pandas as pd
import json
import os
from datetime import datetime
import shutil
import numpy as np

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

# Custom JSON encoder for numpy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def backup_existing_files():
    """Create backup of existing files before updating"""
    print_info("Creating backup of existing files...")
    
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    files_to_backup = [
        'dashboard_data.json',
        'uipath_queue_data.json',
        'uipath_metrics.json',
        'procurement_dashboard.html'
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(backup_dir, file))
    
    print_success(f"Backup created in: {backup_dir}")
    return backup_dir

def process_procurement_data(excel_file):
    """Process the consolidated Excel file"""
    print_header("📊 PROCESSING PROCUREMENT DATA")
    
    if not os.path.exists(excel_file):
        print_error(f"File not found: {excel_file}")
        print_info("Please ensure 'Consolidated.xlsx' is in the same folder as this script")
        return None
    
    print_info(f"Reading file: {excel_file}")
    
    try:
        # Read all sheets
        xls = pd.ExcelFile(excel_file)
        print_success(f"File loaded successfully!")
        print_info(f"Found {len(xls.sheet_names)} sheets")
        
        # 1. PR CREATE
        print_info("Processing PR Create data...")
        df_pr = pd.read_excel(excel_file, sheet_name='PR Create')
        pr_stats = {
            'total': int(len(df_pr)),
            'by_type': {k: int(v) for k, v in df_pr['Req Type'].value_counts().to_dict().items()},
            'by_purchase_group': {k: int(v) for k, v in df_pr['PGr'].value_counts().head(10).to_dict().items()},
            'by_month': {k: int(v) for k, v in df_pr['Month'].value_counts().to_dict().items()},
            'by_status': {k: int(v) for k, v in df_pr['S'].value_counts().to_dict().items()}
        }
        print_success(f"PR Create: {len(df_pr):,} records processed")
        
        # 2. PO CREATE
        print_info("Processing PO Create data...")
        df_po = pd.read_excel(excel_file, sheet_name='PO Create')
        po_stats = {
            'total': int(len(df_po)),
            'by_type': {k: int(v) for k, v in df_po['Type Description'].value_counts().to_dict().items()},
            'by_purchase_group': {k: int(v) for k, v in df_po['PGr'].value_counts().head(10).to_dict().items()},
            'conversion_rate': round((len(df_po) / len(df_pr)) * 100, 2)
        }
        print_success(f"PO Create: {len(df_po):,} records processed")
        
        # 3. POA (Order Acknowledgements)
        print_info("Processing POA data...")
        df_poa = pd.read_excel(excel_file, sheet_name='Order Acknowledgements 1 April ')
        tat_poa = df_poa['Turn around in Days'].dropna()
        
        poa_stats = {
            'total': int(len(df_poa)),
            'avg_tat': round(float(tat_poa.mean()), 2),
            'median_tat': round(float(tat_poa.median()), 2),
            'max_tat': round(float(tat_poa.max()), 2),
            'min_tat': round(float(tat_poa.min()), 2),
            'by_processing_type': {k: int(v) for k, v in df_poa['BOT/MANUAL/SERVICE PROVIDER'].value_counts().to_dict().items()},
            'by_month': {k: int(v) for k, v in df_poa['Month'].value_counts().to_dict().items()},
            'tat_distribution': {
                '0-1 days': int(len(tat_poa[tat_poa <= 1])),
                '1-2 days': int(len(tat_poa[(tat_poa > 1) & (tat_poa <= 2)])),
                '2-3 days': int(len(tat_poa[(tat_poa > 2) & (tat_poa <= 3)])),
                '3+ days': int(len(tat_poa[tat_poa > 3]))
            }
        }
        print_success(f"POA: {len(df_poa):,} records | Avg TAT: {poa_stats['avg_tat']} days")
        
        # 4. RELEASE 31
        print_info("Processing Release 31 data...")
        df_r31 = pd.read_excel(excel_file, sheet_name='PO Release 31')
        df_r31['Created On'] = pd.to_datetime(df_r31['Created On'])
        df_r31['Date(31)'] = pd.to_datetime(df_r31['Date(31)'], format='%Y/%m/%d')
        df_r31['TAT_31'] = (df_r31['Date(31)'] - df_r31['Created On']).dt.total_seconds() / 86400
        tat_r31 = df_r31['TAT_31'].dropna()
        
        r31_stats = {
            'total': int(len(df_r31)),
            'avg_tat': round(float(tat_r31.mean()), 2),
            'median_tat': round(float(tat_r31.median()), 2),
            'same_day_percentage': round((len(tat_r31[tat_r31 <= 1]) / len(tat_r31)) * 100, 2),
            'tat_distribution': {
                'Same day (0-1)': int(len(tat_r31[tat_r31 <= 1])),
                '1-2 days': int(len(tat_r31[(tat_r31 > 1) & (tat_r31 <= 2)])),
                '2-3 days': int(len(tat_r31[(tat_r31 > 2) & (tat_r31 <= 3)])),
                '3+ days': int(len(tat_r31[tat_r31 > 3]))
            }
        }
        print_success(f"Release 31: {len(df_r31):,} records | Avg TAT: {r31_stats['avg_tat']} days")
        
        # 5. RELEASE 37
        print_info("Processing Release 37 data...")
        df_r37 = pd.read_excel(excel_file, sheet_name='PO Release 37')
        df_r37['Created On'] = pd.to_datetime(df_r37['Created On'])
        df_r37['Date(37)'] = pd.to_datetime(df_r37['Date(37)'], format='%Y/%m/%d')
        df_r37['TAT_37'] = (df_r37['Date(37)'] - df_r37['Created On']).dt.total_seconds() / 86400
        tat_r37 = df_r37['TAT_37'].dropna()
        
        r37_stats = {
            'total': int(len(df_r37)),
            'avg_tat': round(float(tat_r37.mean()), 2),
            'median_tat': round(float(tat_r37.median()), 2),
            'same_day_percentage': round((len(tat_r37[tat_r37 <= 1]) / len(tat_r37)) * 100, 2),
            'by_purchase_group': {k: int(v) for k, v in df_r37['Purchasing Group'].value_counts().head(10).to_dict().items()},
            'tat_distribution': {
                'Same day (0-1)': int(len(tat_r37[tat_r37 <= 1])),
                '1-2 days': int(len(tat_r37[(tat_r37 > 1) & (tat_r37 <= 2)])),
                '2-3 days': int(len(tat_r37[(tat_r37 > 2) & (tat_r37 <= 3)])),
                '3+ days': int(len(tat_r37[tat_r37 > 3]))
            }
        }
        print_success(f"Release 37: {len(df_r37):,} records | Avg TAT: {r37_stats['avg_tat']} days")
        
        # Compile all data
        dashboard_data = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_prs': pr_stats['total'],
                'total_pos': po_stats['total'],
                'total_poas': poa_stats['total'],
                'total_releases_31': r31_stats['total'],
                'total_releases_37': r37_stats['total'],
                'avg_tat_poa': poa_stats['avg_tat'],
                'avg_tat_release_31': r31_stats['avg_tat'],
                'avg_tat_release_37': r37_stats['avg_tat']
            },
            'pr_create': pr_stats,
            'po_create': po_stats,
            'poa': poa_stats,
            'release_31': r31_stats,
            'release_37': r37_stats
        }
        
        # Save dashboard data
        print_info("Saving dashboard data...")
        with open('dashboard_data.json', 'w') as f:
            json.dump(dashboard_data, f, indent=2, cls=NumpyEncoder)
        print_success("Dashboard data saved!")
        
        # Create UiPath integration files
        print_header("🤖 GENERATING UIPATH INTEGRATION FILES")
        
        # Queue data
        print_info("Creating queue data...")
        uipath_queue_data = {
            'pending_poas': int(len(df_poa[df_poa['BOT/MANUAL/SERVICE PROVIDER'] == 'BOT'])),
            'manual_poas': int(len(df_poa[df_poa['BOT/MANUAL/SERVICE PROVIDER'] == 'MANUAL'])),
            'pending_releases': int(len(df_r31)),
            'high_tat_poas': int(len(tat_poa[tat_poa > 2])),
            'high_tat_r31': int(len(tat_r31[tat_r31 > 2])),
            'high_tat_r37': int(len(tat_r37[tat_r37 > 2]))
        }
        
        with open('uipath_queue_data.json', 'w') as f:
            json.dump(uipath_queue_data, f, indent=2)
        print_success("Queue data created")
        
        # Metrics
        print_info("Creating metrics data...")
        uipath_metrics = {
            'process_metrics': {
                'pr_to_po_conversion': po_stats['conversion_rate'],
                'bot_automation_rate': round((poa_stats['by_processing_type'].get('BOT', 0) / poa_stats['total']) * 100, 2),
                'avg_processing_time': {
                    'poa': poa_stats['avg_tat'],
                    'release_31': r31_stats['avg_tat'],
                    'release_37': r37_stats['avg_tat']
                },
                'sla_compliance': {
                    'poa_under_1day': round((poa_stats['tat_distribution']['0-1 days'] / poa_stats['total']) * 100, 2),
                    'release_31_same_day': r31_stats['same_day_percentage'],
                    'release_37_same_day': r37_stats['same_day_percentage']
                }
            }
        }
        
        with open('uipath_metrics.json', 'w') as f:
            json.dump(uipath_metrics, f, indent=2)
        print_success("Metrics data created")
        
        # CSV exports
        print_info("Exporting CSV files...")
        df_poa.to_csv('uipath_poa_data.csv', index=False)
        df_r31.to_csv('uipath_r31_data.csv', index=False)
        df_r37.to_csv('uipath_r37_data.csv', index=False)
        print_success("CSV files exported")
        
        print_header("📈 PROCESSING SUMMARY")
        print(f"{Colors.BOLD}Total Records Processed: {Colors.GREEN}{pr_stats['total'] + po_stats['total'] + poa_stats['total'] + r31_stats['total'] + r37_stats['total']:,}{Colors.END}")
        print(f"{Colors.BOLD}Bot Automation Rate: {Colors.GREEN}{uipath_metrics['process_metrics']['bot_automation_rate']}%{Colors.END}")
        print(f"{Colors.BOLD}Average TAT: {Colors.GREEN}{poa_stats['avg_tat']} days{Colors.END}")
        print(f"{Colors.BOLD}SLA Compliance: {Colors.GREEN}{uipath_metrics['process_metrics']['sla_compliance']['poa_under_1day']}%{Colors.END}")
        
        return dashboard_data
        
    except Exception as e:
        print_error(f"Error processing data: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def update_dashboard_html(dashboard_data):
    """Update the dashboard HTML with new data"""
    print_header("🌐 UPDATING DASHBOARD HTML")
    
    if not os.path.exists('procurement_dashboard.html'):
        print_warning("Dashboard HTML not found. Please ensure 'procurement_dashboard.html' is in the same folder.")
        return False
    
    print_info("Reading dashboard template...")
    with open('procurement_dashboard.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and replace the data
    print_info("Injecting new data...")
    
    # Look for the data placeholder or existing data
    data_json = json.dumps(dashboard_data, indent=2, cls=NumpyEncoder)
    
    # Replace the data in the script section
    if 'const dashboardData = {' in html_content:
        # Find the start and end of the dashboardData object
        start_marker = 'const dashboardData = '
        end_marker = '        // Initialize dashboard'
        
        start_idx = html_content.find(start_marker)
        end_idx = html_content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            # Get everything before the data
            before = html_content[:start_idx + len(start_marker)]
            # Get everything after the data
            after = html_content[end_idx:]
            # Combine with new data
            html_content = before + data_json + ';\n\n' + after
        else:
            print_error("Could not find data section in HTML")
            return False
    else:
        print_error("Dashboard structure not recognized")
        return False
    
    # Write the updated HTML
    print_info("Saving updated dashboard...")
    with open('procurement_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print_success("Dashboard HTML updated successfully!")
    return True

def main():
    """Main execution function"""
    print_header("🏭 PROCUREMENT DASHBOARD - DAILY REFRESH")
    print(f"{Colors.CYAN}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")
    
    # Check for Excel file
    excel_file = 'Consolidated.xlsx'
    
    if not os.path.exists(excel_file):
        print_error(f"Excel file not found: {excel_file}")
        print_info("Please place your 'Consolidated.xlsx' file in the same folder as this script")
        print_info(f"Current directory: {os.getcwd()}")
        return
    
    # Create backup
    backup_dir = backup_existing_files()
    
    # Process data
    dashboard_data = process_procurement_data(excel_file)
    
    if dashboard_data is None:
        print_error("Failed to process data. Dashboard not updated.")
        return
    
    # Update HTML
    success = update_dashboard_html(dashboard_data)
    
    if success:
        print_header("✅ REFRESH COMPLETE")
        print(f"{Colors.GREEN}{Colors.BOLD}Your dashboard has been updated with fresh data!{Colors.END}")
        print(f"\n{Colors.CYAN}What's been updated:{Colors.END}")
        print(f"  ✅ Dashboard HTML with new visualizations")
        print(f"  ✅ JSON data files for UiPath integration")
        print(f"  ✅ CSV exports for bot processing")
        print(f"  ✅ Performance metrics and queue data")
        print(f"\n{Colors.CYAN}Backup location:{Colors.END} {backup_dir}")
        print(f"\n{Colors.BOLD}Next step:{Colors.END} Open 'procurement_dashboard.html' in your browser to see the updated dashboard!")
    else:
        print_error("Failed to update dashboard HTML")
        print_info(f"Your data has been processed and saved as JSON files")
        print_info(f"You can restore from backup: {backup_dir}")
    
    print(f"\n{Colors.CYAN}Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Process interrupted by user{Colors.END}")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
