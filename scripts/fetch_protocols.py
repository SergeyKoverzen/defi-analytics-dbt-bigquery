import os
import json
import requests
from datetime import datetime

# URL официального API DeFiLlama для получения списка протоколов
API_URL = "https://api.llama.fi/protocols"
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def fetch_defi_protocols():
    print("info from DeFiLlama API...")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Добавляем метаданные о времени загрузки
        timestamp = datetime.utcnow().isoformat()
        payload = {
            "fetch_timestamp": timestamp,
            "source": "defillama",
            "endpoint": "protocols",
            "data": data
        }
        
        # Создаем папку для сырых данных, если её нет
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        
        # Формируем имя файла с текущей датой
        file_date = datetime.utcnow().strftime("%Y-%m-%d")
        file_path = os.path.join(RAW_DATA_DIR, f"protocols_{file_date}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            
        print(f"Успешно! Данные сохранены в файл: {file_path}")
        print(f"Загружено протоколов: {len(data)}")
        
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

if __name__ == "__main__":
    fetch_defi_protocols()
