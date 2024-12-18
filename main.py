import os
from client import get_client
from get_volume_instance_id import get_volume_instance_id
from backup_schedule_update import update_backup_schedule, DAILY, WEEKLY, MONTHLY
from get_backup_schedule import get_backup_schedule

client = get_client(
    url='https://backboard.railway.app/graphql/v2',
    token=os.getenv("RAILWAY_API_TOKEN")
)

try:
    # Get volume instance ID from environment and service ids
    volume_instance_id = get_volume_instance_id(
        client,
        environment_id="7c1c3245-5321-49cd-87c5-23e502d91962",
        service_id="22dd0308-f505-4516-99fe-b858a6048d87"
    )
    
    print(f"Found volume instance ID: {volume_instance_id}")

    # Get current backup schedules to display
    schedules = get_backup_schedule(
        client,
        volume_instance_id
    )

    print("Current backup schedules:", schedules)
    
    # Enable all backup schedules
    update_backup_schedule(
        client,
        volume_instance_id,
        schedule_kinds=[DAILY, WEEKLY, MONTHLY]
    )

    print("Successfully enabled all backup schedules")

except Exception as e:
    print(f"Error: {str(e)}")