from typing import List
from gql import Client
from gql import gql

# Backup schedule kinds
DAILY = "DAILY"
WEEKLY = "WEEKLY"
MONTHLY = "MONTHLY"

# All available backup schedule kinds
ALL_BACKUP_KINDS = [DAILY, WEEKLY, MONTHLY]

# GraphQL mutation for updating volume instance backup schedule
backup_schedule_update = gql("""
mutation volumeInstanceBackupScheduleUpdate($volumeInstanceId: String!, $kinds: [VolumeInstanceBackupScheduleKind!]!) {
    volumeInstanceBackupScheduleUpdate(
        volumeInstanceId: $volumeInstanceId
        kinds: $kinds
    )
}
""")

def update_backup_schedule(
    client: Client,
    volume_instance_id: str,
    schedule_kinds: List[str] = ALL_BACKUP_KINDS
) -> None:
    """
    Update the backup schedule for a volume instance.
    
    Args:
        client (Client): GraphQL client instance
        volume_instance_id (str): The ID of the volume instance to update
        schedule_kinds (List[str]): List of backup schedule kinds. Defaults to all kinds.
                                  Use DAILY, WEEKLY, MONTHLY constants for valid values.
        
    Raises:
        ValueError: If volume_instance_id is empty or any schedule kind is invalid
        Exception: If the update fails or returns invalid response
    """
    if not volume_instance_id.strip():
        raise ValueError("volume_instance_id cannot be empty")
    if not schedule_kinds:
        raise ValueError("schedule_kinds cannot be empty")

    # Validate schedule kinds
    invalid_kinds = [kind for kind in schedule_kinds if kind not in ALL_BACKUP_KINDS]
    if invalid_kinds:
        raise ValueError(f"Invalid backup schedule kind(s): {invalid_kinds}")

    response = client.execute(
        document=backup_schedule_update,
        variable_values={
            "volumeInstanceId": volume_instance_id,
            "kinds": schedule_kinds
        }
    )
    
    if not response or 'volumeInstanceBackupScheduleUpdate' not in response:
        raise Exception("Invalid response format from API")
        
    if not response['volumeInstanceBackupScheduleUpdate']:
        raise Exception("Failed to update backup schedule")