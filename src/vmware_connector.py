import ssl
from pyVim.connect import SmartConnect, Disconnect
from config.vmware_config import VMWARE_CONFIG
from src.logger import logger

def connect_to_vmware():
    try:
        context = ssl._create_unverified_context()
        si = SmartConnect(host=VMWARE_CONFIG['host'], user=VMWARE_CONFIG['user'], pwd=VMWARE_CONFIG['password'], sslContext=context)
        logger.info("Successfully connected to VMware vCenter")
        return si
    except Exception as e:
        logger.error(f"Failed to connect to VMware vCenter: {e}")
        raise

def disconnect_from_vmware(si):
    try:
        Disconnect(si)
        logger.info("Successfully disconnected from VMware vCenter")
    except Exception as e:
        logger.error(f"Failed to disconnect from VMware vCenter: {e}")
