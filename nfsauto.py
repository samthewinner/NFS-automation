#!/usr/bin/python3
import cgi, cgitb , subprocess

# Create instance of FieldStorage

form = cgi.FieldStorage()

client_uname = "vboxuser"
client_ip = "192.168.0.112"
client_passwd = "changeme"
# command = ["ifconfig","enp0s3","|","awk",r"'/inet/{print $2}'","|","sed",r"'s/addr://'"]
host_ip = "192.168.0.101"

#client_uname = form.getvalue('client_uname')
#client_passwd = form.getvalue('client_passwd')
#client_ip = form.getvalue('client_ip')

#nfs server config
subprocess.run("apt install nfs-kernel-server",shell=True, check=True)
subprocess.run(f"mkdir /var/nfs/{client_uname}/general -p",shell=True, check=True)
subprocess.run(f"chown nobody:nogroup /var/nfs/{client_uname}/general",shell=True, check=True)
subprocess.run(f"echo '/var/nfs/{client_uname}/general {client_ip}(rw,sync,no_subtree_check)' > /etc/exports ",shell=True, check=True)
#subprocess.run(["systemctl" ,"restart", "nfs-kernel-server" ],shell=True, check=True)
result = subprocess.run(["systemctl","restart","nfs-kernel-server"],capture_output = True,text=True,check=True)

print("server side done")

print("Content-type:text/html")

# print(f"all commands have been executed: {op}")


#hostname = "192.168.0.112"

#uname = "vboxuser"
#password = "changeme"


#hostname = "192.168.0.112"
# host_ip = "192.168.0.101"
#uname = "vboxuser"
#password = "changeme"

command = [
    "sshpass",
    "-p", client_passwd,
    "ssh", "-o", "stricthostkeychecking=no",
    f"{client_uname}@{client_ip}",
    f"echo \"{client_passwd}\" | sudo -S mkdir -p /nfs/general",
    f"echo \"{client_passwd}\" | sudo -S mount -t nfs {host_ip}:/var/nfs/{client_uname}/general /nfs/general"
]

op = subprocess.run(command, text=True)

print("client side done")