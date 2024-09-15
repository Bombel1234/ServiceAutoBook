import sqlite3
from android import mActivity



LIST_AUTO = 'list_auto'



def create_baza():
    context = mActivity.getApplicationContext()
    result =  context.getExternalFilesDir(None)   # don't forget the argument
    if result:
        storage_path =  str(result.toString())
        conn = sqlite3.connect(f'{storage_path}/myqsl2.db')
        cur = conn.cursor()
        
    
    return conn, cur


connect, cursor = create_baza()



def create_table_list_auto():
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {LIST_AUTO} ("
        f"marka TEXT NOT NULL,"
        f"marka_model NOT NULL,"
        f"model TEXT NOT NULL)"
    )
    connect.commit()


# чи е таблицi в базi
def or_table_in_baza():
    if cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchone():
        return True
    return False


# чи пуста  таблиця LIST_AUTO
def is_one_rows_table() -> bool:
    if cursor.execute(f"SELECT marka FROM {LIST_AUTO}").fetchone():
        return True
    return False


# вивести все авта в list auto
def select_all_auto():
    res = cursor.execute(f"SELECT marka, model FROM {LIST_AUTO}").fetchall()
    return res


def or_ist_auto(marka_model) -> bool:
    if cursor.execute(f"SELECT marka_model FROM {LIST_AUTO} WHERE marka_model='{marka_model}'").fetchone():
        return True
    return False


# додавання автомобiля до бази
def add_marka_model_baza(marka, title, model) -> None:
    cursor.execute(f"INSERT INTO {LIST_AUTO} VALUES(?,?,?)",
                   (marka, title, model))

    connect.commit()


# function table info-------##########
def create_table_name_auto(name_auto):
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {name_auto} ("
        f"km INT NOT NULL,"
        f"work TEXT NOT NULL,"
        f"cena TEXT NOT NULL,"
        f"data INT NOT NULL)"
    )
    connect.commit()


def is_km(name_auto):
    if cursor.execute(f"SELECT km FROM {name_auto}").fetchone():
        return True
    return False


def digit_end_km(name_auto):
    res = cursor.execute(f"SELECT km FROM {name_auto}").fetchall()
    max_number = max(res)
    return max_number


# додавання iнформаций про авто
def save_info_auto(km, work, cena, data, name_auto):
    cursor.execute(f"INSERT INTO {name_auto} VALUES(?,?,?,?)",
                   (km, work, cena, data))
    connect.commit()


# вибор всех записей об определеным авто
def select_info_auto(name_auto) -> list:
    res = cursor.execute(f"SELECT * FROM {name_auto}").fetchall()
    return res


def select_rowid_for_update(name_auto, km) -> int:
    res = cursor.execute(f"SELECT ROWID FROM {name_auto} WHERE km={km}").fetchone()
    return res[0]


def update_baza_info(km, work, cena, data, name_auto, rowid) -> None:
    cursor.execute(f"UPDATE {name_auto} SET km = {km}, work = '{work}', "
                   f"cena = {cena}, data = '{data}' WHERE ROWID={rowid}")
    connect.commit()


def delete_auto_in_baza(name_auto):
    cursor.execute(f"DROP TABLE {name_auto}")
    cursor.execute(f"DELETE FROM {LIST_AUTO} WHERE marka_model='{name_auto}'")
    connect.commit()
