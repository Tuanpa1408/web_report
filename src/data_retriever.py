from pyVmomi import vim
from src.logger import logger

def get_hosts_info(content):
    hosts_info = []
    try:
        for datacenter in content.rootFolder.childEntity:
            for computeResource in datacenter.hostFolder.childEntity:
                for host in computeResource.host:
                    hardware = host.hardware
                    summary = host.summary
                    hosts_info.append({
                        'name': summary.config.name,
                        'total_ram': hardware.memorySize / (1024 * 1024 * 1024),  # Chuyển từ byte sang GB
                        'used_ram': summary.quickStats.overallMemoryUsage / 1024,  # Chuyển từ KB sang MB
                        'free_ram': (hardware.memorySize - (summary.quickStats.overallMemoryUsage * 1024 * 1024)) / (1024 * 1024 * 1024),  # Chuyển từ byte sang GB
                        'ram_usage_percent': (summary.quickStats.overallMemoryUsage / hardware.memorySize) * 100,
                        'total_cpu': hardware.cpuInfo.numCpuCores * (hardware.cpuInfo.hz / 1000000000),  # Chuyển từ Hz sang GHz
                        'used_cpu': summary.quickStats.overallCpuUsage / (1024 * 1024 * 1024),  # Chuyển từ Hz sang GHz
                        'cpu_usage_percent': (summary.quickStats.overallCpuUsage / (hardware.cpuInfo.numCpuCores * hardware.cpuInfo.hz / 1000000)) * 100
                    })
        logger.info("Successfully retrieved host information")
    except Exception as e:
        logger.error(f"Failed to retrieve host information: {e}")
    return hosts_info

def get_storage_info(content):
    storage_info = []
    try:
        for datacenter in content.rootFolder.childEntity:
            for datastore in datacenter.datastore:
                if isinstance(datastore.info.vmfs, vim.host.MountInfo):
                    summary = datastore.summary
                    # Chỉ lấy thông tin của các SAN storage
                    if summary.type == "VMFS":
                        storage_info.append({
                            'name': summary.name,
                            'total_capacity': summary.capacity / (1024 * 1024 * 1024 * 1024),  # Chuyển từ byte sang TB
                            'used_capacity': (summary.capacity - summary.freeSpace) / (1024 * 1024 * 1024 * 1024),  # Chuyển từ byte sang TB
                            'free_capacity': summary.freeSpace / (1024 * 1024 * 1024 * 1024),  # Chuyển từ byte sang TB
                            'usage_percent': ((summary.capacity - summary.freeSpace) / summary.capacity) * 100
                        })
        logger.info("Successfully retrieved storage information")
    except Exception as e:
        logger.error(f"Failed to retrieve storage information: {e}")
    return storage_info
