import boto3
import time
 
# Instantiate a boto3 client for RDS
rds = boto3.client('rds')

# User defined variables
username = 'dctuser21'
password = 'U2uoelAO'
db_subnet_group = 'vpc-automatingrdswithlambda-db-subnetgroup'
db_cluster_id = 'rds-AutomatingRDSwithLambda-cluster'

# Create the DB cluster
# With a try block we're gonna check if there is a DB cluster 
try:
    response = rds.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
    print(f"The DB cluster named '{db_cluster_id}' already exists. Skipping creation.")
    
# If not, then we create the cluster in the except block 
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(   
        Engine = 'aurora-mysql',
        EngineVersion = '5.7.mysql_aurora.2.08.3',
        DBClusterIdentifier = db_cluster_id,
        MasterUsername = username,
        MasterUserPassword = password,
        DatabaseName = 'rds_AutomatingRDSwithLambda_db',
        DBSubnetGroupName = db_subnet_group,
        EngineMode = 'serverless',
        EnableHttpEndpoint = True,
        ScalingConfiguration = {
            'MinCapacity' : 1, # Minimum ACU
            'MaxCapacity' : 8, # Maximum ACU
            'AutoPause' : True,
            'SecondsUntilAutoPause' : 300 # 5 minutes or 300 seconds
        }
    )
    print(f"The DB cluster named '{db_cluster_id}' has been created.")

    # Wait for the DB cluster to become available
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
        status = response['DBClusters'][0]['Status']
        print(f"The status of the cluster is '{status}'.")
        if status == 'available':
            break
        print("Waiting fo the DB Cluster to become available...")
        time.sleep(40)


# Modify the DB cluster. Update the scaling configuration for the cluster
#response = rds.modify_db_cluster(
#    DBClusterIdentifier = db_cluster_id,
#    ScalingConfiguration = {
#        'MinCapacity' : 1, # Minimum ACU
#        'MaxCapacity' : 16, # Maximum ACU
#        #'AutoPause' : True,
#        'SecondsUntilAutoPause' : 600 # 10 minutes or 300 seconds
#    }
#)
#print(f"Updated the scaling configuration for DB cluster '{db_cluster_id}'.")

# Delete the DB cluster
#response = rds.delete_db_cluster(
#    DBClusterIdentifier = db_cluster_id,
#    SkipFinalSnapshot = True
#)
#print(f"The '{db_cluster_id}' is being deleted.")