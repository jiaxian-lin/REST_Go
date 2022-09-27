import subprocess
import sys
tool = sys.argv[1]

services_1 = ["features-service", "languagetool", "ncs", "news", "scs"]
services_2 = ["restcountries", "scout-api", "genome-nexus", "person-controller", "proxyprint"]
services_3 = ["rest-study", "spring-batch-rest", "cwa-verification", "market", "project-tracking-system"]
services_4 = ["user-management", "genome-nexus", "ocvn", "problem-controller", "spring-boot-sample-app"]
subprocess.run("sh stop_all.sh", shell=True)
for i in range(5):
    subprocess.run("tmux kill-sess -t " + services_1[i], shell=True)
    subprocess.run("tmux kill-sess -t " + services_1[i] + "_cov", shell=True)
    subprocess.run("tmux kill-sess -t " + tool + '_' + services_1[i], shell=True)

for i in range(5):
    subprocess.run("tmux kill-sess -t " + services_2[i], shell=True)
    subprocess.run("tmux kill-sess -t " + services_2[i] + "_cov", shell=True)
    subprocess.run("tmux kill-sess -t " + tool + '_' + services_2[i], shell=True)

for i in range(5):
    subprocess.run("tmux kill-sess -t " + services_3[i], shell=True)
    subprocess.run("tmux kill-sess -t " + services_3[i] + "_cov", shell=True)
    subprocess.run("tmux kill-sess -t " + tool + '_' + services_3[i], shell=True)

for i in range(5):
    subprocess.run("tmux kill-sess -t " + services_4[i], shell=True)
    subprocess.run("tmux kill-sess -t " + services_4[i] + "_cov", shell=True)
    subprocess.run("tmux kill-sess -t " + tool + '_' + services_4[i], shell=True)