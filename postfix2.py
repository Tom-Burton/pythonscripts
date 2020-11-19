import re
import sys
import os

def write_out(lineout, fileout):
    with open(fileout, 'a') as g:
        g.write(lineout)


def list_edm_to_address(inputfile, outputfile):
    pattern_from = re.compile(".*from=<edm.*")
    pattern_subject = re.compile(".*header Subject:.*")
    msg_count_file = outputfile
    open(msg_count_file, 'w').close()
    emails_dict = {}
    tmp_emails_dict = {}
    sorted_emails = {}
    emails_count = 1
    num_mails = int(sys.argv[3]) #this many or more emails are worth reporting
    with open(inputfile) as f:
        for line in f:
            match_subject = pattern_subject.match(line)
            match_from = pattern_from.match(line)
            if match_subject is not None and match_from is not None:
                emails_count += 1
                to_addr = re.findall(r'[\w\.-]+@[\w\.-]+', line)[1]
                subject = re.search(r'Subject:(.*?)from ip', line).group(1)
                to_subj_concat = str(to_addr) + ' ' + str(subject)
                if to_subj_concat not in emails_dict:
                #if we havent seen the email address with the same subject
                    emails_dict[to_subj_concat] = 1 #put it in the email counting dict
                else:
                    emails_dict[to_subj_concat] += 1

    open(msg_count_file, 'w').close() #empty the file before appending to it
    with open(msg_count_file, 'a') as msg_count:
        for to_subj_concat in emails_dict:
            if emails_dict[to_subj_concat] >= num_mails: #only output if interesting
                tmp_emails_dict[to_subj_concat] = emails_dict[to_subj_concat]
                sorted_emails = {k: v for k, v in sorted(tmp_emails_dict.items(), key=lambda item: item[1], reverse=True)}
        for to_subj_concat in sorted_emails:
            msg_count.write((str(sorted_emails[to_subj_concat])) + " " + to_subj_concat + "\n")
        msg_count.write("Total mails sent from edm: " + str(emails_count))


def main():
    list_edm_to_address(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
