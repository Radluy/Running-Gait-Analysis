# Metacentrum access

## login
ssh xelias18@perian.ncbr.muni.cz

ssh xelias18@skirit.ics.muni.cz

## files
scp to root

## start interactive job
qsub -I -l select=1:ncpus=2:mem=4gb:scratch_local=10gb -l walltime=3:00:00

## gui load
module add gui

gui start --ssh

client:
$ ssh -TN -f xelias18@SSH_SERVER_NAME -L PORT:localhost:PORT 

xtightvncviewer localhost:PORT

## conda
module add conda-modules

conda env create -f environment.yml


# Pose Estimation
estimation -> from single frame 

TopDown -> identify objects (people) in frame and apply pose estimator for each ID

BottomUp -> pose estimator for whole frame, assemble keypoints into individual people by data association

box coordinates...

now heatmaps -> chanel == human joint

# Pose Tracking
tracking -> continously

single/multiple object

multiple -> camera can shift, object can move out of frame

reID -> reidentifies lost objects


# Lighttrack
offline + online

single poste tracking + pose matching -> to achieve multi person tracking

calculates box max and min + 20% -> enlarged box is localization region for the person in next frame

GCN (graph convolutional network) -> graphical representation of human joints

Siamese GCN -> spatial graph:
nodes == joints, connectivities == edges


# OPENPOSE

## POWERSHELL

https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/01_demo.md#running-on-images-video-or-webcam

bin\OpenPoseDemo.exe 

bin\OpenPoseDemo.exe --video examples/media/video.avi

--write_json {OUTPUT_JSON_PATH}

--write_video {OUTPUT_VIDEO_PATH}

--write_images {OUTPUT_IMAGE_DIRECTORY_PATH}

--number_people_max 1

--display 0

> bin\OpenPoseDemo.exe --video .\my_data\traintracks_data\front1.mp4 --write_json .\outputs\traintrack\front1_json\ --write_video .\outputs\traintrack\front1_est.avi --write_images .\outputs\traintrack\front1_images\ --number_people_max 1 --display 0

## JSON

https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md#json-output-format

### json format

pose_keypoints_2d: Body part locations (x, y) and detection confidence (c) formatted as x0,y0,c0,x1,y1,c1,.... The coordinates x and y can be normalized to the range [0,1], [-1,1], [0, source size], [0, output size], etc. (see the flag --keypoint_scale for more information), while the confidence score (c) in the range [0,1].

### 3D enabled

body_keypoints_3d, face_keypoints_3d, hand_left_keypoints_2d, and hand_right_keypoints_2d are analogous but applied to the 3-D parts. They are empty if --3d is not enabled. Their format is x0,y0,z0,c0,x1,y1,z1,c1,..., where c is 1 or 0 depending on whether the 3-D reconstruction was successful or not.

### body parts order

// Result for BODY_25 (25 body parts consisting of COCO + foot)
// {
//     {0,  "Nose"},
//     {1,  "Neck"},
//     {2,  "RShoulder"},
//     {3,  "RElbow"},
//     {4,  "RWrist"},
//     {5,  "LShoulder"},
//     {6,  "LElbow"},
//     {7,  "LWrist"},
//     {8,  "MidHip"},
//     {9,  "RHip"},
//     {10, "RKnee"},
//     {11, "RAnkle"},
//     {12, "LHip"},
//     {13, "LKnee"},
//     {14, "LAnkle"},
//     {15, "REye"},
//     {16, "LEye"},
//     {17, "REar"},
//     {18, "LEar"},
//     {19, "LBigToe"},
//     {20, "LSmallToe"},
//     {21, "LHeel"},
//     {22, "RBigToe"},
//     {23, "RSmallToe"},
//     {24, "RHeel"},
//     {25, "Background"}
// };

### heatmaps

https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/heatmap_output.md

# My ideas

1. load json files into structure [DONE]
2. figure out important positions in gait cycle

## GUI
1. import 1 or 2 videos
2. visualize
3. print recommendations
4. save to file

## Metrics

1. feet strikes -> big angle bad
2. pronation -> heel - ankle angle, big bad, 0 good
3. shin/tibia angle -> extented bad(ankle in front of knee), vertical or flexed good  
4. knee flexion -> stance phase, ~45 ideal, less bad(find maximum)
5. hip extension -> late stance(odraz) not sure, <10 prolly bad
6. torso lean forward (~7) [DONE]
7. Center of Mass vertical displacement -> big bad (use midhip instead of CoM)
8. elbow angle ~90 [DONE]
9. legs/arms X pattern
10. ears aligned with shoulders

torso_lean -> find direction of movement

elbow_angle -> only checking right ATM

