import time
import subprocess
import sys


tool = sys.argv[1]
server = sys.argv[2]
time_limit = "0.1"
base_cov_port = 11001
session = tool + '_' + server
cov_session = server + "_cov"
print("Running " + tool + " for " + server + ": " + str(base_cov_port))
subprocess.run("tmux new -d -s " + cov_session + " sh small_cov.sh " + str(base_cov_port), shell=True)

cmd = "python3 run_tool.py " + tool + ' ' + server + ' ' + str(base_cov_port) + " "+time_limit
subprocess.run(cmd, shell=True)


subprocess.run("sh stop_all.sh", shell=True)
subprocess.run("python3 report.py " + str(base_cov_port) + " " + server, shell=True)
subprocess.run("tmux kill-sess -t " + server, shell=True)
subprocess.run("tmux kill-sess -t " + server + "_cov", shell=True)
subprocess.run("tmux kill-sess -t " + tool + '_' + server, shell=True)