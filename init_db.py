import sqlite3

def get_db_connection():
    db_file = 'database.db'
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    conn = get_db_connection()

    with open('schema.sql') as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    # from the tutorial
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('First Post', 'Content for the first post')
                )

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('Second Post', 'Content for the second post')
                )

    conn.commit()
    conn.close()

    # init with default data
    # users
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    if not users:
        cur = conn.cursor()
        insert = "INSERT INTO users (username, passcode) VALUES (?, ?)"
        cur.execute(insert, ('admin', 'pass123'))
        conn.commit()

    # recipe
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    if not recipes:
        # if nothing here, just rebuilt the whole DB
        conn = get_db_connection()
        db_dir =  "C:/Users/Bryan/repos/project/communitycookbook_UI/"
        init_f = db_dir + 'data_init.sql'
        with open(init_f) as f:
            conn.executescript(f.read())

    conn.commit()
    conn.close()
