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
HELP.add_help(["plugin_add"], "Import a plugins from a git repo!",
              "Skip all the steps to add a plugins simply by run this command", args="[-b branch] [-d directory] <link-repo>")
@alemiBot.on_message(is_superuser & filterCommand(["plugin_add"], list(alemiBot.prefixes), options={"dir": ["-d"], "branch": ["-b"]}))
async def plugin_add(client, message):
    try:
        branch = message.command["branch"] if "branch" in message.command else "main"
        folder = message.command["dir"] if "dir" in message.command else ""
        link = ""

        match = None

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

        logger.info(
            f"Adding plugin → \"{match['name']}\" by dev/{match['dev']}")
        proc = await asyncio.create_subprocess_shell(
          f"git submodule add {link} plugins/{folder} && echo \"        branch = {branch}\" >> .gitmodules",
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

#HELP.add_help(["plugin_remove"], "Remove a plugin from the bot", "To see the list of plugins use .plist", args="<plugin>")
#@alemiBot.on_message(is_superuser & filterCommand(["remove"], list(alemiBot.prefixes)))
#async def plugin_remove(client, message):

HELP.add_help(["plugin_list"], "List all the installed plugin", "Yeah, list every plugin..no more..")
@alemiBot.on_message(is_superuser & filterCommand(["plugin_list"], list(alemiBot.prefixes)))
async def plugin_list(client, message):
    try:
        msg = await edit_or_reply(message, f"Listing plugins...")
        logger.info(
            f"Listing plugins...")
        proc = await asyncio.create_subprocess_shell(
          "cat .gitmodules",
          stdout=asyncio.subprocess.PIPE,
          stderr=asyncio.subprocess.STDOUT)

        stdout, stderr = await proc.communicate()
        matches = re.findall(r"\[submodule \"(?P<plugin>.*)\"]", stdout.decode())
        text = "Plugins installed:\n"
        for match in matches:
            text += match

        if text != "Plugins installed:\n":
            await edit_or_reply(message, text)

    except Exception as e:
        traceback.print_exc()
        await edit_or_reply(msg, f"`$ import`\n`[!] → ` " + str(e))