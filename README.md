# Fetch rom info

Script for fetching rom info from freeroms.com.

It fetches rom name and download page url, then stores information
into a sqlite3 database named 'rom_info.db'.

'rom_info.db' has a table named 'rom_info' which created by the statement below:

```python
cur.execute("CREATE TABLE rom_info(id integer PRIMARY KEY, name TEXT, \
	download_page TEXT, download_url TEXT, rom_type TEXT, description TEXT)")
```