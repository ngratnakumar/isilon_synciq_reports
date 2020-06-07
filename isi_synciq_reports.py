import os
import csv
import paramiko
from  secret import *
from datetime import datetime

def run_isi_command(cmd_to_execute):
	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(server, username=username, password=password)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
		stdout = ssh_stdout.readlines()
		ssh.close()
		return stdout
	except Exception as ex:
		print("oops! ... ", ex)

def policies_list():
	command="isi sync policies list --format=csv"
        try:
		policies = run_isi_command(command) # list in CSV format
		for each_policy in policies:
			print(each_policy.strip())
	except Exception as ex:
		print("... oops! , ref -->",ex)
		exit(0)

def reports_list(reports_per_policy):
	command="isi sync reports list --reports-per-policy={} --format=csv".format(reports_per_policy)
        try:
                policies = run_isi_command(command) # list in CSV format
                for each_policy in policies:
                        tkns = each_policy.strip().split(',')
			if "Start" not in each_policy:
				policy_name,job_id,action,state = str(tkns[0]), str(tkns[1]), str(tkns[4]), str(tkns[5])
				start_time, end_time = float(tkns[2]), float(tkns[3])
				start_time = datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
				end_time = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
				if state == "needs_attention" or state == "failed":
					print(policy_name, job_id, start_time, end_time, action, state)
			else:
				print(tkns)
			#print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as ex:
                print("... oops! , ref -->",ex)
                exit(0)

policies_list()
reports_list(2)
