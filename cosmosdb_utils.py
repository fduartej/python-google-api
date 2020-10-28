from azure.cosmos import exceptions, CosmosClient, PartitionKey

class CosmosDBContext:
    client = None

    def __init__(self,end_point,key):
        self.client = CosmosClient( 
            end_point,
            key)
    
    def get_cosmosdb_container(self,database,container_name,partition_key):
        database = self.client.create_database_if_not_exists(
            id=database)
        container = database.create_container_if_not_exists(
            id=container_name, 
            partition_key=PartitionKey(
                path=partition_key
                ),
            offer_throughput=400
        )
        
        return container

class Setting:
    COSMOS_END_POINT=""
    COSMOS_KEY="=="
    COSMOS_DATABASE="DueDiligence"
    COSMOS_CONTAINER_SETUP="SetupContainer"
    COSMOS_CONTAINER_SETUP_PARTITION_KEY="setup"
    COSMOS_CONTAINER_TRACK="EvaluationContainer"
    COSMOS_CONTAINER_TRACK_PARTITION_KEY="customer"