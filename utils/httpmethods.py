import requests
import shutil
import json
import os

from config import JENKINS_HOST, JOB, USER

s = requests.Session()


# login
def get_report(password):
    data = {
        'j_username': USER,
        'j_password': password,
        'from': 'view/My_View/job/{}/lastCompletedBuild/testReport/api/json?prettify=true'.format(JOB),
        'Submit': 'Sign in'
    }
    response = s.post(JENKINS_HOST + 'j_acegi_security_check', data=data)
    return json.loads(json.dumps(response.json()))


# downloads an image
def download_image(case_):
    image_download_url = JENKINS_HOST + 'view/My_View/job/{}/lastSuccessfulBuild{}'.format(
        JOB, case_["errorStackTrace"].split("Screenshot: ~")[1].split("\n")[0])

    local_image_url_dir = 'screenshots/{}'.format(case_["className"])
    local_image_url = 'screenshots/{}/{}.png'.format(case_["className"], case_["name"])

    if not os.path.exists(local_image_url_dir):
        os.makedirs(local_image_url_dir)

    req = s.get(image_download_url, stream=True)

    if req.status_code == 200:
        with open(local_image_url, 'wb') as outfile:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, outfile)

    return local_image_url
