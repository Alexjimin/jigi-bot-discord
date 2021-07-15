from tcp_latency import measure_latency
from dotenv import load_dotenv
import datetime, nest_asyncio
import discord, time, threading, asyncio, os, logging

nest_asyncio.apply()

jigiip = "14.36.69.85"
timestamp = datetime.date.today()
logpath = f"C:/Users/alexj/Documents/dev/jigibot/jigi-bot-discord/log/{timestamp}"
filenumber = 0
while os.path.exists(f"{logpath}-{filenumber}.txt"):
    filenumber += 1
logpath = f"{logpath}-{filenumber}.txt"
f = open(logpath, "w")
logging.basicConfig(
    filename=logpath,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logging.debug("log start")

client = discord.Client()


async def change_name(new_name):
    channel = client.get_channel(864328756956758017)
    await channel.edit(name=new_name)


server_status = False


async def pingjigia():
    print("wtf?")
    global server_status
    channel = client.get_channel(864328756956758017)
    commchannel = client.get_channel(779347281744756759)
    while True:
        print("pingjigia called")
        for i in range(5):
            logging.info("Ping To Jigi Server")
            print("ping to jigisv")
            packet = measure_latency(host=jigiip, port=25565, runs=1, timeout=2.5)[0]
            print("ping sent to jigisv")
            print(packet)
            if packet != None:
                logging.info(f"Packet From Jigi Server {packet}ms")
                print("packet isnt none")
                if server_status == False:
                    # await commchannel.send("@마인크래프트 서버 오픈")
                    await channel.edit(name="🟢ㅣ직이섭 열림")
                    logging.info("Jigi Server Is UP")
                server_status = True
                break
        else:
            print("packet is none")
            if server_status == True:
                await commchannel.send("@마인크래프트 서버 다운")
                await channel.edit(name="🔴ㅣ직이섭 닫힘")
                logging.info("Jigi Server Is DOWN")
            server_status = False
        print(server_status)
        print("repeating soon...")
        await asyncio.sleep(10)


async def pingjigi(message):
    for i in range(5):
        await message.channel.send(f"`send packet {i+1}: 192.0.0.1 -> {jigiip}:25565`")
        packet = measure_latency(host=jigiip, port=25565, runs=1, timeout=2.5)[0]
        print(packet)
        if packet != None:
            await message.channel.send(f"`직이섭({jigiip}:25565) 열림`")
            return
        await message.channel.send("`핑 확인 실패`")

    await message.channel.send(f"`직이섭({jigiip}:25565) 열리지 않음`")


@client.event
async def on_ready():
    print(f"Logged in as {client}")
    await change_name("🔴ㅣ직이섭 닫힘")
    fnon = asyncio.ensure_future(pingjigia())
    loop = asyncio.get_event_loop()
    loop.run_forever()


@client.event
async def on_message(message):
    global jigiip
    if message.author == client.user:
        return

    args = message.content.split(" ")
    print(args)
    if args[0] == "직이섭":
        await message.channel.send("확인중...")
        await pingjigi(message)
    elif args[0] == "직이섭-ip" or args[0] == "wlrdltjq-ip":
        await message.channel.send(
            f"직이섭 IP({jigiip})를 임시적으로 {args[1]} 로 바꿉니다. IP는 다시 키면 초기화되니 봇 제작자한테 요청하세요."
        )
        jigiip = args[1]


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
