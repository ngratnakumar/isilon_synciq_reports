import os
import csv
import paramiko
from  secret import *
from datetime import datetime

policies_hdr = []
reports_hdr = []
policies_issues = []
reports_issues = []
reports_data = []

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
			tkns = each_policy.strip().split(',')
			if "Action" not in each_policy:
				name,path,action,enabled,target = str(tkns[0]), str(tkns[1]),str(tkns[2]), str(tkns[3]), str(tkns[4])
				policies_issues.append([name,path,action,enabled,target])
			else:
				policies_hdr.append(tkns)
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
					reports_issues.append([policy_name, job_id, start_time, end_time, action, state])
				reports_data.append([policy_name, job_id, start_time, end_time, action, state])
			else:
				reports_hdr.append(tkns)
			#print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as ex:
                print("... oops! , ref -->",ex)
                exit(0)

policies_list()
reports_list(reports_per_policy)

html_data=[]
def make_html_tab(hdr, body, msg):
	html_data.append(msg)
	html_data.append("<table><tr>")
	for each_hdr in hdr[0]:
		html_data.append("<th>"+str(each_hdr)+"</th>")
	html_data.append("</tr>")
	for each_body in body:
		html_data.append("<tr>")
		for each_elm in each_body:
			html_data.append("<td>"+str(each_elm)+"</td>")
		html_data.append("</tr>")
	html_data.append("</table>")
html_data.append("<html><head><style>table, th, td {  border: 1px solid black;}</style></head><body>")
make_html_tab(policies_hdr, policies_issues, "<p>All SyncIQ Policies in "+server+"</p>")
make_html_tab(reports_hdr, reports_issues, "<p>Policies with issues in "+server+"</p>")
make_html_tab(reports_hdr, reports_data, "<p>Policies reports in "+server+" ["+str(reports_per_policy)+" records per policy] </p>")
html_data.append("</body></html>")

html = ""

for ele in html_data:
	html=html.join(ele)

print(html)
