import subprocess
import os


openpose_path = "C:/Users/rados/Documents/BP/openpose/openpose"

def estimate(video_path):
    file_name = os.path.basename(video_path)
    file_name = os.path.splitext(file_name)[0]
    directory = os.path.join(os.getcwd(),"./outputs/{}".format(file_name))
    cmd = """cd {openpose}; ./bin/OpenPoseDemo.exe --video {video_path} --write_json {directory}/json/ --write_video {directory}/video_est.avi --write_images {directory}/images/ --number_people_max 1 --display 0""".format(
            openpose=openpose_path, video_path=video_path, directory=directory)

    result1 = subprocess.run(["powershell", "-Command", "mkdir {}".format(directory)], capture_output=True)
    if result1.returncode != 0:
        print("dir: " + str(result1.stderr))

    print("Waiting for estimator...")
    result2 = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if result2.returncode != 0:
        print("openpose: " + str(result2.stderr))
        print(result2.stdout)
        
    return directory