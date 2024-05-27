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
                        'total_ram': round(hardware.memorySize / (1024 * 1024 * 1024), 2),  # Chuyển từ byte sang GB và làm tròn đến số thập phân thứ 2
                        'used_ram': round(summary.quickStats.overallMemoryUsage / 1024, 2),  # Chuyển từ KB sang MB và làm tròn đến số thập phân thứ 2
                        'free_ram': round((hardware.memorySize - (summary.quickStats.overallMemoryUsage * 1024 * 1024)) / (1024 * 1024 * 1024), 2),  # Chuyển từ byte sang GB và làm tròn đến số thập phân thứ 2
                        'ram_usage_percent': round((summary.quickStats.overallMemoryUsage / hardware.memorySize) * 100, 2),  # Làm tròn đến số thập phân thứ 2
                        'total_cpu': round(hardware.cpuInfo.numCpuCores * (hardware.cpuInfo.hz / 1000000000), 2),  # Chuyển từ Hz sang GHz và làm tròn đến số thập phân thứ 2
                        'used_cpu': round(summary.quickStats.overallCpuUsage / (1024 * 1024 * 1024), 2),  # Chuyển từ Hz sang GHz và làm tròn đến số thập phân thứ 2
                        'cpu_usage_percent': round((summary.quickStats.overallCpuUsage / (hardware.cpuInfo.numCpuCores * hardware.cpuInfo.hz / 1000000)) * 100, 2)  # Làm tròn đến số thập phân thứ 2
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
                            'total_capacity': round(summary.capacity / (1024 * 1024 * 1024 * 1024), 2),  # Chuyển từ byte sang TB và làm tròn đến số thập phân thứ 2
                            'used_capacity': round((summary.capacity - summary.freeSpace) / (1024 * 1024 * 1024 * 1024), 2),  # Chuyển từ byte sang TB và làm tròn đến số thập phân thứ 2
                            'free_capacity': round(summary.freeSpace / (1024 * 1024 * 1024 * 1024), 2),  # Chuyển từ byte sang TB và làm tròn đến số thập phân thứ 2
                            'usage_percent': round(((summary.capacity - summary.freeSpace) / summary.capacity) * 100, 2)  # Làm tròn đến số thập phân thứ 2
                        })
        logger.info("Successfully retrieved storage information")
    except Exception as e:
        logger.error(f"Failed to retrieve storage information: {e}")
    return storage_info
