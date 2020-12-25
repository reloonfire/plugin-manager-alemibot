# Wrapping like with a super car
from bot import alemiBot

import asyncio
import re
import logging
import traceback
import io

from pyrogram import filters
from util.command import filterCommand
from util.parse import cleartermcolor
from util.message import tokenize_json, tokenize_lines, is_me, edit_or_reply
from util.serialization import convert_to_dict
from util.permission import is_superuser
from plugins.help import HelpCategory

logger = logging.getLogger(__name__)

HELP = HelpCategory("Plugins")
HELP.add_help(["import"], "Import a plugins from a git repo!",
              "Skip all the steps to add a plugins simply by run this command", args="[-b branch] [-d directory] <link-repo>")


@alemiBot.on_message(is_superuser & filterCommand(["import"], list(alemiBot.prefixes), options={"dir": ["-d"], "branch": ["-b"]}))
async def plugin_add(client, message):
    branch = ""
    folder = ""
    link = ""

    match = None

    if message.command["dir"]:
        folder = message.command["dir"]

    if message.command["branch"]:
        branch = message.command["branch"]
    else:
        branch = "main"

    if "arg" in message.command:
        link = message.command["arg"]
        match = re.search(
            r"https:\/\/github.com\/(?P<dev>.*)\/(?P<name>.*).git", link)
        if match is None:
            return await edit_or_reply(message, "`[!] → ` The link given is incorrect")
        else:
            if folder == "":
                folder = match["name"]
    else:
        return await edit_or_reply(message, "`[!] → ` No link provided")

    msg = await edit_or_reply(message, f"Adding plugin → \"{match['name']}\" by dev/{match['dev']}")
    try:
        logger.info(
            f"Adding plugin → \"{match['name']}\" by dev/{match['dev']}")
        proc = await asyncio.create_subprocess_shell(
            f"git submodule add {link} plugins/{folder}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT)

        await asyncio.create_subprocess_shell(
            f"echo \"        branch = {branch}\" >> .gitmodules",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT)

        stdout, stderr = await proc.communicate()
        output = cleartermcolor(stdout.decode())
        if len(output) > 4080:
            await msg.edit(f"```$ import\n → Output too long, sending as file```")
            out = io.BytesIO((f"$ import\n" + output).encode('utf-8'))
            out.name = "output.txt"
            await client.send_document(message.chat.id, out)
        else:
            await msg.edit(tokenize_lines(f"$ import\n\n" + output, mode='html'), parse_mode='html')

    except Exception as e:
        traceback.print_exc()
        await edit_or_reply(msg, f"`$ import`\n`[!] → ` " + str(e))
