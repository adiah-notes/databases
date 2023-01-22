# SQLite

Provides a convenient way to manage data without the overhead of dedicated relational databases.
SQLite is embedded into the application it serves. It's open source and truly free.

A database; programming library; command-line tool.
For programmers, it's an easy way to bind applications and their data.

If you know SQL, you'd recognize how difficult it would be to implement something like this for yourself:

```sql
SELECT x STDEV(w)
FROM table
ORDER BY x
HAVING x > MIN(2) OR x < MAX(y)
ORDER BY y DESC
LIMIT 10 OFFSET 3;
```

- [Basics of SQLite](program.md)
- [SQL for SQLite](sql.md)
