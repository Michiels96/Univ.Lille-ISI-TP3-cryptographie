import subprocess


res = subprocess.check_output(["ls", "-l"], universal_newlines=True)
res = res.split('\n')
print("ici "+str(res))