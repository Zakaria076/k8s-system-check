import subprocess
import os
import datetime

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_k8s_status():
    nodes = run_command("kubectl get nodes")
    pods = run_command("kubectl get pods --all-namespaces")
    return nodes, pods

def get_system_info():
    cpu_info = run_command("lscpu")
    memory_info = run_command("free -h")
    disk_info = run_command("df -h")
    return cpu_info, memory_info, disk_info

def generate_report():
    nodes, pods = get_k8s_status()
    cpu_info, memory_info, disk_info = get_system_info()

    report = f"""
    Kubernetes Cluster Status Report
    ================================
    Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Nodes:
    {nodes}

    Pods:
    {pods}

    System Information:
    -------------------
    CPU Info:
    {cpu_info}

    Memory Info:
    {memory_info}

    Disk Info:
    {disk_info}
    """
    return report

def save_report(report):
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_filename = os.path.join(report_dir, f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_filename, 'w') as f:
        f.write(report)
    print(f"Report saved to {report_filename}")

if __name__ == "__main__":
    report = generate_report()
    save_report(report)
