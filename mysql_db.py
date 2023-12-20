import pymysql


# 打开数据库连接
def connect():
    db = pymysql.connect(host="localhost", user="root", password="root1234", database="device")

    return db


# 断开连接
def disconnect(db):
    db.close()


def login_db(customer_name):
    db = connect()
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM customer WHERE customer_name = %s"
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql, (customer_name,))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results


def get_user(customer_id):
    db = connect()
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM customer WHERE customer_id = %s"
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql, (customer_id,))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results


def register_db(row):
    db = connect()
    cursor = db.cursor()

    sql = "INSERT INTO customer (customer_name,customer_phone,billing_addr,passwd) VALUES (%s, %s, %s, %s)"

    result = False
    try:
        # 执行sql语句
        cursor.execute(sql, tuple(row))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result


def get_locations(customer_id):
    db = connect()
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM location WHERE customer_id = %s"
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql,(customer_id))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results


def get_locations_by_id(location_id):
    db = connect()
    cursor = db.cursor()
    sql = "SELECT * FROM location WHERE location_id = %s"
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql, (location_id,))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results


def add_locations(row):
    db = connect()
    cursor = db.cursor()

    sql = """
    INSERT INTO location (customer_id,unit_and_street_address,city,state,zip_code,acquisitiondate,square_footage,number_of_bedrooms,number_of_occupants) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    result = False
    try:
        # 执行sql语句
        cursor.execute(sql, tuple(row))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result


def update_locations(location_id, row):
    db = connect()
    cursor = db.cursor()

    sql = """
     UPDATE location SET 
            customer_id = %s, 
            unit_and_street_address = %s,
            city = %s,
            state = %s,   
            zip_code = %s,
            acquisitiondate = %s,
            square_footage = %s,
            number_of_bedrooms = %s,
            number_of_occupants =%s
        WHERE location_id = %s
     """
    row.append(location_id)
    result = False
    try:
        # 执行sql语句
        cursor.execute(sql, tuple(row))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result


def del_location(location_id):
    db = connect()
    cursor = db.cursor()

    sql = "DELETE FROM location WHERE location_id = %s"
    result = False
    try:
        # 执行sql语句
        cursor.execute(sql, (location_id,))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result

def get_devices_by_location_id(location_id):
    db=connect()
    cursor=db.cursor()

    sql='SELECT * FROM device WHERE location_id = %s'
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql, (location_id,))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results

def get_devices_by_id(device_id):
    db=connect()
    cursor=db.cursor()

    sql='SELECT * FROM device WHERE device_id = %s'
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql, (device_id,))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results

def add_device(row):
    db=connect()
    cursor=db.cursor()

    sql = """
    INSERT INTO device (location_id,device_type,model_num) 
    VALUES (%s, %s, %s)
    """

    result = False
    try:
        # 执行sql语句
        cursor.execute(sql, tuple(row))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result

def update_device(device_id,row):
    db=connect()
    cursor=db.cursor()

    sql = """
    UPDATE device SET location_id = %s, device_type = %s, model_num = %s WHERE device_id = %s
    """
    result = False
    row.append(device_id)
    try:
        # 执行sql语句
        cursor.execute(sql, tuple(row))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result

def del_device(device_id):
    db = connect()
    cursor = db.cursor()

    sql = "DELETE FROM device WHERE device_id = %s"
    result = False
    try:
        # 执行sql语句
        cursor.execute(sql, (device_id,))
        # 执行sql语句
        db.commit()
        result = True
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    disconnect(db)
    return result


def get_usage_by_device_id(device_id):
    db=connect()
    cursor=db.cursor()

    sql='SELECT * FROM energy_usage WHERE device_id = %s'
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql, (device_id,))
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    disconnect(db)
    return results


"""以下为创建数据库表"""


def creat_if_customer_not_exists():
    # 如果不存在，创建表
    db = connect()
    # 使用预处理语句创建表
    sql = """CREATE TABLE IF NOT EXISTS customer (
              customer_id INT AUTO_INCREMENT PRIMARY KEY,
              customer_name VARCHAR(255),
              customer_phone VARCHAR(20),
              billing_addr VARCHAR(255),
              passwd VARCHAR(64)
             )"""
    cursor = db.cursor()
    cursor.execute(sql)
    disconnect(db)


def creat_if_location_not_exists():
    db = connect()
    sql = """
        CREATE TABLE IF NOT EXISTS location (
        location_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        unit_and_street_address VARCHAR(255),
        city VARCHAR(100),
        state VARCHAR(100),
        zip_code VARCHAR(10),
        acquisitiondate DATETIME,
        square_footage INT,
        number_of_bedrooms INT,
        number_of_occupants INT,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
        )
        """
    cursor = db.cursor()
    cursor.execute(sql)
    disconnect(db)


def creat_if_device_not_exists():
    db = connect()
    sql = """
        CREATE TABLE IF NOT EXISTS  device (
        device_id INT AUTO_INCREMENT PRIMARY KEY,
        location_id INT,
        device_type VARCHAR(100),
        model_num VARCHAR(100),
        FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE CASCADE
        )
        """
    cursor = db.cursor()
    cursor.execute(sql)
    disconnect(db)

def creat_if_energyusage_not_exists():
    db=connect()
    sql="""
    CREATE TABLE IF NOT EXISTS energy_usage (
        device_id INT,
        timestamp DATETIME,
        interval_time INT,
        event_label VARCHAR(100),
        event_value DECIMAL(10, 3),
        PRIMARY KEY (device_id,timestamp),
        FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE CASCADE
    ) 
    """
    cursor = db.cursor()
    cursor.execute(sql)
    disconnect(db)

def creat_if_energyprice_not_exists():
    db=connect()
    sql="""
     CREATE TABLE IF NOT EXISTS energy_price (
        zip_code VARCHAR(10),
        start_time DATETIME,
        price_per_KWh DECIMAL(10, 3),
        PRIMARY KEY (zip_code, start_time)
     )
    """
    cursor = db.cursor()
    cursor.execute(sql)
    disconnect(db)

if __name__ == "__main__":
    creat_if_customer_not_exists()
    creat_if_location_not_exists()
    creat_if_device_not_exists()
    creat_if_energyusage_not_exists()
    creat_if_energyprice_not_exists()
