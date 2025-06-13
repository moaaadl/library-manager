# 📚 Library Manager (Python OOP Project)

**Are you learning Python too?**  
<p>Fork this project, play with the code, and maybe even add a new feature!  
Pull requests are welcome!</p>

<h3>Installation & Setup</h3>

```bash
# Clone the repo
git clone https://github.com/moaaadl/library-manager.git

# Change directory
cd library-manager

# Install Required Packages
pip install python-dotenv
```

<h3>Database Setup</h3>


<p>The application now uses SQLite, which requires no additional setup! The database file (library.db) will be created automatically when you first run the application.
SQLite benefits:

No separate database server needed
Lightweight and fast
Perfect for local development
Database stored as a single file</p>


<h3>Run the Application</h3>


```bash
python3 main.py
```
<h3>How to Use</h3>

| Command       | Description                          |
|---------------|--------------------------------------|
| `add`         | Add a new book to the library        |
| `show`        | Display all books in your collection |
| `search`      | Search for books by title            |
| `edit`        | Edit book information                |
| `remove`      | Remove a book from the library       |
| `state`       | Show library statistics              |
| `clear`       | Clear the terminal screen            |
| `help`        | Show all available commands          |
| `exit` or `X` | Exit the program                     |
| `help add`    | Show how to add books                |
| `help edit`   | Show how to edit books               |
| `help search` | Show how to search books             |
| `help remove` | Show how to remove books             |

<h3>Example Usage</h3>

```
Enter command (or 'help' for options): add "Can't Hurt Me" "David Goggins" 2018
Are you sure you want to save 'Can't Hurt Me'? (Y/N) y
'Can't Hurt Me by David Goggins in 2018' has been added successfully!

Enter command (or 'help' for options): search Goggins
Matching books for 'Goggins':
1 - 'Can't Hurt Me by David Goggins in 2018'

Enter command (or 'help' for options): help add

=== ADD COMMAND ===
Usage: add "Title" "Author" year
Example: add "1984" "George Orwell" 1949
===================
```
