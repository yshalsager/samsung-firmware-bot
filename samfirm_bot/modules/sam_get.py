""" SamFirm Bot get updates module"""

from telethon import events, Button
from telethon.errors import MessageNotModifiedError
from telethon.tl.types import PeerChannel

from samfirm_bot import TG_BOT_ADMINS
from samfirm_bot.samfirm_bot import BOT, SF
from samfirm_bot.utils.checker import is_device, is_region


@BOT.on(events.NewMessage(pattern=r'/samget(?:@\S+)?(?: )(.*)(?: )([a-zA-Z0-9]{3})'))
async def get(event):
    """ get Samsung firmware """
    model = event.pattern_match.group(1).upper()
    region = event.pattern_match.group(2).upper()
    if event.message.sender_id not in TG_BOT_ADMINS:
        if not await is_device(model) or not await is_region(region):
            await event.reply("**Either model or region is incorrect!**")
            return
    sf_path = f"{SF.project}/{model}/{region}/"
    sf_folder = f"{SF.url}/files/{model}/{region}"
    if await SF.check(sf_path):
        message = f"**Available firmware for {model} ({region}):**\n\n"
        for item in await SF.sftp.listdir(sf_path):
            if item.startswith('.'):
                continue
            message += f"[{item}]({sf_folder}/{item})\n"
        await event.reply(message)
    else:
        await event.reply(f"**There is no available firmware for {model} ({region}) yet\n"
                          f"However, you can submit a request using the button below**",
                          buttons=[
                              Button.inline("Request Firmware", data=f"request_{model}_{region}")
                          ])


@BOT.on(events.CallbackQuery(data=lambda d: d.startswith(b'request')))
async def request(event):
    """request a firmware"""
    params = event.data.decode("utf-8")
    model = params.split('_')[1]
    region = params.split('_')[2]
    entity = await BOT.get_entity(PeerChannel(1348663969))
    message = f"**New Firmware request**!\n\n" \
              f"**Device: {model}\n" \
              f"**Region: {region}\n\n" \
              f"`/samup {model} {region}`"
    await BOT.send_message(entity, message)
    try:
        await event.edit(
            "**Your request has been submitted.**\n"
            "Join @samsungfws to get notified when your request is processed.",
            buttons=Button.clear())
    except MessageNotModifiedError:
        pass
