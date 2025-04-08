#!/usr/bin/env python3
# Guest Book Application - GUI
# This file contains the GUI implementation for the guest book application.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
from data_handler import DataHandler
import os

class GuestBookApp:
    """Main application class for the Guest Book"""
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title("Guest Book Application")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Set app icon using Unicode character (instead of an image file)
        self.root.iconbitmap("")  # Using default
        
        # Initialize data handler
        self.data_handler = DataHandler()
        
        # Setup GUI components
        self.setup_ui()
        
        # Load initial data
        self.refresh_entries()
    
    def setup_ui(self):
        """Set up the user interface"""
        self.create_menu()
        self.create_main_frame()
        self.create_entry_form()
        self.create_entries_display()
        self.create_search_filter()
        self.create_status_bar()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Guest Book", command=self.new_guestbook)
        file_menu.add_command(label="Open Guest Book", command=self.open_guestbook)
        file_menu.add_command(label="Save As...", command=self.save_guestbook_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear All Entries", command=self.clear_all_entries)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_main_frame(self):
        """Create the main frame that will contain all widgets"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid layout
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)  # Entry form
        self.main_frame.rowconfigure(1, weight=0)  # Search filter
        self.main_frame.rowconfigure(2, weight=1)  # Entries display
    
    def create_entry_form(self):
        """Create form for adding new entries"""
        # Create a frame for the form
        form_frame = ttk.LabelFrame(self.main_frame, text="Add New Entry", padding="10")
        form_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure grid layout
        form_frame.columnconfigure(0, weight=0)  # Labels
        form_frame.columnconfigure(1, weight=1)  # Entry fields
        form_frame.columnconfigure(2, weight=0)  # Date label
        form_frame.columnconfigure(3, weight=1)  # Date field
        
        # Name field
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Date field
        ttk.Label(form_frame, text="Date:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(form_frame, textvariable=self.date_var)
        date_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        
        # Message field
        ttk.Label(form_frame, text="Message:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.message_text = tk.Text(form_frame, height=3, width=50)
        self.message_text.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Add button
        add_button = ttk.Button(form_frame, text="Add Entry", command=self.add_entry)
        add_button.grid(row=2, column=3, sticky="e", padx=5, pady=5)
        
        # Make Enter key submit the form when in name field
        name_entry.bind('<Return>', lambda event: self.add_entry())
    
    def create_search_filter(self):
        """Create search and filter controls"""
        search_frame = ttk.Frame(self.main_frame, padding="5")
        search_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Search field
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Search button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_entries)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Filter by date elements
        ttk.Label(search_frame, text="Filter by date:").pack(side=tk.LEFT, padx=(20, 5))
        self.filter_start_var = tk.StringVar()
        filter_start_entry = ttk.Entry(search_frame, textvariable=self.filter_start_var, width=10)
        filter_start_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="to").pack(side=tk.LEFT)
        self.filter_end_var = tk.StringVar()
        filter_end_entry = ttk.Entry(search_frame, textvariable=self.filter_end_var, width=10)
        filter_end_entry.pack(side=tk.LEFT, padx=5)
        
        # Filter button
        filter_button = ttk.Button(search_frame, text="Filter", command=self.filter_entries)
        filter_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_button = ttk.Button(search_frame, text="Reset", command=self.refresh_entries)
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Make Enter key trigger search when in search field
        search_entry.bind('<Return>', lambda event: self.search_entries())
    
    def create_entries_display(self):
        """Create the area to display all guest book entries"""
        # Create a frame for the entries
        display_frame = ttk.LabelFrame(self.main_frame, text="Guest Book Entries", padding="10")
        display_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add a treeview with scrollbars
        self.tree = ttk.Treeview(display_frame, columns=("id", "name", "date", "message"), show="headings")
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("message", text="Message")
        
        # Configure column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=150)
        self.tree.column("date", width=120)
        self.tree.column("message", width=400)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Place elements in grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid layout
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Add right-click context menu
        self.create_context_menu()
    
    def create_context_menu(self):
        """Create context menu for treeview"""
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Delete Entry", command=self.delete_selected_entry)
        
        # Bind right-click to show context menu
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under the mouse
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def create_status_bar(self):
        """Create a status bar at the bottom of the window"""
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial status
        self.status_var.set("Ready")
    
    def add_entry(self):
        """Add a new entry from the form data"""
        name = self.name_var.get().strip()
        date = self.date_var.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()
        
        # Validate inputs
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        
        if not message:
            messagebox.showerror("Error", "Message cannot be empty")
            return
        
        # Validate date format
        try:
            if date:
                datetime.datetime.strptime(date, "%Y-%m-%d")
                # Add time part to the date
                date = f"{date} {datetime.datetime.now().strftime('%H:%M:%S')}"
            else:
                date = None  # Let the data handler use current date and time
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return
        
        # Add the entry
        if self.data_handler.add_entry(name, message, date):
            self.status_var.set(f"New entry added: {name}")
            
            # Clear form fields
            self.name_var.set("")
            self.date_var.set(datetime.datetime.now().strftime("%Y-%m-%d"))
            self.message_text.delete("1.0", tk.END)
            
            # Refresh entries display
            self.refresh_entries()
        else:
            messagebox.showerror("Error", "Failed to add entry")
    
    def refresh_entries(self):
        """Refresh the entries displayed in the treeview"""
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all entries and add them to the treeview
        entries = self.data_handler.get_all_entries()
        
        if not entries:
            self.status_var.set("No entries found")
            return
        
        # Add entries to treeview
        for entry in entries:
            self.tree.insert("", "end", values=(
                entry['id'],
                entry['name'],
                entry['date'],
                entry['message']
            ))
        
        self.status_var.set(f"Displaying {len(entries)} entries")
    
    def search_entries(self):
        """Search entries based on the search query"""
        query = self.search_var.get().strip()
        
        if not query:
            self.refresh_entries()
            return
        
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search entries
        results = self.data_handler.search_entries(query)
        
        if not results:
            self.status_var.set(f"No entries found for '{query}'")
            return
        
        # Add search results to treeview
        for entry in results:
            self.tree.insert("", "end", values=(
                entry['id'],
                entry['name'],
                entry['date'],
                entry['message']
            ))
        
        self.status_var.set(f"Found {len(results)} entries matching '{query}'")
    
    def filter_entries(self):
        """Filter entries by date range"""
        start_date = self.filter_start_var.get().strip()
        end_date = self.filter_end_var.get().strip()
        
        if not start_date:
            messagebox.showerror("Error", "Start date is required for filtering")
            return
        
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter entries
        results = self.data_handler.filter_by_date(start_date, end_date)
        
        if not results:
            self.status_var.set("No entries found in the specified date range")
            return
        
        # Add filtered results to treeview
        for entry in results:
            self.tree.insert("", "end", values=(
                entry['id'],
                entry['name'],
                entry['date'],
                entry['message']
            ))
        
        date_range = f"from {start_date}"
        if end_date:
            date_range += f" to {end_date}"
        
        self.status_var.set(f"Found {len(results)} entries {date_range}")
    
    def delete_selected_entry(self):
        """Delete the selected entry"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No entry selected")
            return
        
        # Get the ID of the selected entry
        item_values = self.tree.item(selected_item, "values")
        entry_id = int(item_values[0])
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this entry?"):
            if self.data_handler.delete_entry(entry_id):
                self.status_var.set(f"Entry {entry_id} deleted")
                self.refresh_entries()
            else:
                messagebox.showerror("Error", "Failed to delete entry")
    
    def new_guestbook(self):
        """Create a new guest book"""
        if messagebox.askyesno("New Guest Book", "Create a new guest book? This will clear all current entries."):
            self.data_handler = DataHandler()
            self.refresh_entries()
            self.status_var.set("New guest book created")
    
    def open_guestbook(self):
        """Open an existing guest book file"""
        file_path = filedialog.askopenfilename(
            title="Open Guest Book",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            self.data_handler = DataHandler(file_path)
            self.refresh_entries()
            self.status_var.set(f"Opened guest book from {file_path}")
    
    def save_guestbook_as(self):
        """Save the guest book to a new file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Guest Book As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            # Update the data handler with the new file path
            self.data_handler.file_path = file_path
            
            # Save the data
            if self.data_handler.save_data():
                self.status_var.set(f"Guest book saved to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to save guest book")
    
    def export_to_csv(self):
        """Export the guest book to a CSV file"""
        file_path = filedialog.asksaveasfilename(
            title="Export to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.data_handler.export_to_csv(file_path):
                self.status_var.set(f"Guest book exported to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to export to CSV")
    
    def clear_all_entries(self):
        """Clear all entries after confirmation"""
        if messagebox.askyesno("Clear All Entries", "Are you sure you want to clear all entries? This cannot be undone."):
            self.data_handler.entries = []
            if self.data_handler.save_data():
                self.refresh_entries()
                self.status_var.set("All entries cleared")
            else:
                messagebox.showerror("Error", "Failed to clear entries")
    
    def show_about(self):
        """Show the about dialog"""
        messagebox.showinfo(
            "About Guest Book",
            "Guest Book Application\n\n"
            "A simple application to manage guest book entries.\n\n"
            "Version 1.0"
        )
    
    def run(self):
        """Run the application main loop"""
        self.root.mainloop()
