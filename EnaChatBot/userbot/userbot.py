import asyncio
from os import getenv
from config import OWNER_ID
from dotenv import load_dotenv
from pyrogram import Client
import config


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="EnaBotsAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(getattr(config, "STRING_SESSION", "")),
            no_updates=False,
            plugins=dict(root="EnaChatBot.idchatbot"),
        )

    async def start(self):
        print(f"Starting Id chatbot...")

        if getattr(config, "STRING_SESSION", ""):
            await self.one.start()
            try:
                await self.one.join_chat("TeamXUpdate")
                await self.one.join_chat("TeamsXchat")
                await self.one.join_chat("TeamXdevs")
                await self.one.join_chat("TeamXcoders")
            except Exception:
                pass
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username

            print(f"Id-Chatbot Started as {self.one.me.first_name}")

    async def stop(self):
        try:
            if getattr(config, "STRING_SESSION", ""):
                await self.one.stop()
        except Exception:
            pass
