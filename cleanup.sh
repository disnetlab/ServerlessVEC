ps -ef| grep "python3 sumilateTrafficContainernet.py"| grep -v "grep"| awk '{print $2}'| xargs sudo kill -9; sudo mn -c
