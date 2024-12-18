from typing import Optional
from gql import Client
from gql import gql

# GraphQL query to get volume instances for an environment
environment_config = gql("""
query environment_config($environmentId: String!) {
    environment(id: $environmentId) {
        id
        volumeInstances {
            edges {
                node {
                    id
                    serviceId
                }
            }
        }
    }
}
""")

def get_volume_instance_id(client: Client, environment_id: str, service_id: str) -> str:
    """
    Get volume instance ID for a given service ID by querying the GraphQL API.
    
    Args:
        client (Client): GraphQL client instance
        environment_id (str): The environment ID that the service belongs to
        service_id (str): The service ID that the volume instance belongs to
        
    Returns:
        str: Volume instance ID
        
    Raises:
        Exception: If no volume instance is found or other errors occur
    """
    if not environment_id.strip():
        raise ValueError("environment_id cannot be empty")
    if not service_id.strip():
        raise ValueError("service_id cannot be empty")

    # Execute GraphQL query
    response = client.execute(
        document=environment_config,
        variable_values={"environmentId": environment_id}
    )
    
    # Extract volume instances from response
    if not response or 'environment' not in response:
        raise Exception("Invalid response format from API")
        
    volume_instances = response['environment']['volumeInstances']['edges']
    
    # Find matching volume instance
    for instance in volume_instances:
        if instance['node']['serviceId'] == service_id:
            return instance['node']['id']
    
    raise Exception(f"No volume instance found for service ID: {service_id}")