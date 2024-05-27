import mysql.connector
from config.db_config import DB_CONFIG
from datetime import datetime

def store_data_mysql(hosts_info, storage_info):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    check_time = datetime.now()

    # Bảng RAM
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS RAM (
            id INT AUTO_INCREMENT PRIMARY KEY,
            host_name VARCHAR(255),
            total_ram BIGINT,
            used_ram BIGINT,
            free_ram BIGINT,
            ram_usage_percent FLOAT,
            check_time DATETIME
        )
    """)

    for host in hosts_info:
        cursor.execute("""
            INSERT INTO RAM (host_name, total_ram, used_ram, free_ram, ram_usage_percent, check_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (host['name'], host['total_ram'], host['used_ram'], host['free_ram'], host['ram_usage_percent'], check_time))

    # Bảng CPU
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CPU (
            id INT AUTO_INCREMENT PRIMARY KEY,
            host_name VARCHAR(255),
            total_cpu INT,
            used_cpu INT,
            cpu_usage_percent FLOAT,
            check_time DATETIME
        )
    """)

    for host in hosts_info:
        cursor.execute("""
            INSERT INTO CPU (host_name, total_cpu, used_cpu, cpu_usage_percent, check_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (host['name'], host['total_cpu'], host['used_cpu'], host['cpu_usage_percent'], check_time))

    # Bảng Storage
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Storage (
            id INT AUTO_INCREMENT PRIMARY KEY,
            datastore_name VARCHAR(255),
            total_capacity BIGINT,
            used_capacity BIGINT,
            free_capacity BIGINT,
            usage_percent FLOAT,
            check_time DATETIME
        )
    """)

    for storage in storage_info:
        cursor.execute("""
            INSERT INTO Storage (datastore_name, total_capacity, used_capacity, free_capacity, usage_percent, check_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (storage['name'], storage['total_capacity'], storage['used_capacity'], storage['free_capacity'], storage['usage_percent'], check_time))

    conn.commit()
    cursor.close()
    conn.close()
