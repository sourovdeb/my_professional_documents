#!/usr/bin/env python3
"""
Google Sheets Sync
===================
Bidirectional sync between Google Sheets and local CSV files.

Keeps your project tracking centralized in Google Sheets while maintaining
local CSV copies for automation scripts.

Usage:
    # Download from Google Sheets
    python3 sheets_sync.py --download --sheet "1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE" --tab "Essay Ideas"

    # Upload from local CSV
    python3 sheets_sync.py --upload --csv TRACKING/job_opportunities.csv --tab "Job Opportunities"

Setup:
    1. Create Google API credentials (OAuth2)
    2. Save to ~/.config/google_sheets_config.json
    3. Grant permissions to your Google Sheet
    4. Run with --download or --upload flags

Author: Sourov Deb
Last updated: 2026-06-02
"""

import csv
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import Google Sheets API
try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.colab import auth as colab_auth
    import gspread
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False
    logger.warning("⚠️  gspread not installed. Install with: pip install gspread google-auth-httplib2 google-auth-oauthlib")


class GoogleSheetsSync:
    """Syncs local CSV files with Google Sheets."""

    def __init__(self, sheet_id: str, config_path: Optional[str] = None):
        self.sheet_id = sheet_id
        self.gc = None
        self.sheet = None

        if HAS_GSPREAD:
            self._authenticate(config_path)

    def _authenticate(self, config_path: Optional[str] = None):
        """Authenticate with Google Sheets API."""
        if not HAS_GSPREAD:
            logger.error("gspread not available. Cannot authenticate.")
            return

        # Try service account (recommended)
        if config_path is None:
            config_path = os.path.expanduser('~/.config/google_sheets_config.json')

        if os.path.exists(config_path):
            try:
                logger.info(f"📝 Authenticating with service account: {config_path}")
                credentials = Credentials.from_service_account_file(
                    config_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets',
                            'https://www.googleapis.com/auth/drive']
                )
                self.gc = gspread.Authorized(auth=credentials)
                self.sheet = self.gc.open_by_key(self.sheet_id)
                logger.info("✅ Authenticated successfully")
            except Exception as e:
                logger.error(f"❌ Authentication failed: {e}")
                logger.info("💡 Get Google API credentials: https://console.cloud.google.com/apis/credentials")
        else:
            logger.warning(f"⚠️  Config file not found: {config_path}")
            logger.info("💡 Save Google API credentials to: ~/.config/google_sheets_config.json")

    def download_tab(self, tab_name: str) -> List[Dict]:
        """Download a tab from Google Sheets."""
        if not self.sheet:
            logger.error("❌ Not authenticated. Cannot download.")
            return []

        try:
            logger.info(f"📥 Downloading tab: {tab_name}")
            worksheet = self.sheet.worksheet(tab_name)
            records = worksheet.get_all_records()
            logger.info(f"✅ Downloaded {len(records)} rows")
            return records
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            return []

    def upload_tab(self, tab_name: str, data: List[Dict]) -> bool:
        """Upload data to a Google Sheets tab."""
        if not self.sheet:
            logger.error("❌ Not authenticated. Cannot upload.")
            return False

        try:
            logger.info(f"📤 Uploading to tab: {tab_name}")

            # Get or create worksheet
            try:
                worksheet = self.sheet.worksheet(tab_name)
                worksheet.clear()
            except gspread.exceptions.WorksheetNotFound:
                logger.info(f"  Creating new tab: {tab_name}")
                worksheet = self.sheet.add_worksheet(title=tab_name, rows=len(data) + 10, cols=len(data[0]) if data else 10)

            if data:
                # Write headers
                headers = list(data[0].keys())
                worksheet.append_row(headers)

                # Write rows
                for row_data in data:
                    row = [row_data.get(h, '') for h in headers]
                    worksheet.append_row(row)

                logger.info(f"✅ Uploaded {len(data)} rows to {tab_name}")
                return True
            else:
                logger.warning("⚠️  No data to upload")
                return False

        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")
            return False

    def export_to_csv(self, tab_name: str, output_path: str) -> bool:
        """Download Google Sheets tab and save as CSV."""
        records = self.download_tab(tab_name)

        if not records:
            logger.error(f"❌ No data to export from {tab_name}")
            return False

        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)

            logger.info(f"✅ Exported to CSV: {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return False

    def import_from_csv(self, csv_path: str, tab_name: str) -> bool:
        """Load CSV file and upload to Google Sheets tab."""
        if not os.path.exists(csv_path):
            logger.error(f"❌ CSV file not found: {csv_path}")
            return False

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)

            if not data:
                logger.warning(f"⚠️  CSV is empty: {csv_path}")
                return False

            logger.info(f"📤 Importing {len(data)} rows from {csv_path}")
            return self.upload_tab(tab_name, data)

        except Exception as e:
            logger.error(f"❌ Import failed: {e}")
            return False


class SyncManager:
    """Manages multiple syncs with configuration."""

    def __init__(self, sheet_id: str, config_file: Optional[str] = None):
        self.sheet_id = sheet_id
        self.syncer = GoogleSheetsSync(sheet_id)
        self.config = self._load_config(config_file)

    def _load_config(self, config_file: Optional[str] = None) -> Dict:
        """Load sync configuration."""
        if config_file is None:
            config_file = 'tools/google_sheets_sync/sync_config.json'

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return {}
        else:
            logger.warning(f"Config file not found: {config_file}")
            return {}

    def sync_all(self, direction: str = 'both'):
        """Sync all configured sheets."""
        logger.info(f"🔄 Starting sync (direction: {direction})")

        if not self.config:
            logger.warning("No sync configuration. Create sync_config.json")
            return

        syncs = self.config.get('syncs', [])

        for sync in syncs:
            sheet_tab = sync.get('sheet_tab')
            csv_file = sync.get('csv_file')
            sync_dir = sync.get('direction', 'both')

            logger.info(f"\n📋 Syncing: {sheet_tab} ↔ {csv_file}")

            if sync_dir in ['download', 'both']:
                self.syncer.export_to_csv(sheet_tab, csv_file)

            if sync_dir in ['upload', 'both']:
                self.syncer.import_from_csv(csv_file, sheet_tab)

        logger.info("\n✅ Sync complete!")

    def sync_one(self, sheet_tab: str, csv_file: str, direction: str = 'both'):
        """Sync a single sheet."""
        logger.info(f"🔄 Syncing: {sheet_tab} ↔ {csv_file}")

        if direction in ['download', 'both']:
            self.syncer.export_to_csv(sheet_tab, csv_file)

        if direction in ['upload', 'both']:
            self.syncer.import_from_csv(csv_file, sheet_tab)

        logger.info("✅ Sync complete!")


def create_default_config(output_file: str = 'tools/google_sheets_sync/sync_config.json'):
    """Create a default sync configuration."""
    config = {
        "sheet_id": "1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE",
        "syncs": [
            {
                "sheet_tab": "Essay Ideas",
                "csv_file": "TRACKING/essay_ideas.csv",
                "direction": "both"
            },
            {
                "sheet_tab": "Job Opportunities",
                "csv_file": "TRACKING/job_opportunities.csv",
                "direction": "both"
            },
            {
                "sheet_tab": "Contacts Discovered",
                "csv_file": "TRACKING/contacts_discovered.csv",
                "direction": "both"
            },
            {
                "sheet_tab": "Publishing Calendar",
                "csv_file": "TRACKING/publishing_tracker.csv",
                "direction": "both"
            },
            {
                "sheet_tab": "Health Tracking",
                "csv_file": "TRACKING/health_log.csv",
                "direction": "both"
            }
        ]
    }

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)

    logger.info(f"✅ Created config: {output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Sync with Google Sheets')
    parser.add_argument('--sheet', type=str, default='1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE',
                        help='Google Sheet ID')
    parser.add_argument('--download', action='store_true', help='Download from Google Sheets')
    parser.add_argument('--upload', action='store_true', help='Upload to Google Sheets')
    parser.add_argument('--tab', type=str, help='Sheet tab name')
    parser.add_argument('--csv', type=str, help='Local CSV file')
    parser.add_argument('--sync-all', action='store_true', help='Sync all configured sheets')
    parser.add_argument('--init-config', action='store_true', help='Create default config')

    args = parser.parse_args()

    if args.init_config:
        create_default_config()
        return

    if args.sync_all:
        manager = SyncManager(args.sheet)
        manager.sync_all()
        return

    if not args.tab or not args.csv:
        logger.error("❌ Provide --tab and --csv")
        return

    syncer = GoogleSheetsSync(args.sheet)

    if args.download:
        syncer.export_to_csv(args.tab, args.csv)

    if args.upload:
        syncer.import_from_csv(args.csv, args.tab)

    if not args.download and not args.upload:
        logger.info("💡 Use --download or --upload flag")


if __name__ == '__main__':
    main()
