# libs/tag_utils.py

async def get_group_members_jids(client, group_jid):
    """
    Returns a list of member JIDs and numbers for a group.
    """
    members = await client.get_group_members(group_jid)
    jids = [member.jid for member in members]
    numbers = [member.number for member in members]
    return jids, numbers


def format_mention(jid: str, display: str = None) -> dict:
    """
    Returns text and context_info for mentioning a single user.
    display: what to show in text (optional, defaults to number)
    """
    text = f"@{display or jid.split('@')[0]}"
    context_info = {"mentioned_jid": [jid]}
    return {"text": text, "context_info": context_info}


def format_mentions(jids: list, displays: list = None) -> dict:
    """
    Returns text and context_info for mentioning multiple users.
    displays: list of names/numbers to show in text (optional)
    """
    if displays and len(displays) != len(jids):
        displays = None  # fallback to JID numbers if mismatch
    text_list = [f"@{d}" for d in (displays or [j.split('@')[0] for j in jids])]
    return {"text": " ".join(text_list), "context_info": {"mentioned_jid": jids}}
