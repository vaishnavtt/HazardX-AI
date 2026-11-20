"""
HAZARDX AI — Repository Consolidation and Cleanup Script (Phase 9)
Safely cleans up obsolete phase-by-phase reports and development clutter,
preserving the 5 canonical consolidated reports, model artifacts, datasets, and tests.
"""

import os
import shutil
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")

CANONICAL_REPORTS = {
    "SCIENTIFIC_VALIDATION.md",
    "MODEL_EVALUATION.md",
    "API_AND_DATA_QUALITY.md",
    "FINAL_RELEASE_VERIFICATION.md",
    "PROJECT_CLEANUP_SUMMARY.md"
}

PRESERVED_DIRS = {"figures", "e2e_screenshots"}

def cleanup_reports():
    print("=" * 80)
    print("HAZARDX AI — REPOSITORY CONSOLIDATION & CLEANUP")
    print("=" * 80)

    # 1. Create root screenshots directory and copy genuine screenshots
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    src_images = os.path.join(ROOT_DIR, "docs", "images")
    if os.path.exists(src_images):
        for img in os.listdir(src_images):
            src_f = os.path.join(src_images, img)
            dst_f = os.path.join(SCREENSHOTS_DIR, img)
            if os.path.isfile(src_f):
                shutil.copy2(src_f, dst_f)
        print(f"[1/4] Preserved screenshots in {SCREENSHOTS_DIR} ({len(os.listdir(SCREENSHOTS_DIR))} images).")

    # 2. Remove obsolete phase subdirectories in reports/
    removed_dirs = 0
    for item in os.listdir(REPORTS_DIR):
        p = os.path.join(REPORTS_DIR, item)
        if os.path.isdir(p) and item not in PRESERVED_DIRS:
            shutil.rmtree(p)
            removed_dirs += 1
    print(f"[2/4] Removed {removed_dirs} obsolete phase and execution report subdirectories in reports/.")

    # 3. Remove obsolete loose phase markdown and json files in reports/
    removed_files = 0
    for item in os.listdir(REPORTS_DIR):
        p = os.path.join(REPORTS_DIR, item)
        if os.path.isfile(p) and item not in CANONICAL_REPORTS:
            os.remove(p)
            removed_files += 1
    print(f"[3/4] Removed {removed_files} obsolete loose phase reports/data logs in reports/.")

    # 4. Verify canonical reports
    remaining = os.listdir(REPORTS_DIR)
    print(f"[4/4] Remaining items in reports/: {remaining}")
    assert CANONICAL_REPORTS.issubset(set(remaining)), "Error: Canonical reports were lost!"
    print("\nCleanup completed successfully! Reports directory is now clean and canonical.")

if __name__ == "__main__":
    cleanup_reports()
