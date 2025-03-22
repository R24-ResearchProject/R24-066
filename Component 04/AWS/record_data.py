import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="SeamSense",
    user="root",
    password="minu2001",
    # host="your_db_host",
    # port="your_db_port"
)
cursor = conn.cursor()

# Example of inserting defect counts
for worker_id, defect_type, defect_count, date in defect_data:
    cursor.execute("""
        INSERT INTO defect_counts (worker_id, defect_type, date, defect_count)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (worker_id, defect_type, date) 
        DO UPDATE SET defect_count = defect_counts.defect_count + EXCLUDED.defect_count
    """, (worker_id, defect_type, date, defect_count))
    conn.commit()

cursor.close()
conn.close()
