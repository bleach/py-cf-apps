
from flask import Flask
import os
import psycopg2
import json

app = Flask(__name__)

@app.route('/')
def show():
    header =  """<html><head>
              <style>
              td {
                width: 30%;
                border: 1px solid black;
              }
              </style>
              </head> 
              <body>"""

    return header + tuplelist_to_table(show_all()) + '</html></body>'

def tuplelist_to_table(rows):
    """Take a list of tuples containing strings.
    Return a string containing a HTML table."""
    table = '<table>\n'
    for row in rows:
        table += '<tr>'
        for col in row:
            table += '<td>%s</td>' % col
        table += '</tr>'
    table += '</table>\n'
    return table 

def show_all():
    conn = psycopg2.connect(pg_uri())
    try:
        cur = conn.cursor()
        cur.execute('SHOW ALL;')
        rows = cur.fetchall()
    finally:
        conn.close()
    return rows

def pg_uri():
    if 'VCAP_SERVICES' in os.environ:
        services = json.loads(os.getenv('VCAP_SERVICES'))
        postgres = services['postgres'][0]['credentials']['uri']
    else:
        postgres = 'dbname=graham'
    return postgres

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
