from azure.cosmos import CosmosClient, PartitionKey, exceptions
import yaml


def run():
    databases = {
        "Conf": [
            {
                "source_name": "ActionConf",
                "dest_name": "ActionConf",
                "partition_key": "/id"
            },
            {
                "source_name": "ActionDefinition",
                "dest_name": "ActionDefinition",
                "partition_key": "/id"
            },
            {
                "source_name": "EntityConf",
                "dest_name": "EntityConf",
                "partition_key": "/id"
            },
            {
                "source_name": "ParsingConf",
                "dest_name": "ParsingConf",
                "partition_key": "/id"
            },
            {
                "source_name": "ReportConf",
                "dest_name": "ReportConf",
                "partition_key": "/id"
            }
        ],
        "Salem": [
            {
                "source_name": "Alerts",
                "dest_name": "Alerts",
                "partition_key": "/date"
            },
            {
                "source_name": "Questions",
                "dest_name": "Questions",
                "partition_key": "/type"
            },
        ]
    }

    configs = load_configs()

    # create necessary db and containers
    for db_name, container_props in databases.items():
        try:
            source_db_conn = get_database(configs["source_CosmosConnection"], db_name)
            dest_db_conn = get_database(configs["dest_CosmosConnection"], db_name)
        except Exception as e:
            print(f"failed to establish necessary connections for: {db_name}")
            print(str(e))
            continue

        for cont_prop in container_props:
            try:
                print(f"---Migrating: {cont_prop['source_name']}---")
                source_cont_conn = get_container(source_db_conn, cont_prop['source_name'], cont_prop['partition_key'])
                dest_cont_conn = get_container(dest_db_conn, cont_prop['dest_name'], cont_prop['partition_key'])
                copy_container(source_cont_conn, dest_cont_conn)
                print(f"---Completed: {cont_prop['source_name']}---\n")
            except Exception as e:
                print(f"failed to copy {db_name}: {cont_prop}")
                print(str(e))

    pass


def copy_container(source_container, dest_container):
    source_items = get_items(source_container)
    print(f"     Migrating {len(source_items)} items")
    for item in source_items:
        dest_container.upsert_item(item)
    return


def get_database(connection_string, database_name):
    connection = CosmosClient.from_connection_string(connection_string)
    return connection.get_database_client(database_name)


def get_container(database, container_name, partition_key):
    try:
        return database.create_container(id=container_name, partition_key=PartitionKey(path=partition_key))
    except exceptions.CosmosResourceExistsError:
        return database.get_container_client(container_name)


def list_containers(database_client):
    return database_client.list_containers()


def get_items(container):
    return list(container.read_all_items())


def load_configs():
    with open("./connections.yml") as file_stream:
        conf = yaml.safe_load(file_stream)
    return conf


if __name__ == "__main__":
    run()
