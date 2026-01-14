import os
import sys
import hashlib
import mysql.connector

def main():
    conn = mysql.connector.connect(
        host=os.getenv('IP_ADDRESS', 'mariadb'),
        port=int(os.getenv('MARIADB_PORT', '3306')),
        user=os.environ.get('MARIADB_USER'),
        password=os.environ.get('MARIADB_PASSWORD'),
        database=os.environ.get('MARIADB_DATABASE')
    )
    cursor = conn.cursor()
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `server_migrations` (
          `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
          `migration_name` varchar(255) NOT NULL,
          `applied_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `migration_name` (`migration_name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    conn.commit()
    
    # Get already applied migrations
    cursor.execute("SELECT migration_name FROM server_migrations")
    applied = {row[0] for row in cursor.fetchall()}
    
    # Get migration files from same directory as script
    migrations_dir = os.path.dirname(os.path.abspath(__file__))
    migrations_dir = os.path.join(migrations_dir, 'migrations')
    migration_files = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith('.sql') and not f.startswith('.')
    ])
    
    # Apply pending migrations
    pending = [f for f in migration_files if f not in applied]
    
    print(f"Applying {len(pending)} pending migrations.\n")
    
    for filename in pending:
        filepath = os.path.join(migrations_dir, filename)
        print(f"-> Applying {filename}.")
        
        try:
            with open(filepath, 'r') as f:
                sql = f.read()
            
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            
            cursor.execute("INSERT INTO server_migrations (migration_name) VALUES (%s)", (filename,))
            conn.commit()
            
        except Exception as e:
            print(f"Failed: {e}")
            conn.rollback()
            conn.close()
            sys.exit(1)
    
    print(f"Successfully applied {len(pending)} migrations")
    
    conn.close()

if __name__ == "__main__":
    main()

