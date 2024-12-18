import boto3, time
data_client = boto3.client('rds-data')

def createDB():
    rds_client = boto3.client('rds')
    # User defined variables
    username = 'rdscesar001'
    password = 'U2uoelAO'
    db_subnet_group = 'vpc-hol-db-subnet-group'
    db_cluster_id = 'rds-hol-CRUD-cluster'

    # Create the DB cluster
    # With a try block we're gonna check if there is a DB cluster 
    try:
        response = rds_client.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
        print(f"The DB cluster named '{db_cluster_id}' already exists. Skipping creation.")
        
    # If not, then we create the cluster in the except block 
    except rds_client.exceptions.DBClusterNotFoundFault:
        response = rds_client.create_db_cluster(   
            Engine = 'aurora-mysql',
            EngineVersion = '5.7.mysql_aurora.2.08.3',
            DBClusterIdentifier = db_cluster_id,
            MasterUsername = username,
            MasterUserPassword = password,
            DatabaseName = 'rds_hol-crud',
            DBSubnetGroupName = db_subnet_group,
            EngineMode = 'serverless',
            EnableHttpEndpoint = True,
            ScalingConfiguration = {
                'MinCapacity' : 1, # Minimum ACU
                'MaxCapacity' : 8, # Maximum ACU
                'AutoPause' : True,
                'SecondsUntilAutoPause' : 600 # 5 minutes or 300 seconds
            }
        )
        print(f"The DB cluster named '{db_cluster_id}' has been created.")
    
        # Wait for the DB cluster to become available
        while True:
            response = rds_client.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
            status = response['DBClusters'][0]['Status']
            print(f"The status of the cluster is '{status}'.")
            if status == 'available':
                break
            print("Waiting fo the DB Cluster to become available...")
            time.sleep(40)
            
def createTable():
    results = ''
    return results

def main():
    return 'Tasks completed'
    
if __name__ == '__main__':
    main()