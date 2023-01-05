# Project assignment: Data migration
- psycopg2 and sqlite3 libraries were used to create a script for migrating data to a new database.
- After applying the script, all movies, personalities and genres appear in PostgreSQL.
- All connections between records are saved.
- The code uses `dataclass`.
- Data is loaded in batches of n records.
- Restarting the script does not create duplicate entites.
- The code has write and read error handling.

# Проектное задание: перенос данных
- Использованы библиотеки psycopg2 и sqlite3, чтобы создать скрипт для миграции данных в новую базу.
- После применения скрипта все фильмы, персоны и жанры появляются в PostgreSQL.  
- Все связи между записями сохранены. 
- В коде используются `dataclass`.
- Данные загружаются пачками по n записей.
- Повторный запуск скрипта не создаёт дублирующиеся записи.
- В коде есть обработка ошибок записи и чтения.
