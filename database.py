# Function to open a connection to the SQLite database
def get_db_conn():
    conn = sqlite3.connect(DB_FILE)  # Connect to DB file (ma-create if wala pa)
    conn.row_factory = sqlite3.Row   # Para column names ma-access like dictionary
    return conn                      # Return the connection object

# Function to initialize the database and create tables if wala pa sila
def init_db():
    conn = get_db_conn()     # Get database connection
    c = conn.cursor()        # Create cursor para maka-run SQL commands

    # Create table for user accounts
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    # Table para ma-track kung asa na chapter ang user, pag iyang e save and exit
    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER PRIMARY KEY,
            chapter INTEGER NOT NULL
        )
    """)

    # Table para sa forensic logs — mga actions sa user
    c.execute("""
        CREATE TABLE IF NOT EXISTS forensic_logs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            action TEXT,
            timestamp TEXT
        )
    """)

    # Table para evidence registry per chapter
    c.execute("""
        CREATE TABLE IF NOT EXISTS evidence_registry (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            chapter INTEGER,
            file_path TEXT,
            description TEXT
        )
    """)

    # Table para storing the random seed per user per chapter
    c.execute("""
        CREATE TABLE IF NOT EXISTS seeds (
            user_id INTEGER,
            chapter INTEGER,
            seed INTEGER,
            PRIMARY KEY(user_id, chapter)
        )
    """)

    conn.commit()   # Save changes
    conn.close()    # Close connection
