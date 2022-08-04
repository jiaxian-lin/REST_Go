import time
import subprocess
import sys
if __name__ == "__main__":
    tool = sys.argv[1]
    time_limit = "0.1"
    port_list = []
    base_cov_port = 11000
    services = ["features-service", "languagetool", "ncs", "news", "restcountries"]
    services_2 = ["restcountries", "scout-api", "scs", "genome-nexus", "person-controller"]
    services_3 = ["problem-controller", "rest-study", "spring-batch-rest", "spring-boot-sample-app", "user-management"]
    services_4 = ["cwa-verification", "market", "project-tracking-system", "proxyprint"]
    for i in range(5):
        cov_port = base_cov_port + i*10
        port_list.append(cov_port)
        print("Running " + tool + " for " + services[i] + ": " + str(cov_port))
        session = tool + '_' + services[i]
        cov_session = services[i] + "_cov"
        subprocess.run("tmux new -d -s " + cov_session + " sh small_cov.sh " + str(cov_port), shell=True)
        cmd = "tmux new -d -s " + session + " 'timeout " + time_limit + "h python3 run_tool.py " + tool + ' ' + services[i] + ' ' + str(cov_port) + " "+time_limit+ " '"
        subprocess.run("tmux new -d -s " + session + " 'timeout " + time_limit + "h python3 run_tool.py " + tool + ' ' + services[i] + ' ' + str(cov_port) + " "+time_limit+ " '", shell=True)

    time.sleep(float(time_limit) * 60 * 60)

    subprocess.run("sh stop_all.sh", shell=True)
    for i in range(5):
        subprocess.run("python3 report.py " + str(port_list[i]) + " " + services[i], shell=True)
        subprocess.run("tmux kill-sess -t " + services[i], shell=True)
        subprocess.run("tmux kill-sess -t " + services[i] + "_cov", shell=True)
        subprocess.run("tmux kill-sess -t " + tool + '_' + services[i], shell=True)
