#!/usr/bin/env python3
# Guest Book Application - Data Handler
# This file contains the data handling logic for the guest book application.

import json
import os
import datetime
from pathlib import Path

class DataHandler:
    """Handles all data operations for the guest book application"""
    
    def __init__(self, file_path="guestbook_data.json"):
        """Initialize the data handler with the specified file path"""
        self.file_path = file_path
        self.entries = []
        self.load_data()
    
    def load_data(self):
        """Load guest book entries from the JSON file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    self.entries = json.load(file)
            else:
                self.entries = []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data: {e}")
            self.entries = []
    
    def save_data(self):
        """Save guest book entries to the JSON file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.entries, file, indent=4)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False
    
    def add_entry(self, name, message, date=None):
        """Add a new guest book entry"""
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = {
            "id": len(self.entries) + 1,
            "name": name,
            "message": message,
            "date": date
        }
        
        self.entries.append(entry)
        return self.save_data()
    
    def get_all_entries(self):
        """Return all guest book entries"""
        return self.entries
    
    def search_entries(self, query):
        """Search for entries containing the query in name or message"""
        query = query.lower()
        results = []
        
        for entry in self.entries:
            if (query in entry['name'].lower() or 
                query in entry['message'].lower()):
                results.append(entry)
        
        return results
    
    def filter_by_date(self, start_date, end_date=None):
        """Filter entries by date range"""
        try:
            # Convert string dates to datetime objects for comparison
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            
            if end_date:
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end = end.replace(hour=23, minute=59, second=59)  # End of day
            else:
                end = datetime.datetime.now()
            
            results = []
            for entry in self.entries:
                entry_date = datetime.datetime.strptime(entry['date'].split()[0], "%Y-%m-%d")
                if start <= entry_date <= end:
                    results.append(entry)
            
            return results
        except ValueError as e:
            print(f"Date format error: {e}")
            return []
    
    def delete_entry(self, entry_id):
        """Delete an entry by its ID"""
        for i, entry in enumerate(self.entries):
            if entry['id'] == entry_id:
                del self.entries[i]
                return self.save_data()
        return False
    
    def export_to_csv(self, file_path):
        """Export all entries to a CSV file"""
        import csv
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(['ID', 'Name', 'Date', 'Message'])
                # Write data
                for entry in self.entries:
                    writer.writerow([
                        entry['id'],
                        entry['name'],
                        entry['date'],
                        entry['message']
                    ])
            return True
        except IOError as e:
            print(f"Error exporting to CSV: {e}")
            return False
