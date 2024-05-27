from src.vmware_connector import connect_to_vmware, disconnect_from_vmware
from src.data_retriever import get_hosts_info, get_storage_info
from src.data_saver import store_data_mysql
from src.logger import logger

def main():
    try:
        si = connect_to_vmware()
        content = si.RetrieveContent()

        hosts_info = get_hosts_info(content)
        storage_info = get_storage_info(content)

        store_data_mysql(hosts_info, storage_info)

        disconnect_from_vmware(si)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
