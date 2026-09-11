import sqlite3
import json
from datetime import datetime
def load_mistake():
    try:
        with open("mistakes.json","r")as file:
            return json.load(file)
    except FileNotFoundError:
        return[]
def save_mistakes(mistakes):
    with open("mistakes.json","w") as file:
        json.dump(mistakes,file,index=4)

def add_mistake():

    print("\n--- Add Mistake ---")

    error_message = input("Error message: ")
    # Automatic detection
    error_type = detect_error_type(error_message)

    print(f"\n🤖 Detected Error Type: {error_type}")
    category = categorize_error(error_type)

    print("\n🤖 Automatic Analysis")
    print("------------------------")
    print("Detected Error Type:", error_type)
    print("Detected Category:", category)
    project = input("Project name: ")
    code = input("Code: ")
    explanation = input("What was my mistake? ")
    solution = input("Solution: ")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO mistakes
    (error_type,category, error_message, project, code, explanation, solution, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
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

    print("\n✅ Mistake saved successfully!")
def view_mistakes():

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM mistakes")

    mistakes = cursor.fetchall()

    connection.close()

    if not mistakes:
        print("\nNo mistakes found.")
        return

    print("\n====================================")
    print("          YOUR MISTAKES")
    print("====================================")

    for mistake in mistakes:

        print("\n------------------------------")

        print("ID:", mistake[0])
        print("Error Type:", mistake[1])
        print("Error Message:", mistake[2])
        print("Project:", mistake[3])
        print("Code:", mistake[4])
        print("Your Mistake:", mistake[5])
        print("Solution:", mistake[6])
        print("Date:", mistake[7])
def edit_mistake():

    print("\n--- Edit Mistake ---")

    mistake_id = input("Enter mistake ID: ")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM mistakes WHERE id = ?",
        (mistake_id,)
    )

    mistake = cursor.fetchone()

    if mistake is None:
        print("Mistake not found!")
        connection.close()
        return

    print("\nCurrent mistake:")
    print("Error Type:", mistake[1])
    print("Error Message:", mistake[2])
    print("Project:", mistake[3])
    print("Code:", mistake[4])
    print("Explanation:", mistake[5])
    print("Solution:", mistake[6])

    print("\nEnter new values")

    error_type = input("Error type: ")
    error_message = input("Error message: ")
    project = input("Project name: ")
    code = input("Code: ")
    explanation = input("What was my mistake? ")
    solution = input("Solution: ")

    cursor.execute("""
        UPDATE mistakes
        SET error_type = ?,
            error_message = ?,
            project = ?,
            code = ?,
            explanation = ?,
            solution = ?
        WHERE id = ?
    """, (
        error_type,
        error_message,
        project,
        code,
        explanation,
        solution,
        mistake_id
    ))

    connection.commit()
    connection.close()

    print("\n✅ Mistake updated successfully!")

def delete_mistake():

    print("\n--- Delete Mistake ---")

    mistake_id = input("Enter mistake ID: ")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    # Check whether the mistake exists
    cursor.execute(
        "SELECT * FROM mistakes WHERE id = ?",
        (mistake_id,)
    )

    mistake = cursor.fetchone()

    if mistake is None:
        print("❌ Mistake not found!")
        connection.close()
        return

    # Show the mistake before deleting
    print("\nMistake found:")
    print("ID:", mistake[0])
    print("Error Type:", mistake[1])
    print("Error Message:", mistake[2])
    print("Project:", mistake[3])
    print("Code:", mistake[4])
    print("Your Mistake:", mistake[5])
    print("Solution:", mistake[6])
    print("Date:", mistake[7])
    confirmation = input("\nAre you sure you want to delete it? (y/n): ")

    if confirmation.lower() == "y":

        cursor.execute(
            "DELETE FROM mistakes WHERE id = ?",
            (mistake_id,)
        )

        connection.commit()

        print("✅ Mistake deleted successfully!")

    else:
        print("❌ Delete cancelled.")

    connection.close()
def show_statistics():

    print("\n--- Mistake Statistics ---")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    # Total number of mistakes
    cursor.execute("SELECT COUNT(*) FROM mistakes")

    total = cursor.fetchone()[0]

    print("\nTotal mistakes:", total)

    if total == 0:
        print("No mistakes recorded yet.")
        connection.close()
        return

    # Count mistakes by error type
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()

    print("\nMistakes by error type:")
    print("-------------------------")

    for error_type, count in results:
        print(f"{error_type}: {count}")

    connection.close()

def project_statistics():

    print("\n--- Project Statistics ---")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT project, COUNT(*)
        FROM mistakes
        GROUP BY project
        ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()

    if not results:
        print("No mistakes recorded yet.")
        connection.close()
        return

    print("\nMistakes by project:")
    print("---------------------")
    for project,count in results:
        print(f"{project}:{count}")
    print("\n most problematic project:")
    print(f"{results[0][0]}({results[0][1]} mistakes)")
    connection.close()

def improvement_tracking():

    print("\n====================================")
    print("       📈 IMPROVEMENT REPORT")
    print("====================================")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DATE(created_at), COUNT(*)
        FROM mistakes
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """)

    results = cursor.fetchall()

    if not results:
        print("\nNo mistakes recorded yet.")
        connection.close()
        return

    print("\nMistakes over time:")
    print("----------------------------")

    for date, count in results:
        print(f"{date} : {count} mistakes")

    # Trend analysis
    if len(results) >= 2:

        first_count = results[0][1]
        last_count = results[-1][1]

        print("\n--------------------------------")

        if last_count < first_count:
            print("📉 Trend: Improving! Great job!")

        elif last_count > first_count:
            print("📈 Trend: More mistakes recently.")

        else:
            print("➡️ Trend: No major change.")

    else:
        print("\nNeed more data to analyze improvement.")

    connection.close()

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

def detect_patterns():

    print("\n====================================")
    print("       🤖 PATTERN DETECTION")
    print("====================================")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    # Most frequent error
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM mistakes
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    frequent_error = cursor.fetchone()

    # Most common category
    cursor.execute("""
        SELECT category, COUNT(*)
        FROM mistakes
        WHERE category IS NOT NULL
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

    print()

    if frequent_error:
        print("🔥 Frequent Error:")
        print(f"{frequent_error[0]} — {frequent_error[1]} times")

    if common_category:
        print("\n📁 Main Problem Category:")
        print(f"{common_category[0]} — {common_category[1]} times")

    if problematic_project:
        print("\n💻 Most Problematic Project:")
        print(f"{problematic_project[0]} — {problematic_project[1]} mistakes")

    print("\n====================================")
    print("💡 RECOMMENDATION")
    print("====================================")

    if common_category:
        print(
            f"Focus more on practicing: {common_category[0]}"
        )

    connection.close()

def search_mistakes():
    search = input("\nEnter error type to search: ")

    connection = sqlite3.connect("museum.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM mistakes WHERE error_type LIKE ?",
        ("%" + search + "%",)
    )

    mistakes = cursor.fetchall()

    connection.close()

    if not mistakes:
        print("\n❌ No mistakes found.")
        return

    print("\n====================================")
    print("          SEARCH RESULTS")
    print("====================================")

    for mistake in mistakes:

        print("\n------------------------------")

        print("ID:", mistake[0])
        print("Error Type:", mistake[1])
        print("Error Message:", mistake[2])
        print("Project:", mistake[3])
        print("Code:", mistake[4])
        print("Your Mistake:", mistake[5])
        print("Solution:", mistake[6])
        print("Date:", mistake[7])

while True:

    print("\n====================================")
    print("     🐛 PROGRAMMING MISTAKE MUSEUM")
    print("====================================")

    print("1. Add mistake")
    print("2. View mistakes")
    print("3.search mistakes")
    print("4.Edit mistakes")
    print("5.delete mistakes")
    print("6.Statistics")
    print("7.prject Statistics")
    print("8.check improvement")
    print("9.pattern")
    print("10. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_mistake()

    elif choice == "2":
        view_mistakes()
    elif choice == "3":
        search_mistakes()
    elif choice == "4":
        edit_mistake()
    elif choice == "5":
        delete_mistake()
    elif choice == "6":
        show_statistics()
    elif choice == "7":
        project_statistics()
    elif choice == "8":
        improvement_tracking()
    elif choice == "9":
        detect_patterns()
    else:
        print("\n❌ Invalid option. Please try again.")