import requests
import bs4
import ast

#A1 Start
#I am connecting to this site so that I can scrape the quotes from the website.
res = requests.get("https://friends-quotes-api.herokuapp.com/quotes")

#converted the quotes from a string to a dictionary
clean_text = res.text[1:-1]
dic = ast.literal_eval(clean_text)

#i found this code at https://docs.nats.io/developing-with-nats/sending/structure by googling how to send data to nats
#My code doesnt work after this.
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"])

for quote_actor in dic:
    await nc.publish("updates", json.dumps({'quote': quote_actor['quote'], 'character': quote_actor['character'] }).encode())
#A1 End
    
#I took this code from https://docs.nats.io/developing-with-nats/receiving/async
#this cod is supposed to subscribe to Updates and get messages from it
#A2 Start
async def cb(msg):
  nonlocal future
  future.set_result(msg)
    
await nc.subscribe("updates", cb=cb)
await nc.publish("updates", b'All is Well')
await nc.flush()

# Wait for message to come in
msg = await asyncio.wait_for(future, 1)

#convert message to dictionary
data = ast.literal_eval(msg)

#this is supposed to add the message from NATS to a Postgresql table
from psycopg2.extensions import AsIs
cur = conn.cursor()
cur.executemany("""INSERT INTO bar(quote,character) VALUES (%(quote)s, %(character)s)""", data)

#A2 end
await nc.close()