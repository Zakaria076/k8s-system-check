import os
import datetime
import subprocess

def run_system_checks():
    # Controleer systeeminformatie
    system_info = subprocess.check_output(['uname', '-a']).decode('utf-8')

    # Voer een vulnerability scan uit met trivy
    trivy_scan = subprocess.check_output(['trivy', 'filesystem', '/']).decode('utf-8')

    # Voer een vulnerability scan uit met kube-hunter
    kube_hunter_scan = subprocess.check_output(['kube-hunter', '--report', 'json']).decode('utf-8')

    # Genereer rapport
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.txt"
    report_path = os.path.join("reports", report_filename)

    with open(report_path, 'w') as report_file:
        report_file.write("System Information:\n")
        report_file.write(system_info + "\n")
        report_file.write("Trivy Scan Results:\n")
        report_file.write(trivy_scan + "\n")
        report_file.write("Kube-hunter Scan Results:\n")
        report_file.write(kube_hunter_scan + "\n")

    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    os.makedirs('reports', exist_ok=True)
    run_system_checks()
