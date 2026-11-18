"""
HAZARDX AI - Safe Project Cleanup Executor
Moves confirmed redundant root files and historical single-hazard prototype scripts
into _archive/, preserving folder structure, and generates _archive/CLEANUP_MANIFEST.md.
"""

import os
import shutil

ARCHIVE_DIR = '_archive'
MANIFEST_PATH = os.path.join(ARCHIVE_DIR, 'CLEANUP_MANIFEST.md')

CLEANUP_OPERATIONS = [
    # 1. Redundant root reports (outdated duplicates of canonical reports in reports/)
    {
        'src': 'DATASET_INTEGRATION_REPORT.md',
        'dest': '_archive/root/DATASET_INTEGRATION_REPORT.md',
        'reason': 'Outdated early snapshot (4.1 KB); full canonical report is maintained at reports/DATASET_INTEGRATION_REPORT.md (5.5 KB).'
    },
    {
        'src': 'DATASET_INVENTORY.md',
        'dest': '_archive/root/DATASET_INVENTORY.md',
        'reason': 'Outdated early snapshot (6.0 KB); canonical report maintained at reports/DATASET_INVENTORY.md (8.2 KB).'
    },
    {
        'src': 'DATASET_METADATA.json',
        'dest': '_archive/root/DATASET_METADATA.json',
        'reason': 'Outdated early snapshot (2.4 KB); canonical report maintained at reports/DATASET_METADATA.json (3.7 KB).'
    },
    {
        'src': 'DATASET_REPORT.md',
        'dest': '_archive/root/DATASET_REPORT.md',
        'reason': 'Outdated early snapshot (18.5 KB); full 5-hazard catalog report maintained at reports/DATASET_REPORT.md (21.6 KB).'
    },
    {
        'src': 'DATASET_SUITABILITY_REPORT.md',
        'dest': '_archive/root/DATASET_SUITABILITY_REPORT.md',
        'reason': 'Outdated early snapshot (11.7 KB); canonical report maintained at reports/DATASET_SUITABILITY_REPORT.md (14.6 KB).'
    },
    {
        'src': 'DATA_COLLECTION_REPORT.md',
        'dest': '_archive/root/DATA_COLLECTION_REPORT.md',
        'reason': 'Redundant root duplicate; canonical report maintained at reports/DATA_COLLECTION_REPORT.md.'
    },
    {
        'src': 'DATA_QUALITY_REPORT.md',
        'dest': '_archive/root/DATA_QUALITY_REPORT.md',
        'reason': 'Outdated early snapshot (3.8 KB); complete data quality report maintained at reports/DATA_QUALITY_REPORT.md (10.5 KB).'
    },
    {
        'src': 'DATA_READINESS_MATRIX.md',
        'dest': '_archive/root/DATA_READINESS_MATRIX.md',
        'reason': 'Outdated early snapshot (5.2 KB); updated 6-stage maturity report maintained at reports/DATA_READINESS_MATRIX.md (6.3 KB).'
    },
    {
        'src': 'DATA_SOURCE_REGISTER.csv',
        'dest': '_archive/root/DATA_SOURCE_REGISTER.csv',
        'reason': 'Outdated early snapshot (2.6 KB); canonical register maintained at reports/DATA_SOURCE_REGISTER.csv (3.2 KB).'
    },
    {
        'src': 'EDA_REPORT.md',
        'dest': '_archive/root/EDA_REPORT.md',
        'reason': 'Outdated early snapshot (3.5 KB); comprehensive EDA report maintained at reports/EDA_REPORT.md (4.9 KB).'
    },
    
    # 2. Historical single-hazard prototype scripts (superseded by scripts/data_collection/ and scripts/ml_prep/)
    {
        'src': 'scripts/audit_and_process_earthquakes.py',
        'dest': '_archive/scripts/audit_and_process_earthquakes.py',
        'reason': 'Historical prototype for Earthquake EDA; superseded by scripts/data_collection/download_earthquake_data.py and scripts/ml_prep/build_earthquake_dataset.py.'
    },
    {
        'src': 'scripts/audit_landslides.py',
        'dest': '_archive/scripts/audit_landslides.py',
        'reason': 'Historical prototype for Landslide inspection; superseded by scripts/eda/run_full_eda.py and scripts/ml_prep/build_landslide_dataset.py.'
    },
    {
        'src': 'scripts/download_all_earthquakes.py',
        'dest': '_archive/scripts/download_all_earthquakes.py',
        'reason': 'Historical batch downloader script; superseded by scripts/data_collection/download_earthquake_data.py.'
    },
    {
        'src': 'scripts/download_earthquakes.py',
        'dest': '_archive/scripts/download_earthquakes.py',
        'reason': 'Initial test downloader for USGS API; superseded by scripts/data_collection/download_earthquake_data.py.'
    },
    {
        'src': 'scripts/process_floods.py',
        'dest': '_archive/scripts/process_floods.py',
        'reason': 'Initial test processor for DFO shapefiles; superseded by scripts/data_collection/download_flood_data.py and scripts/ml_prep/build_flood_dataset.py.'
    },
    {
        'src': 'scripts/process_landslides.py',
        'dest': '_archive/scripts/process_landslides.py',
        'reason': 'Initial test processor for NASA GLC; superseded by scripts/data_collection/download_landslide_data.py and scripts/ml_prep/build_landslide_dataset.py.'
    }
]

def main():
    print("Executing safe project cleanup...")
    manifest_rows = []
    
    for item in CLEANUP_OPERATIONS:
        src = item['src']
        dest = item['dest']
        reason = item['reason']
        
        if os.path.exists(src):
            dest_dir = os.path.dirname(dest)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src, dest)
            print(f"Moved: {src} -> {dest}")
            manifest_rows.append({
                'src': src,
                'dest': dest,
                'reason': reason,
                'status': 'MOVED'
            })
        else:
            print(f"Source not found (skipped): {src}")
            manifest_rows.append({
                'src': src,
                'dest': dest,
                'reason': reason,
                'status': 'NOT_FOUND'
            })
            
    # Write CLEANUP_MANIFEST.md
    lines = []
    lines.append("# HAZARDX AI — Safe Project Cleanup Manifest")
    lines.append("## Archived Files, Relocation Mapping, and Rationale\n")
    lines.append("**Date of Cleanup:** 2026-11-17  ")
    lines.append("**Integrity Guarantee:** Zero files permanently deleted. All archived files preserved with original structures under `_archive/`.\n")
    lines.append("---\n")
    lines.append("## 1. Archive Manifest Table\n")
    lines.append("| Original Path | New Archive Path | Status | Reason for Archiving |")
    lines.append("| :--- | :--- | :---: | :--- |")
    
    for r in manifest_rows:
        lines.append(f"| `{r['src']}` | `{r['dest']}` | **{r['status']}** | {r['reason']} |")
        
    lines.append("\n---\n")
    lines.append("## 2. Recovery Instructions")
    lines.append("To restore any archived file to its original location, move it back using its relative path:")
    lines.append("```bash")
    lines.append("# Example: Restoring an archived script")
    lines.append("mv _archive/scripts/download_earthquakes.py scripts/download_earthquakes.py")
    lines.append("```\n")
    
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Saved cleanup manifest to {MANIFEST_PATH}")

if __name__ == '__main__':
    main()

