from typing import List
from gql import Client
from gql import gql
from backup_schedule_update import DAILY, WEEKLY, MONTHLY

# GraphQL query for getting volume instance backup schedule
backup_schedule_list = gql("""
query volumeInstanceBackupScheduleList($volumeInstanceId: String!) {
    volumeInstanceBackupScheduleList(volumeInstanceId: $volumeInstanceId) {
        name
        kind
    }
}
""")

def get_backup_schedule(client: Client, volume_instance_id: str) -> List[str]:
    """
    Get the backup schedule for a volume instance.
    
    Args:
        client (Client): GraphQL client instance
        volume_instance_id (str): The ID of the volume instance
        
    Returns:
        List[str]: List of backup schedule kinds (DAILY, WEEKLY, MONTHLY)
        
    Raises:
        ValueError: If volume_instance_id is empty
        Exception: If the query fails or returns invalid response
    """
    if not volume_instance_id.strip():
        raise ValueError("volume_instance_id cannot be empty")

    response = client.execute(
        document=backup_schedule_list,
        variable_values={"volumeInstanceId": volume_instance_id}
    )
    
    if not response or 'volumeInstanceBackupScheduleList' not in response:
        raise Exception("Invalid response format from API")
        
    return [schedule['kind'] for schedule in response['volumeInstanceBackupScheduleList']] 