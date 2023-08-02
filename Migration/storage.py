from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableClient, TableServiceClient
import yaml


def run():
    configs = load_configs()
    salem_tables = ["alertFilter", "defaultContextLookup"]     # TODO only these tables will be migrated

    # fetch list of tables from the source
    source_client = table_service_client(configs["source_AzureWebJobsStorage"])
    source_tables = list_tables(source_client)
    source_client.close()

    tables_to_migrate = [table for table in salem_tables if table in source_tables]

    print(f"Preparing to migrate tables {tables_to_migrate}")

    # migrating alertFilter TODO
    for table in tables_to_migrate:
        copy_table(table, configs)

    return


def table_service_client(connection_string):
    return TableServiceClient.from_connection_string(connection_string)


def table_client(connection_string, table):
    return TableClient.from_connection_string(connection_string, table)


def list_tables(client):
    """
    list all tables in the Salem storage account
    """
    try:
        return [t.name for t in client.list_tables()]
    except Exception as e:
        print(f"Error connecting to table service. check connection string: {str(e)}")


def copy_table(table_name, configs):
    print(f"----Migrating {table_name}----")

    # dest_table_name = table_name + "MigTest"
    dest_table_name = table_name

    source_table_client = table_client(configs["source_AzureWebJobsStorage"], table_name)
    source_entities = source_table_client.list_entities()

    dest_table_client = table_client(configs["source_AzureWebJobsStorage"], dest_table_name)
    try:
        dest_table_client.create_table()
    except ResourceExistsError:
        print(f"{table_name} table already exists")
    except ResourceExistsError as e:
        print(f"Error occurred while creating table {table_name}")
        print(str(e))

    # prepare batches grouped by PartitionKey
    batches = {}
    for item in list(source_entities):
        key = item['PartitionKey']
        if key not in batches.keys():
            batches[key] = []

        batches[key].append(("upsert", item))

    try:
        for key, entities in batches.items():
            dest_table_client.submit_transaction(entities)
            print(f"Batch insert completed for PartitionKey: {key}")

        source_table_client.close()
        dest_table_client.close()
        print(f"----Completed migrating {table_name}----")
    except Exception as e:
        print(f"Failed to migrate table: {table_name}. \n")
        print(str(e))


def load_configs():
    with open("./connections.yml") as file_stream:
        conf = yaml.safe_load(file_stream)
    return conf


if __name__ == "__main__":
    run()
