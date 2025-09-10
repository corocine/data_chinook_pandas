import pandas as pd
import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent

BASE_DIR = SCRIPT_DIR.parent

DB_PATH = BASE_DIR / 'data' / "chinook.db"
    
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor() 
query = """SELECT
        i.invoiceId,
        i.invoiceDate,
        i.total AS invoiceTotal,
        ii.invoiceLineId,
        ii.unitPrice AS itemUnitPrice,

        c.customerId,
        c.firstName AS customerFirstName,
        c.lastName AS customerLastName,
        c.company AS customerCompany,
        c.country AS customerCountry,

        e.employeeId,
        e.firstName AS employeeFirstName,
        e.lastName AS employeeLastName,
        e.title AS employeeTitle,
        e.ReportsTo AS employeeReportsTo,

        t.trackId,
        t.name AS trackName,
        t.composer,
        t.Milliseconds,

        al.title AS albumTitle,
        ar.name AS artistName,

        g.name AS genreName,
        mt.name AS mediaTypeName
    

    FROM
        invoice_items AS ii
    LEFT JOIN invoices AS i ON ii.invoiceId = i.invoiceId
    LEFT JOIN customers AS c ON i.customerId = c.customerId
    LEFT JOIN employees AS e ON c.supportRepId = e.employeeId
    LEFT JOIN tracks AS t ON ii.trackId = t.trackId
    LEFT JOIN albums AS al ON t.albumId = al.albumId
    LEFT JOIN artists AS ar ON al.artistId = ar.artistId
    LEFT JOIN genres AS g ON t.genreId = g.genreId
    LEFT JOIN media_types AS mt ON t.mediaTypeId = mt.mediaTypeId;
    """
df = pd.read_sql_query(query, conn)
conn.close()  

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
timedeltas = pd.to_timedelta(df['Milliseconds'], unit='ms')
minutos = timedeltas.dt.components.minutes
segundos = timedeltas.dt.components.seconds
df['duration'] = minutos.astype(str) + ':' + segundos.astype(str).str.zfill(2)

output_dir = BASE_DIR / 'data'
output_dir.mkdir(parents=True, exist_ok=True)
df.to_parquet(output_dir / 'chinook_processed.parquet')
