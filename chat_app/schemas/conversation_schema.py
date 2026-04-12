from datetime import datetime

def create_conversation_document(participant_ids, is_group=False, group_name=None, created_by=None):
    return {
        "participants": participant_ids,
        "is_group": is_group,
        "group_name": group_name,
        "created_by": created_by,
        "created_at": datetime.utcnow(),
        "last_message_at": datetime.utcnow()
    }