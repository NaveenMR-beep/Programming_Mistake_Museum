import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import logging
import os
import shutil

from config import DATABASE_NAME, APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

# ----------------------------
# Functions for buttons
# ----------------------------
logging.basicConfig(
    filename="museum.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def add_mistake():

    add_window = tk.Toplevel(root)

    add_window.title("Add Programming Mistake")

    add_window.geometry("700x600")


    # Title
    title = tk.Label(
        add_window,
        text="➕ ADD PROGRAMMING MISTAKE",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=20)


    # Form Frame
    form_frame = tk.Frame(add_window)

    form_frame.pack(pady=10)


    # Error Message
    tk.Label(
        form_frame,
        text="Error Message:",
        font=("Arial", 12)
    ).grid(row=0, column=0, padx=10, pady=10)

    error_entry = tk.Entry(
        form_frame,
        width=40
    )

    error_entry.grid(row=0, column=1)


    # Project
    tk.Label(
        form_frame,
        text="Project:",
        font=("Arial", 12)
    ).grid(row=1, column=0, padx=10, pady=10)

    project_entry = tk.Entry(
        form_frame,
        width=40
    )

    project_entry.grid(row=1, column=1)


    # Code
    tk.Label(
        form_frame,
        text="Code:",
        font=("Arial", 12)
    ).grid(row=2, column=0, padx=10, pady=10)

    code_text = tk.Text(
        form_frame,
        width=40,
        height=5
    )

    code_text.grid(row=2, column=1)


    # Explanation
    tk.Label(
        form_frame,
        text="My Mistake:",
        font=("Arial", 12)
    ).grid(row=3, column=0, padx=10, pady=10)

    explanation_text = tk.Text(
        form_frame,
        width=40,
        height=4
    )

    explanation_text.grid(row=3, column=1)


    # Solution
    tk.Label(
        form_frame,
        text="Solution:",
        font=("Arial", 12)
    ).grid(row=4, column=0, padx=10, pady=10)

    solution_text = tk.Text(
        form_frame,
        width=40,
        height=4
    )

    solution_text.grid(row=4, column=1)

    def save_mistake():
        error_message = error_entry.get().strip()
        project = project_entry.get().strip()

        code = code_text.get("1.0", tk.END).strip()
        explanation = explanation_text.get("1.0", tk.END).strip()
        solution = solution_text.get("1.0", tk.END).strip()

        # Check required fields
        if not error_message or not project:
            messagebox.showwarning(
            "Missing Information",
            "Please enter Error Message and Project."
            )
            return

    # Automatic analysis
        error_type = detect_error_type(error_message)

        category = categorize_error(error_type)

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            connection = sqlite3.connect(DATABASE_NAME)

            cursor = connection.cursor()

            cursor.execute("""
            INSERT INTO mistakes
            (
                error_type,
                category,
                error_message,
                project,
                code,
                explanation,
                solution,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            error_type,
            category,
            error_message,
            project,
            code,
            explanation,
            solution,
            created_at
            ))

            connection.commit()

            connection.close()
            logging.info(
                    f"New mistake added: {error_type} | Project: {project}"
                    )

            messagebox.showinfo(
           "Success",
            f"✅ Mistake saved successfully!\n\n"
            f"Detected Error: {error_type}\n"
            f"Category: {category}"
            )

            # Clear fields
            error_entry.delete(0, tk.END)
            project_entry.delete(0, tk.END)

            code_text.delete("1.0", tk.END)
            explanation_text.delete("1.0", tk.END)
            solution_text.delete("1.0", tk.END)

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                 str(error)
            )
            logging.error(
                f"Database error: {error}"
                )

    save_button = tk.Button(
       add_window,
       text="💾 SAVE MISTAKE",
       font=("Arial", 14, "bold"),
       width=20,
       command=save_mistake
       )

    save_button.pack(pady=20)

def view_mistakes():

    # Create new window
    view_window = tk.Toplevel(root)

    view_window.title("View Mistakes")

    view_window.geometry("1000x550")


    # Title
    title = tk.Label(
        view_window,
        text="📋 ALL PROGRAMMING MISTAKES",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=20)


    # Table columns
    columns = (
        "ID",
        "Error Type",
        "Category",
        "Project",
        "Date"
    )


    # Create table
    table = ttk.Treeview(
        view_window,
        columns=columns,
        show="headings"
    )


    # Column headings
    for column in columns:

        table.heading(column, text=column)

        table.column(column, width=180)


    # Get data from database
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            error_type,
            category,
            project,
            created_at
        FROM mistakes
        ORDER BY id DESC
    """)

    mistakes = cursor.fetchall()

    connection.close()


    # Insert data into table
    for mistake in mistakes:

        table.insert(
            "",
            tk.END,
            values=mistake
        )


    # Show table
    table.pack(
        fill=tk.BOTH,
        expand=True,
        padx=20,
        pady=20
    )


    # =====================================
    # DELETE FUNCTION
    # =====================================

    def delete_selected():

        selected_item = table.selection()

        if not selected_item:

            messagebox.showwarning(
                "No Selection",
                "Please select a mistake first."
            )

            return


        values = table.item(
            selected_item[0]
        )["values"]

        mistake_id = values[0]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this mistake?"
        )

        if not confirm:
            return


        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM mistakes WHERE id = ?",
            (mistake_id,)
        )

        connection.commit()

        connection.close()
        logging.info(
            f"Mistake deleted: ID {mistake_id}"
        )


        # Remove from GUI table
        table.delete(selected_item[0])


        messagebox.showinfo(
            "Success",
            "✅ Mistake deleted successfully!"
        )


    # =====================================
    # EDIT FUNCTION
    # =====================================

    def edit_selected():

        selected_item = table.selection()

        if not selected_item:

            messagebox.showwarning(
                "No Selection",
                "Please select a mistake first."
            )

            return


        values = table.item(
            selected_item[0]
        )["values"]

        mistake_id = values[0]


        # Get selected mistake from database
        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                error_message,
                project,
                code,
                explanation,
                solution
            FROM mistakes
            WHERE id = ?
        """, (mistake_id,))


        mistake = cursor.fetchone()

        connection.close()


        if not mistake:

            messagebox.showerror(
                "Error",
                "Mistake not found."
            )

            return


        # =====================================
        # CREATE EDIT WINDOW
        # =====================================

        edit_window = tk.Toplevel(view_window)

        edit_window.title("Edit Mistake")

        edit_window.geometry("700x600")


        tk.Label(
            edit_window,
            text="✏️ EDIT PROGRAMMING MISTAKE",
            font=("Arial", 18, "bold")
        ).pack(pady=20)


        form_frame = tk.Frame(edit_window)

        form_frame.pack(pady=10)


        # =====================================
        # ERROR MESSAGE
        # =====================================

        tk.Label(
            form_frame,
            text="Error Message:"
        ).grid(row=0, column=0, padx=10, pady=10)


        error_entry = tk.Entry(
            form_frame,
            width=40
        )

        error_entry.grid(row=0, column=1)

        error_entry.insert(0, mistake[0])


        # =====================================
        # PROJECT
        # =====================================

        tk.Label(
            form_frame,
            text="Project:"
        ).grid(row=1, column=0, padx=10, pady=10)


        project_entry = tk.Entry(
            form_frame,
            width=40
        )

        project_entry.grid(row=1, column=1)

        project_entry.insert(0, mistake[1])


        # =====================================
        # CODE
        # =====================================

        tk.Label(
            form_frame,
            text="Code:"
        ).grid(row=2, column=0, padx=10, pady=10)


        code_text = tk.Text(
            form_frame,
            width=40,
            height=5
        )

        code_text.grid(row=2, column=1)

        code_text.insert("1.0", mistake[2])


        # =====================================
        # EXPLANATION
        # =====================================

        tk.Label(
            form_frame,
            text="My Mistake:"
        ).grid(row=3, column=0, padx=10, pady=10)


        explanation_text = tk.Text(
            form_frame,
            width=40,
            height=4
        )

        explanation_text.grid(row=3, column=1)

        explanation_text.insert("1.0", mistake[3])


        # =====================================
        # SOLUTION
        # =====================================

        tk.Label(
            form_frame,
            text="Solution:"
        ).grid(row=4, column=0, padx=10, pady=10)


        solution_text = tk.Text(
            form_frame,
            width=40,
            height=4
        )

        solution_text.grid(row=4, column=1)

        solution_text.insert("1.0", mistake[4])


        # =====================================
        # SAVE CHANGES FUNCTION
        # =====================================

        def save_changes():

            error_message = error_entry.get().strip()

            project = project_entry.get().strip()

            code = code_text.get(
                "1.0",
                tk.END
            ).strip()

            explanation = explanation_text.get(
                "1.0",
                tk.END
            ).strip()

            solution = solution_text.get(
                "1.0",
                tk.END
            ).strip()


            # Detect error automatically
            error_type = detect_error_type(error_message)

            category = categorize_error(error_type)


            # Update database
            connection = sqlite3.connect(DATABASE_NAME)

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE mistakes
                SET
                    error_type = ?,
                    category = ?,
                    error_message = ?,
                    project = ?,
                    code = ?,
                    explanation = ?,
                    solution = ?
                WHERE id = ?
            """, (
                error_type,
                category,
                error_message,
                project,
                code,
                explanation,
                solution,
                mistake_id
            ))


            connection.commit()

            connection.close()
            logging.info(
                f"Mistake updated: ID {mistake_id} | Error: {error_type}"
            )


            # Update GUI table
            table.item(
                selected_item[0],
                values=(
                    mistake_id,
                    error_type,
                    category,
                    project,
                    values[4]
                )
            )


            messagebox.showinfo(
                "Success",
                "✅ Mistake updated successfully!"
            )


            edit_window.destroy()


        # =====================================
        # SAVE BUTTON
        # =====================================

        save_button = tk.Button(
            edit_window,
            text="💾 SAVE CHANGES",
            font=("Arial", 13, "bold"),
            command=save_changes
        )

        save_button.pack(pady=20)


    # =====================================
    # EDIT + DELETE BUTTONS
    # =====================================

    button_frame = tk.Frame(view_window)

    button_frame.pack(pady=10)


    edit_button = tk.Button(
        button_frame,
        text="✏️ Edit Selected",
        font=("Arial", 12),
        command=edit_selected
    )

    edit_button.grid(
        row=0,
        column=0,
        padx=10
    )


    delete_button = tk.Button(
        button_frame,
        text="🗑️ Delete Selected",
        font=("Arial", 12),
        command=delete_selected
    )

    delete_button.grid(
        row=0,
        column=1,
        padx=10
    )

        

def search_mistakes():

    search_window = tk.Toplevel(root)

    search_window.title("Search Mistakes")

    search_window.geometry("1000x550")


    # Title
    title = tk.Label(
        search_window,
        text="🔍 SEARCH PROGRAMMING MISTAKES",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=20)


    # Search frame
    search_frame = tk.Frame(search_window)

    search_frame.pack(pady=10)


    tk.Label(
        search_frame,
        text="Search:",
        font=("Arial", 13)
    ).grid(row=0, column=0, padx=10)


    search_entry = tk.Entry(
        search_frame,
        width=40,
        font=("Arial", 12)
    )

    search_entry.grid(row=0, column=1, padx=10)


    # Table columns
    columns = (
        "ID",
        "Error Type",
        "Category",
        "Error Message",
        "Project",
        "Date"
    )


    table = ttk.Treeview(
        search_window,
        columns=columns,
        show="headings"
    )


    # Configure columns
    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=150
        )


    table.pack(
        fill=tk.BOTH,
        expand=True,
        padx=20,
        pady=20
    )


    # Search function
    def perform_search():

        search_text = search_entry.get().strip()


        # Clear old results
        for item in table.get_children():
            table.delete(item)


        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()


        cursor.execute("""
            SELECT
                id,
                error_type,
                category,
                error_message,
                project,
                created_at
            FROM mistakes
            WHERE
                error_type LIKE ?
                OR category LIKE ?
                OR error_message LIKE ?
                OR project LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search_text}%",
            f"%{search_text}%",
            f"%{search_text}%",
            f"%{search_text}%"
        ))


        results = cursor.fetchall()

        connection.close()


        # Insert search results
        for mistake in results:

            table.insert(
                "",
                tk.END,
                values=mistake
            )


        # Show message if nothing found
        if not results:

            messagebox.showinfo(
                "Search Results",
                "No mistakes found."
            )


    # Search button
    search_button = tk.Button(
        search_frame,
        text="🔍 Search",
        font=("Arial", 12),
        command=perform_search
    )

    search_button.grid(
        row=0,
        column=2,
        padx=10
    )

def show_error_chart():

    # Connect to database
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    # Get error types and their counts
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
    """)


    data = cursor.fetchall()

    connection.close()


    # Check if data exists
    if not data:

        messagebox.showinfo(
            "No Data",
            "No mistakes available to create a chart."
        )

        return


    # Separate names and counts
    error_types = []

    counts = []

    for error_type, count in data:

        error_types.append(error_type)

        counts.append(count)


    # Create chart
    plt.figure(figsize=(10, 6))

    plt.bar(error_types, counts)


    # Chart labels
    plt.title("Programming Errors Analysis")

    plt.xlabel("Error Type")

    plt.ylabel("Number of Mistakes")


    # Rotate names
    plt.xticks(rotation=30)


    # Adjust layout
    plt.tight_layout()


    # Show chart
    plt.show()


def backup_database():

    # Create backups folder if it doesn't exist
    if not os.path.exists("backups"):
        os.makedirs("backups")


    # Create backup filename with date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = f"backups/museum_backup_{timestamp}.db"


    try:

        # Copy database
        shutil.copy2(
            DATABASE_NAME,
            backup_file
        )


        logging.info(
            f"Database backup created: {backup_file}"
        )


        messagebox.showinfo(
            "Backup Successful",
            f"✅ Database backup created successfully!\n\n{backup_file}"
        )


    except Exception as error:

        logging.error(
            f"Backup error: {error}"
        )


        messagebox.showerror(
            "Backup Error",
            str(error)
        )

def show_statistics():

    statistics_window = tk.Toplevel(root)
    statistics_window.title("Programming Mistake Statistics")
    statistics_window.geometry("700x600")

    # Title
    tk.Label(
        statistics_window,
        text="📊 PROGRAMMING MISTAKE STATISTICS",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # Connect database
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Total mistakes
    cursor.execute("SELECT COUNT(*) FROM mistakes")
    total = cursor.fetchone()[0]

    # Most common error
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    common_error = cursor.fetchone()

    # Most common category
    cursor.execute("""
        SELECT category, COUNT(*)
        FROM mistakes
        GROUP BY category
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    common_category = cursor.fetchone()

    # Most problematic project
    cursor.execute("""
        SELECT project, COUNT(*)
        FROM mistakes
        GROUP BY project
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    common_project = cursor.fetchone()

    # Error distribution
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
    """)
    error_data = cursor.fetchall()

    connection.close()

    # Total
    tk.Label(
        statistics_window,
        text=f"📚 Total Mistakes: {total}",
        font=("Arial", 15, "bold")
    ).pack(pady=10)

    # Common error
    if common_error:
        text = f"🔥 Most Common Error: {common_error[0]} ({common_error[1]} times)"
    else:
        text = "🔥 Most Common Error: None"

    tk.Label(
        statistics_window,
        text=text,
        font=("Arial", 13)
    ).pack(pady=5)

    # Common category
    if common_category:
        text = f"📁 Most Common Category: {common_category[0]} ({common_category[1]} times)"
    else:
        text = "📁 Most Common Category: None"

    tk.Label(
        statistics_window,
        text=text,
        font=("Arial", 13)
    ).pack(pady=5)

    # Problematic project
    if common_project:
        text = f"💻 Most Problematic Project: {common_project[0]} ({common_project[1]} mistakes)"
    else:
        text = "💻 Most Problematic Project: None"

    tk.Label(
        statistics_window,
        text=text,
        font=("Arial", 13)
    ).pack(pady=5)

    # Distribution title
    tk.Label(
        statistics_window,
        text="📈 Error Distribution",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Table
    columns = ("Error Type", "Count")

    table = ttk.Treeview(
        statistics_window,
        columns=columns,
        show="headings",
        height=10
    )

    table.heading("Error Type", text="Error Type")
    table.heading("Count", text="Number of Mistakes")

    table.column("Error Type", width=300)
    table.column("Count", width=200)

    for error_type, count in error_data:
        table.insert(
            "",
            tk.END,
            values=(error_type, count)
        )

    table.pack(
        padx=20,
        pady=10,
        fill=tk.X
    )

def detect_patterns():

    pattern_window = tk.Toplevel(root)

    pattern_window.title("Pattern Detection")

    pattern_window.geometry("750x600")


    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        pattern_window,
        text="🤖 PROGRAMMING MISTAKE PATTERNS",
        font=("Arial", 20, "bold")
    ).pack(pady=20)


    # =====================================
    # DATABASE CONNECTION
    # =====================================

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    # =====================================
    # FIND REPEATED ERROR TYPES
    # =====================================

    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        HAVING COUNT(*) >= 2
        ORDER BY COUNT(*) DESC
    """)

    repeated_errors = cursor.fetchall()


    # =====================================
    # FIND REPEATED PROJECTS
    # =====================================

    cursor.execute("""
        SELECT project, COUNT(*)
        FROM mistakes
        GROUP BY project
        HAVING COUNT(*) >= 2
        ORDER BY COUNT(*) DESC
    """)

    repeated_projects = cursor.fetchall()


    connection.close()


    # =====================================
    # ERROR PATTERNS
    # =====================================

    tk.Label(
        pattern_window,
        text="⚠️ Repeated Error Patterns",
        font=("Arial", 16, "bold")
    ).pack(pady=10)


    if repeated_errors:

        for error_type, count in repeated_errors:

            message = (
                f"⚠️ {error_type} "
                f"appeared {count} times"
            )

            tk.Label(
                pattern_window,
                text=message,
                font=("Arial", 13)
            ).pack(pady=4)

    else:

        tk.Label(
            pattern_window,
            text="✅ No repeated error patterns found.",
            font=("Arial", 13)
        ).pack(pady=5)


    # =====================================
    # PROJECT PATTERNS
    # =====================================

    tk.Label(
        pattern_window,
        text="💻 Repeated Project Patterns",
        font=("Arial", 16, "bold")
    ).pack(pady=15)


    if repeated_projects:

        for project, count in repeated_projects:

            message = (
                f"💻 {project} "
                f"has {count} recorded mistakes"
            )

            tk.Label(
                pattern_window,
                text=message,
                font=("Arial", 13)
            ).pack(pady=4)

    else:

        tk.Label(
            pattern_window,
            text="✅ No repeated project patterns found.",
            font=("Arial", 13)
        ).pack(pady=5)


    # =====================================
    # RECOMMENDATION
    # =====================================

    tk.Label(
        pattern_window,
        text="💡 Recommendation",
        font=("Arial", 16, "bold")
    ).pack(pady=20)


    if repeated_errors:

        most_common = repeated_errors[0]

        recommendation = (
            f"You should practice {most_common[0]}.\n"
            f"It is your most frequently repeated error."
        )

    else:

        recommendation = (
            "🎉 Great job!\n"
            "You don't have any repeated errors yet."
        )


    tk.Label(
        pattern_window,
        text=recommendation,
        font=("Arial", 13),
        justify=tk.CENTER
    ).pack(pady=5)

def get_dashboard_data():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Total mistakes
    cursor.execute("""
        SELECT COUNT(*)
        FROM mistakes
    """)

    total_mistakes = cursor.fetchone()[0]

    # Most common error
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    common_error = cursor.fetchone()

    # Most common category
    cursor.execute("""
        SELECT category, COUNT(*)
        FROM mistakes
        GROUP BY category
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    common_category = cursor.fetchone()

    # Most problematic project
    cursor.execute("""
        SELECT project, COUNT(*)
        FROM mistakes
        GROUP BY project
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    problematic_project = cursor.fetchone()

    connection.close()

    return (
        total_mistakes,
        common_error,
        common_category,
        problematic_project
    )



# ----------------------------
# Main Window
# ----------------------------

root = tk.Tk()

root.title(APP_TITLE)

root.geometry("700x600")


# ----------------------------
# Title
# ----------------------------

title = tk.Label(
    root,
    text="🐛 PROGRAMMING MISTAKE MUSEUM",
    font=("Arial", 20, "bold")
)

title.pack(pady=30)


chart_button = tk.Button(
    root,
    text="📊 Error Charts",
    font=("Arial", 12),
    command=show_error_chart
)

chart_button.pack(pady=10)


# ============================
# GET DASHBOARD DATA
# ============================

total_mistakes, common_error, common_category, problematic_project = get_dashboard_data()


# ============================
# DASHBOARD FRAME
# ============================

dashboard_frame = tk.Frame(root)

dashboard_frame.pack(pady=10)


# Total mistakes
total_label = tk.Label(
    dashboard_frame,
    text=f"📊 Total Mistakes: {total_mistakes}",
    font=("Arial", 14, "bold")
)

total_label.pack(pady=5)


# Most common error
error_label = tk.Label(
    dashboard_frame,
    text="🔥 Most Common Error: None",
    font=("Arial", 13)
)

if common_error:

    error_label.config(
        text=f"🔥 Most Common Error: {common_error[0]} ({common_error[1]} times)"
    )

error_label.pack(pady=5)


# Main category
category_label = tk.Label(
    dashboard_frame,
    text="📁 Main Category: None",
    font=("Arial", 13)
)

if common_category:

    category_label.config(
        text=f"📁 Main Category: {common_category[0]}"
    )

category_label.pack(pady=5)


# Problematic project
project_label = tk.Label(
    dashboard_frame,
    text="💻 Most Problematic Project: None",
    font=("Arial", 13)
)

if problematic_project:

    project_label.config(
        text=f"💻 Most Problematic Project: {problematic_project[0]} ({problematic_project[1]} mistakes)"
    )

project_label.pack(pady=5)


def refresh_dashboard():

    total_mistakes, common_error, common_category, problematic_project = get_dashboard_data()

    total_label.config(
        text=f"📊 Total Mistakes: {total_mistakes}"
    )

    if common_error:
        error_label.config(
            text=f"🔥 Most Common Error: {common_error[0]} ({common_error[1]} times)"
        )
    else:
        error_label.config(
            text="🔥 Most Common Error: None"
        )

    if common_category:
        category_label.config(
            text=f"📁 Main Category: {common_category[0]}"
        )
    else:
        category_label.config(
            text="📁 Main Category: None"
        )

    if problematic_project:
        project_label.config(
            text=f"💻 Most Problematic Project: {problematic_project[0]} ({problematic_project[1]} mistakes)"
        )
    else:
        project_label.config(
            text="💻 Most Problematic Project: None"
        )
refresh_button = tk.Button(
    root,
    text="🔄 Refresh Dashboard",
    font=("Arial", 11),
    command=refresh_dashboard
)

refresh_button.pack(pady=10)


# ----------------------------
# Buttons
# ----------------------------

add_button = tk.Button(
    root,
    text="➕ Add Mistake",
    font=("Arial", 14),
    width=25,
    command=add_mistake
)

add_button.pack(pady=8)


view_button = tk.Button(
    root,
    text="📋 View Mistakes",
    font=("Arial", 14),
    width=25,
    command=view_mistakes
)

view_button.pack(pady=8)


search_button = tk.Button(
    root,
    text="🔍 Search Mistakes",
    font=("Arial", 14),
    width=25,
    command=search_mistakes
)

search_button.pack(pady=8)


statistics_button = tk.Button(
    root,
    text="📊 Statistics",
    font=("Arial", 14),
    width=25,
    command=show_statistics
)

statistics_button.pack(pady=8)


pattern_button = tk.Button(
    root,
    text="🤖 Pattern Detection",
    font=("Arial", 14),
    width=25,
    command=detect_patterns
)

pattern_button.pack(pady=8)



exit_button = tk.Button(
    root,
    text="❌ Exit",
    font=("Arial", 14),
    width=25,
    command=root.destroy
)

exit_button.pack(pady=8)


backup_button = tk.Button(
    root,
    text="💾 Backup Database",
    font=("Arial", 12),
    command=backup_database
)

backup_button.pack(pady=10)


# ----------------------------
# Run Application
# ----------------------------
def categorize_error(error_type):

    categories = {

        "NameError": "Variable / Naming Problem",

        "SyntaxError": "Code Structure Problem",

        "IndentationError": "Code Structure Problem",

        "TypeError": "Data Type Problem",

        "IndexError": "Collection Problem",

        "KeyError": "Collection Problem",

        "AttributeError": "Object / Attribute Problem",

        "ZeroDivisionError": "Mathematical Problem",

        "Unknown Error": "Unknown Category"
    }

    return categories.get(error_type, "Unknown Category")
def detect_error_type(error_message):

    message = error_message.lower()

    error_patterns = {

        "NameError": [
            "nameerror",
            "is not defined"
        ],

        "SyntaxError": [
            "syntaxerror",
            "invalid syntax"
        ],

        "TypeError": [
            "typeerror",
            "unsupported operand type"
        ],

        "IndexError": [
            "indexerror",
            "list index out of range"
        ],

        "KeyError": [
            "keyerror"
        ],

        "AttributeError": [
            "attributeerror",
            "has no attribute"
        ],

        "IndentationError": [
            "indentationerror",
            "unexpected indent"
        ],

        "ZeroDivisionError": [
            "zerodivisionerror",
            "division by zero"
        ]
    }

    for error_type, patterns in error_patterns.items():

        for pattern in patterns:

            if pattern in message:
                return error_type

    return "Unknown Error"




root.mainloop()