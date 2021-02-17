import subprocess
import os


#subprocess.run("ls -l")

res = subprocess.check_output(["ls", "-l"], universal_newlines=True)

print("ici "+res)
# for line in res.splitlines():
#     # process the output line by line

#     print("ici "+str(line))



# os.system('ls -l')
# decrypt command
# os.system