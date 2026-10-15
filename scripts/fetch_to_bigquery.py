import os
from databricks import sql
from google.cloud import bigquery

# Настройки Databricks
DATABRICKS_SERVER_HOSTNAME = "dbc-804b1d3a-hnsjgn.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/60////.........."
DATABRICKS_TOKEN = "dapi0031963aec5b39d934c4905532______"

# Настройки BigQuery
BQ_PROJECT = "defi-crypto-sandbox"
BQ_DATASET = "bronze"
BQ_TABLE = "bronze_protocols_raw"
BQ_TABLE_FULL = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
KEYFILE_PATH = "C:/Users/koverzen/.dbt/bigquery-key.json"

def sync_databricks_to_bigquery():
    print("1. Подключаемся к Databricks...")
    connection = sql.connect(
        server_hostname=DATABRICKS_SERVER_HOSTNAME,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN
    )
    
    cursor = connection.cursor()
    query = "SELECT * FROM workspace.bronze.bronze_protocols_raw"
    print(f"Выполняем запрос в Databricks: {query}")
    
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    print(f"Получено строк из Databricks: {len(rows)}")
    if not rows:
        print("Нет данных для синхронизации.")
        return

    records = [dict(zip(columns, row)) for row in rows]
    
    print(f"2. Подключаемся к BigQuery ({BQ_PROJECT})...")
    bq_client = bigquery.Client.from_service_account_json(KEYFILE_PATH)

    # Проверяем/создаем таблицу с нужной схемой перед вставкой
    table_ref = bq_client.dataset(BQ_DATASET).table(BQ_TABLE)
    try:
        bq_client.get_table(table_ref)
        print(f"Таблица {BQ_TABLE} уже существует.")
    except Exception:
        print(f"Создаем таблицу {BQ_TABLE} в BigQuery...")
        schema = [
            bigquery.SchemaField("fetch_timestamp", "STRING"),
            bigquery.SchemaField("protocol_id", "STRING"),
            bigquery.SchemaField("protocol_name", "STRING"),
            bigquery.SchemaField("raw_json", "STRING"),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        bq_client.create_table(table)
        print("Таблица успешно создана.")

    print("3. Загружаем данные в BigQuery пачками...")
    batch_size = 500
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        errors = bq_client.insert_rows_json(BQ_TABLE_FULL, batch)
        
        if errors != []:
            print(f"Ошибки на пачке {i}: {errors}")
            return
        print(f"Загружено: {min(i + batch_size, len(records))}/{len(records)}")

    print("Синхронизация Databricks -> BigQuery успешно завершена!")

if __name__ == "__main__":
    sync_databricks_to_bigquery()
