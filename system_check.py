import subprocess
import os
import datetime

def run_command(command, timeout=600):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"Command '{command}' timed out."

def get_k8s_status():
    nodes = run_command("kubectl get nodes")
    pods = run_command("kubectl get pods --all-namespaces")
    return nodes, pods

def get_system_info():
    cpu_info = run_command("lscpu")
    memory_info = run_command("free -h")
    disk_info = run_command("df -h")
    return cpu_info, memory_info, disk_info

def run_trivy_scan():
    return run_command("trivy filesystem / --no-progress", timeout=300)

def run_kube_hunter_scan():
    return run_command("kube-hunter --report json", timeout=300)

def generate_report():
    nodes, pods = get_k8s_status()
    cpu_info, memory_info, disk_info = get_system_info()
    trivy_report = run_trivy_scan()
    kube_hunter_report = run_kube_hunter_scan()

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

    Vulnerability Scan Reports:
    ---------------------------
    Trivy Report:
    {trivy_report}

    Kube Hunter Report:
    {kube_hunter_report}
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
