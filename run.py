import time
import subprocess
import sys
if __name__ == "__main__":
    tool = sys.argv[1]
    total_time = sys.argv[2]
    time_limit = "1"
    services_0 = ["features-service", "languagetool", "ncs","news", "genome-nexus","cwa-verification"]
    services_1 = ["restcountries", "scout-api", "scs", "spring-boot-sample-app", "market"]
    services_2 = [ "rest-study","proxyprint", "person-controller", "spring-batch-rest", "project-tracking-system"]
    server_list = [services_0, services_1, services_2]
    subprocess.run("mkdir -p experiment/"+tool, shell=True)
    port_list = []
    base_cov_port = 11000
    for current_time in range(int(total_time)):
        for services in server_list:
            for i in range(len(services)):
                cov_port = base_cov_port + i*10
                port_list.append(cov_port)
                print("Running " + tool + " for " + services[i] + ": " + str(cov_port))
                session = tool + '_' + services[i]
                cov_session = services[i] + "_cov"
                subprocess.run("tmux new -d -s " + cov_session + " sh get_cov.sh " + str(cov_port), shell=True)
                cmd = "tmux new -d -s " + session + " 'python3 run_tool.py " + tool + ' ' + services[i] + ' ' + str(cov_port) + " "+time_limit+ " '"
                subprocess.run(cmd, shell=True)
                time.sleep(5)

            time.sleep(float(time_limit)*60*61)
            time.sleep(60)
            subprocess.run("sh stop_all.sh", shell=True)
            for i in range(len(services)):
                target_dir = f"experiment/{tool}/{current_time}/{services[i]}"
                subprocess.run("mkdir -p " + target_dir, shell=True)
                subprocess.run("python3 report.py " + str(port_list[i]) + " " + services[i], shell=True)
                time.sleep(5)
                subprocess.run(f"mv data/{services[i]}/res.csv {target_dir} -f", shell=True)
                if tool == "evomaster-blackbox":
                    subprocess.run(f"mv {tool}/{services[i]}/result.txt {target_dir} -f", shell=True)
                elif tool == "evomaster-whitebox":
                    subprocess.run(f"mv {tool}/{services[i]}/result.txt {target_dir} -f", shell=True)
                elif tool == "foREST":
                    subprocess.run(f"mv foREST/log/{services[i]}/summery.txt {target_dir} -f", shell=True)
                subprocess.run("tmux kill-sess -t " + services[i], shell=True)
                subprocess.run("tmux kill-sess -t " + services[i] + "_cov", shell=True)
                subprocess.run("tmux kill-sess -t " + tool + '_' + services[i], shell=True)
            time.sleep(10)
