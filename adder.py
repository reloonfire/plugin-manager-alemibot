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
          f"git submodule add -b {branch} {link} plugins/{folder}",
          stdout=asyncio.subprocess.PIPE,
          stderr=asyncio.subprocess.STDOUT)

        stdout, stderr = await proc.communicate()
        output = cleartermcolor(stdout.decode())
        await msg.edit(f"[✓]{link} by {match['dev']} installed!")

    except Exception as e:
        traceback.print_exc()
        await edit_or_reply(msg, f"`$ plugin_add`\n`[!] → ` " + str(e))

HELP.add_help(["plugin_remove"], "Remove a plugin from the bot", "To see the list of plugins use .plugin_list", args="<plugin>")
@alemiBot.on_message(is_superuser & filterCommand(["plugin_remove"], list(alemiBot.prefixes)))
async def plugin_remove(client, message):
    try:
        plugin = ""
        if "arg" not in message.command:
            return await edit_or_reply(message, "`[!] → ` No plugin provided")
        else:
            plugin = message.command["arg"]
        
        logger.info(
            f"Removing plugin → \"{plugin}\"")
        proc = await asyncio.create_subprocess_shell(
          f"git submodule deinit -f {plugin} && rm -rf .git/modules/{plugin} && git rm -f {plugin}",
          stdout=asyncio.subprocess.PIPE,
          stderr=asyncio.subprocess.STDOUT)

        stdout, stderr = await proc.communicate()
        await edit_or_reply(message, f"{plugin} removed!")
    except Exception as e:
        traceback.print_exc()
        await edit_or_reply(message, f"`$ plugin_remove`\n`[!] → ` " + str(e))

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
            text += match + "\n"

        if text != "Plugins installed:\n":
            await edit_or_reply(message, text)
        else:
            await edit_or_reply(message, "No plugins found.")

    except Exception as e:
        traceback.print_exc()
        await edit_or_reply(msg, f"`$ plugin_list`\n`[!] → ` " + str(e))