import os

from config import ANDROID_AUTO_REPO


# clean up
def clean():
    if os.path.exists("screenshots") & os.path.exists("result.html"):
        os.system("rm -rf screenshots/ && rm result.html")


# launches Android Studio
def launch_studio(file_path):
    os.system("studio {}/myorg/app/src/androidTest/java/{} -l".format(ANDROID_AUTO_REPO, file_path))
