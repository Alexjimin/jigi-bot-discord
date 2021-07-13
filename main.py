from tcp_latency import measure_latency
from dotenv import load_dotenv
import discord, time, threading, asyncio, os


client = discord.Client()


async def change_name(new_name):
    channel = client.get_channel(864328756956758017)
    await channel.edit(name=new_name)


server_status = False


async def pingjigia():
    global server_status
    channel = client.get_channel(864328756956758017)
    while True:
        print(server_status)
        for i in range(5):
            packet = measure_latency(
                host="14.36.69.97", port=25565, runs=1, timeout=2.5
            )[0]
            if packet != None:
                print(packet)
                server_status = True
                await channel.edit(name="마크 서버 열림")
                break
        else:
            print("BUG")
            server_status = False
            await channel.edit(name="마크 서버 닫힘")

        await asyncio.sleep(60)


async def pingjigi(message):
    for i in range(5):
        await message.channel.send(
            f"`send packet {i+1}: 192.0.0.1 -> 14.36.69.97:25565`"
        )
        packet = measure_latency(host="14.36.69.97", port=25565, runs=1, timeout=2.5)[0]
        print(packet)
        if packet != None:
            await message.channel.send("`직이섭(14.36.69.97) 열림`")
            return
        await message.channel.send("`핑 확인 실패`")

    await message.channel.send("`직이섭(14.36.69.97) 열리지 않음`")


@client.event
async def on_ready():
    print(f"Logged in as {client}")
    fnon = asyncio.ensure_future(pingjigia())
    loop = asyncio.get_event_loop()
    loop.run_forever()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    args = message.content.split(" ")
    if message.content.startswith("직이섭"):
        await message.channel.send("확인중...")
        await pingjigi(message)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
