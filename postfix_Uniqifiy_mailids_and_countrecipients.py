#!/usr/bin/python
#script by tom burton


#arg1 = input file
#arg2 = output  file
#arg3 = this many or more emails per recipient is worth reporting


import re
import sys
import os
from collections import defaultdict

def uniqify(fname):
    searchterm = "client=ip"
     #this string only appears in the first line of a mail's log chunk
    mailids_dict = {} #dictionary for mail ids and no. of times they occur
    linelist = []
    pattern = re.compile('^(.*)' + searchterm + '(.*)$')
    outputlog = f'{fname}{"_uniq-out.log"}'
    open(outputlog, 'w').close() #empty the output file before writing
    with open(fname) as f:
        for (i, line) in enumerate(f):
            match = pattern.match(line)
            mailid=(line.split(":")[3])
            if match is not None:
                if mailid not in mailids_dict:
                    mailids_dict[mailid] = 1
                    #if it's not yet in the dict it must be unique so far,
                    # so don't change the line
                    write_out(line, outputlog)
                else:
                    #on a matched line: if it's in the dict then
                    #it has been used before in another mail's log chunk
                    idcount=mailids_dict[mailid]
                    idcount += 1
                    mailids_dict[mailid] = idcount
                    #concat the occurence count to the mail id, replace it
                    #in the line and write out the new version
                    newmailid = f'{mailid}{mailids_dict[mailid]}'
                    newline = line.replace(mailid, newmailid)
                    write_out(newline, outputlog)
            else:
                if mailid in mailids_dict and mailids_dict[mailid] > 1:
                    #if it's in the dict and the count is more than one,
                    #then update the mailid
                    newmailid = f'{mailid}{mailids_dict[mailid]}'
                    newline = line.replace(mailid, newmailid)
                    write_out(newline, outputlog)
                else:
                    write_out(line, outputlog)
    return outputlog

def write_out(lineout, fileout):
    with open(fileout, 'a') as g:
        g.write(lineout)


def list_edm_to_address(inputfile, outputfile):
    pattern_from = re.compile("^(.*)qmgr.*from=<edm")
    pattern_subject = re.compile("header Subject:.*$")
    msg_count_file = outputfile
    open(msg_count_file, 'w').close()
    edm_mailids = []
    emails_dict = {}
    subject_mailid_dict = {}
    subject_toaddress_dict = collections.defaultdict(list)
    tmp_emails_dict = {}
    sorted_emails = {}
    num_mails = int(sys.argv[3]) #this many or more emails are worth reporting
    with open(inputfile) as f:
        for line in f:
            match_from = pattern_from.match(line)
            line_mailid = line.split(":")[3]
            if match_from is not None: #is it a "from" line?
                edm_mailids.append(line_mailid) #then add the mail id to the list
            elif line_mailid in edm_mailids: #if it's an edm mail id, process it
                pattern_to = re.compile("^(.*)smtp\[.+" + line_mailid + ": to=<(.*)$")
                match_to = pattern_to.match(line)
                match_subject = pattern_subject.match(line)
                if match_subject is not None: #if it's a subject line, put it in the array
                    subject_mailid_dict[line_mailid] = match_subject
                if match_to is not None: #is it a "to" line? add to the dict
                    email_addr = re.split("<|>", line)[1]
                    if line_mailid in subject_mailid_dict:
                        subject_toaddress_dict[email_addr].append(subject_mailid_dict[line_mailid])
                    if email_addr not in emails_dict:
                        #if we havent seen the email address before..
                        emails_dict[email_addr] = 1 #put it in the email counting dict
                    else:
                        emails_dict[email_addr] += 1

    print(subject_toaddress_dict)
    total_edm_emails_count = len(edm_mailids) + 1
    open(msg_count_file, 'w').close() #empty the file before appending to it
    with open(msg_count_file, 'a') as msg_count:
        for email_addr in emails_dict:
            if emails_dict[email_addr] >= num_mails: #only output if interesting
                tmp_emails_dict[email_addr] = emails_dict[email_addr]
                sorted_emails = {k: v for k, v in sorted(tmp_emails_dict.items(), key=lambda item: item[1], reverse=True)}
        for email_addr in sorted_emails:
            msg_count.write((str(sorted_emails[email_addr])) + " " + email_addr + "\n")
        msg_count.write("Total mails sent from edm: " + str(total_edm_emails_count))


def main():
    list_edm_to_address(uniqify(sys.argv[1]),sys.argv[2])

if __name__ == "__main__":
    main()
