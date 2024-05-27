from pyVmomi import vim

def get_hosts_info(content):
    hosts_info = []
    for datacenter in content.rootFolder.childEntity:
        for computeResource in datacenter.hostFolder.childEntity:
            for host in computeResource.host:
                hardware = host.hardware
                summary = host.summary
                hosts_info.append({
                    'name': summary.config.name,
                    'total_ram': hardware.memorySize,
                    'used_ram': summary.quickStats.overallMemoryUsage * 1024 * 1024,
                    'free_ram': hardware.memorySize - (summary.quickStats.overallMemoryUsage * 1024 * 1024),
                    'ram_usage_percent': (summary.quickStats.overallMemoryUsage * 1024 * 1024) / hardware.memorySize * 100,
                    'total_cpu': hardware.cpuInfo.numCpuCores,
                    'used_cpu': summary.quickStats.overallCpuUsage,
                    'cpu_usage_percent': summary.quickStats.overallCpuUsage / (hardware.cpuInfo.numCpuCores * hardware.cpuInfo.hz / 1000000) * 100
                })
    return hosts_info

def get_storage_info(content):
    storage_info = []
    for datacenter in content.rootFolder.childEntity:
        for datastore in datacenter.datastore:
            summary = datastore.summary
            storage_info.append({
                'name': summary.name,
                'total_capacity': summary.capacity,
                'used_capacity': summary.capacity - summary.freeSpace,
                'free_capacity': summary.freeSpace,
                'usage_percent': (summary.capacity - summary.freeSpace) / summary.capacity * 100
            })
    return storage_info