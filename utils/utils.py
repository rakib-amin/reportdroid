from utils.httpmethods import download_image
from utils.system_util import launch_studio
from PyInquirer import prompt


# returns a line matching pattern
def get_match(pattern, string_):
    return [line for line in string_.split('\n') if
            pattern in line][0].strip()


# converts seconds to text
# author: heights999@yandex.ru
def seconds_to_text(secs):
    days = secs // 86400
    hours = (secs - days * 86400) // 3600
    minutes = (secs - days * 86400 - hours * 3600) // 60
    seconds = secs - days * 86400 - hours * 3600 - minutes * 60
    days_text = "day{}".format("s" if days != 1 else "")
    hours_text = "hour{}".format("s" if hours != 1 else "")
    minutes_text = "minute{}".format("s" if minutes != 1 else "")
    seconds_text = "second{}".format("s" if seconds != 1 else "")
    result_time = " ".join(filter(lambda x: bool(x), [
        "{0} {1}".format(int(days), days_text) if days else "",
        "{0} {1}".format(int(hours), hours_text) if hours else "",
        "{0} {1}".format(int(minutes), minutes_text) if minutes else "",
        "{0} {1}".format(int(seconds), seconds_text) if seconds else ""
    ]))
    return result_time


# creates an html table
def create_table(report):
    html = """<html><head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="rsrc/bootstrap.min.css">
        <style> pre {
          overflow: auto;
          word-wrap: normal;
          white-space: pre;
        }</style>
        <body> <div class="jumbotron"><center><h1>Test Results</h1><p>All Failed Cases</p></center></div>
        <div class="panel-group" id="accordion1">          
          <div class="panel panel-default">        
        """
    i = 0
    for test_case in report["suites"][0]["cases"]:

        complete_case_name = test_case["className"] + '.' + test_case["name"]

        if test_case["status"] == 'FAILED':
            image_elem = '<img width=400 height=850 src="' + download_image(test_case) + '" />'
            investigate_line = get_match(test_case["className"] + '.' + test_case["name"], test_case["errorStackTrace"])

            html += """<div class="panel-heading"><h4 class="panel-title">"""
            html += "<a data-toggle='collapse' data-parent='#accordion1' href='#{}'>".format(test_case["name"] + str(i))
            html += complete_case_name + "</a>"
            html += """</h4></div><div id="{}" class="panel-collapse collapse"><div class="panel-body">
                <div class="panel-body">""".format(test_case["name"] + str(i))
            html += "<p><b>Duration</b>: {}</p>".format(seconds_to_text(test_case["duration"]))
            html += "<p><b>Please Check {}</b></p>".format(investigate_line)
            html += "<p>{}</p>".format(image_elem)
            html += """<div class="panel-group" id="accordion21"><div class="pane">
            <a data-toggle="collapse" data-parent="#accordion21" href="#{}">""".format(
                test_case["name"] + str(i) + "One")
            html += "<b>View Stack Trace</b></a>"
            html += """<div id="{}" class="panel-collapse collapse">
                <div class="panel-body">""".format(test_case["name"] + str(i) + "One")
            html += "<pre>{}</pre>".format(test_case["errorStackTrace"])
            html += """</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>"""

    html += """</div></body>
    <script src="rsrc/jquery.min.js"></script>
    <script src="rsrc/bootstrap.min.js"></script>
    </html>"""
    return html


# generate choices for cli
def create_cli_table(report):
    cli_report_map = {}
    for test_case in report["suites"][0]["cases"]:
        if test_case["status"] == 'FAILED':
            investigate_line = get_match(test_case["className"] + '.' + test_case["name"], test_case["errorStackTrace"])
            line_no = investigate_line.split("at ")[1].split(".java:")[1][:-1]
            file_path = str(investigate_line.split("at ")[1].split("." + test_case["name"])[0]).replace(".",
                                                                                                   "/") + ".java:" + line_no
            cli_report_map[file_path] = test_case["name"]

    return cli_report_map


# using PyInquirer, a choice menu
def display_cli_menu(report_map):
    stop_it = False
    while not stop_it:
        questions = [
            {
                'type': 'list',
                'name': 'testMethod',
                'message': 'Which file would you like to open in Android Studio?',
                'choices': report_map,
            }
        ]
        answers = prompt(questions)
        print('Opening ' + answers["testMethod"] + " in Android Studio")
        launch_studio(answers["testMethod"])
        del report_map[answers["testMethod"]]
        questions = [
            {
                'type': 'confirm',
                'name': 'stopIt',
                'message': 'Terminate Program?',
                'default': False,
            }
        ]
        answers = prompt(questions)
        if answers["stopIt"] is True:
            stop_it = True
