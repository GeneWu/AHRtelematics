import psycopg2

try:
    conn = psycopg2.connect("dbname='telematics' user='driver' password=''")
except:
    print "Not connected"
cur = conn.cursor()
print "successful connected"
