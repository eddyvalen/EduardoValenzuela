#i found this code at https://docs.nats.io/developing-with-nats/receiving/async
nc = NATS()

async def sub(msg):
  await nc.publish(msg.reply, b'response')

await nc.connect(servers=["nats://demo.nats.io:4222"])
await nc.subscribe("time", cb=sub)

# Send the request
try:
  msg = await nc.request("time", b'', timeout=1)
  # Use the response
  print("Reply:", msg)
except asyncio.TimeoutError:
  print("Timed out waiting for response")




sub, err := nc.SubscribeSync(replyTo)
if err != nil {
    log.Fatal(err)
}

# Send the request immediately
nc.PublishRequest(subject, replyTo, []byte(input))
nc.Flush()

#// Wait for a single response
for {
    msg, err := sub.NextMsg(1 * time.Second)
    if err != nil {
        log.Fatal(err)
    }
    #this will get user input to get a certain amount of responses.
    val = input("Enter an integer to get a certain ammount of entries: ")
    response = string(val.Data)
    break
}
sub.Unsubscribe()