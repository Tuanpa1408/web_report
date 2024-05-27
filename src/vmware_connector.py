import ssl
from pyVim.connect import SmartConnect, Disconnect
from config.vmware_config import VMWARE_CONFIG

def connect_to_vmware():
    context = ssl._create_unverified_context()
    si = SmartConnect(host=VMWARE_CONFIG['host'], user=VMWARE_CONFIG['user'], pwd=VMWARE_CONFIG['password'], sslContext=context)
    return si

def disconnect_from_vmware(si):
    Disconnect(si)
