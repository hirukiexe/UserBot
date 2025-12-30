from telethon.tl.types import Channel, Chat
import asyncio
import random


# ==========================
# MAIN HANDLER
# ==========================
async def handle(event):
    if not event.is_reply:
        await event.reply("Reply kisi message par karo.")
        return

    client = event.client
    reply_msg = await event.get_reply_message()

    groups = await get_all_groups(client)
    total = len(groups)

    if total == 0:
        await event.reply("Koi group nahi mila.")
        return

    from_peer = reply_msg.chat_id
    message_id = reply_msg.id

    sent_status = None
    count = 1

    for group in groups:
        title = group["title"]
        chat_id = group["id"]
        to_peer = int(f"-100{chat_id}")

        delay = round(random.uniform(2.5, 4.0), 2)

        status_text = (
            f"Progress: {count}/{total}\n"
            f"Group: {title}\n"
            f"Next message will be sent in {delay} seconds."
        )

        try:
            await client.forward_messages(
                entity=to_peer,
                messages=message_id,
                from_peer=from_peer
            )
        except Exception as e:
            status_text = (
                f"Progress: {count}/{total}\n"
                f"Group: {title}\n"
                f"Status: Failed ({str(e)[:40]})"
            )

        # Send or edit status message
        if not sent_status:
            sent_status = await event.respond(status_text)
        else:
            await sent_status.edit(status_text)

        count += 1
        await asyncio.sleep(delay)

    # Final message
    await sent_status.edit(
        f"Completed\n"
        f"Total groups: {total}\n"
        f"Messages sent successfully."
    )


# ==========================
# GET ALL USER GROUPS
# ==========================
async def get_all_groups(client):
    groups = []

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        if isinstance(entity, Channel) and entity.megagroup:
            groups.append({
                "id": entity.id,
                "title": entity.title
            })

        elif isinstance(entity, Chat):
            groups.append({
                "id": entity.id,
                "title": entity.title
            })

    return groups
