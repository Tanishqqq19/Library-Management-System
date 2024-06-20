import sqlite3 as sql 
def user_exist(email: str | None) -> bool:
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
        return False
    finally:
        conn.close()