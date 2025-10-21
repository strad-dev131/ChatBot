
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from EnaChatBot import EnaChatBot as app, LOGGER
from config import UPDATE_CHNL as MUST_JOIN

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://envs.sh/EuZ.jpg",
                    caption=(f"**👋 ʜᴇʟʟᴏ {msg.from_user.mention},**\n\n**ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ [ᴄʜᴀɴɴᴇʟ]({link}) ᴛᴏ sᴇɴᴅ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ʙᴏᴛ.**"),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("๏ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ๏", url=link)]]))
        
                # Stop further processing by returning early
                return
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        LOGGER.warning(f"Promote me as admin in required chat: {MUST_JOIN}")
