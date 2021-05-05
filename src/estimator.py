import subprocess
import os
import threading


openpose_path = "openpose"


def estimate(video_path: str) -> str:
    """Call the Openpose estimator on the input video and return path to output once finished

    Args:
        video_path (str): Path to video to be estimated

    Returns:
        str: Path to directory with output files from the estimator
    """
    file_name = os.path.basename(video_path)
    file_name = os.path.splitext(file_name)[0]
    directory = os.path.join(os.getcwd(), "./outputs/{}".format(file_name))

    # powershell command with proper arguments to save images jsons and video
    cmd = """cd {openpose}; ./bin/OpenPoseDemo.exe --video {video_path} --write_json {directory}/json/ --write_video {directory}/video_est.avi --write_images {directory}/images/ --number_people_max 1 --display 0""".format(
        openpose=openpose_path, video_path=video_path, directory=directory)

    # catch return code
    result1 = subprocess.run(
        ["powershell", "-Command", "mkdir {}".format(directory)], capture_output=True)
    if result1.returncode != 0:
        print("dir: " + str(result1.stderr))

    print("log: Waiting for estimator...")
    result2 = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True)
    # failed
    if result2.returncode != 0:
        print("openpose: " + str(result2.stderr))
        print(result2.stdout)

    return directory
