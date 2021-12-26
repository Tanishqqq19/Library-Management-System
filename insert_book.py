import sqlite3 as sql
conn=None
# books
# https://i.postimg.cc/cCG9FxkM/pride-and-prejudice.jpg
# https://i.postimg.cc/1zgvPnLr/harry-potter1.jpg
# https://i.postimg.cc/jdsv2kp5/harry-potter2.jpg
# https://i.postimg.cc/vm6tCRVP/great-expectations.jpg
# https://i.postimg.cc/1XMGDskz/emma.jpg
# https://i.postimg.cc/pTJztPXB/percy-jackson1.jpg
# https://i.postimg.cc/mkrzfMnb/arms-and-the-man.jpg
# https://i.postimg.cc/rpStSqWL/robinson-crusoe.jpg
# https://i.postimg.cc/HWS80ZJj/David-Copperfield.jpg
# https://i.postimg.cc/1zZ8Rbd7/Heroes-of-Olympus1.jpg

try:
    print(1)
    with sql.connect('library.db') as conn:
        cur=conn.cursor()
        print(2)
        for i in range(5):
            cur.execute('INSERT INTO records(books_name, start, end, first_name) Values(?,?,?,?)',("Heroes of Olympus",'21-7-21','24-7-21',"jeff"))
except Exception as e:
    conn.rollback()
finally:
    print(5)
    conn.close()

