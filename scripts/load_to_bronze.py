import os
import json
import glob
from databricks import sql

SERVER_HOSTNAME = "dbc-804dfgkndf-8c53.cloud.databricks.com"
HTTP_PATH = "/sql/1.0/warehouses/605jgfdfsk81af3fa7ba"
ACCESS_TOKEN = "dapi0031963dfbd___2c"

def load_latest_json_to_databricks():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    json_files = glob.glob(os.path.join(raw_dir, "protocols_*.json"))
    
    if not json_files:
        print("Не найдены файлы с сырыми данными в data/raw/")
        return
        
    latest_file = max(json_files, key=os.path.getctime)
    print(f"Читаем файл: {latest_file}")
    
    with open(latest_file, "r", encoding="utf-8") as f:
        payload = json.load(f)
        
    fetch_timestamp = payload.get("fetch_timestamp")
    protocols = payload.get("data", [])
    
    print(f"Всего протоколов в файле: {len(protocols)}")
    
    print("Подключение к Databricks...")
    connection = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN
    )
    
    cursor = connection.cursor()
    
    cursor.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
    cursor.execute("USE SCHEMA bronze;")
    
    print("Пересоздание таблицы bronze_protocols_raw...")
    cursor.execute("DROP TABLE IF EXISTS bronze_protocols_raw;")
    cursor.execute("""
        CREATE TABLE bronze_protocols_raw (
            fetch_timestamp STRING,
            protocol_id STRING,
            protocol_name STRING,
            raw_json STRING
        )
    """)
    
    print("Формирование единого пакета данных...")
    # Генерируем список значений для вставки за один запрос
    values_list = []
    for proto in protocols:
        p_id = str(proto.get("id", "")).replace("'", "''")
        p_name = str(proto.get("name", "")).replace("'", "''")
        p_json = json.dumps(proto, ensure_ascii=False).replace("'", "''")
        values_list.append(f"('{fetch_timestamp}', '{p_id}', '{p_name}', '{p_json}')")
    
    # Объединяем чанками по 1000 штук, чтобы не превысить лимиты сети/размера запроса
    chunk_size = 1000
    for i in range(0, len(values_list), chunk_size):
        chunk = values_list[i:i + chunk_size]
        values_str = ", ".join(chunk)
        insert_sql = f"INSERT INTO bronze_protocols_raw (fetch_timestamp, protocol_id, protocol_name, raw_json) VALUES {values_str}"
        
        print(f"Отправка чанка {i // chunk_size + 1}...")
        cursor.execute(insert_sql)
    
    cursor.close()
    connection.close()
    print("Успешно! Все протоколы загружены мгновенно.")

if __name__ == "__main__":
    load_latest_json_to_databricks()
