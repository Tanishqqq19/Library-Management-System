import sqlite3 as sql
def user_exist(email):
    conn=None
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            cur.execute('Select email from register_and_login where email=?',[email])
            records=cur.fetchall()
            if len(records)>0:
                return True
            else:
                return False
    except Exception as e:
        conn.rollback()
        n='operation unsuccessful'
    finally:
        conn.close()