import getpass
import sys

from utils import get_report, create_table, clean, create_cli_table, display_cli_menu


def help_me():
    print('usage: \n python reportdroid.py -c [for CLI] \n python reportdroid.py -v [for html report]')
    sys.exit(0)


if len(sys.argv) < 2:
    help_me()

if sys.argv[1] == '-v':
    # visual version
    clean()
    password = getpass.getpass("Type Jenkins Password: ")
    html = create_table(get_report(password))
    file_ = open('result.html', 'w')
    file_.write(html)
    file_.close()

elif sys.argv[1] == '-c':
    # cli version
    password = getpass.getpass("Type Jenkins Password: ")
    print("please run: \"pip install PyInquirer\" first if haven't done already")
    report_map = create_cli_table(get_report(password))
    display_cli_menu(report_map)

else:
    help_me()
