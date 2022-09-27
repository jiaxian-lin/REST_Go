import time
import subprocess
import sys
if __name__ == "__main__":
    tool = sys.argv[1]
    time_limit = "0.1"
    port_list = []
    base_cov_port = 11000
    services_0 = ["features-service", "languagetool", "ncs"]
    services_1 = ["restcountries", "scout-api", "scs"]
    services_2 = ["problem-controller", "rest-study"]
    services_3 = ["cwa-verification", "market", "project-tracking-system"]
    services_4 = ["restcountries", "person-controller", "user-management"]
    services_5 = ["news", "genome-nexus", "spring-boot-sample-app"]
    services_6 = ["proxyprint", "spring-batch-rest"]
    for services in [services_0, services_1,services_2,services_3,services_4,services_5,services_6]:
        for i in range(len(services)):
            cov_port = base_cov_port + i*10
            port_list.append(cov_port)
            print("Running " + tool + " for " + services[i] + ": " + str(cov_port))
            session = tool + '_' + services[i]
            cov_session = services[i] + "_cov"
            subprocess.run("tmux new -d -s " + cov_session + " sh small_cov.sh " + str(cov_port), shell=True)
            cmd = "tmux new -d -s " + session + " 'timeout " + time_limit + "h python3 run_tool.py " + tool + ' ' + services[i] + ' ' + str(cov_port) + " "+time_limit+ " '"
            subprocess.run(cmd, shell=True)

        time.sleep(float(time_limit) * 60 * 60)

        subprocess.run("sh stop_all.sh", shell=True)
        for i in range(len(services)):
            subprocess.run("python3 report.py " + str(port_list[i]) + " " + services[i], shell=True)
            subprocess.run("tmux kill-sess -t " + services[i], shell=True)
            subprocess.run("tmux kill-sess -t " + services[i] + "_cov", shell=True)
            subprocess.run("tmux kill-sess -t " + tool + '_' + services[i], shell=True)
        time.sleep(float(time_limit) * 60 * 60)
