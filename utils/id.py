import uuid


def generate_uuid():
    return str(uuid.uuid4()).upper().replace('-', '')[:8]
