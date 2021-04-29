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

> mkdir back1
> bin\OpenPoseDemo.exe --video .\my_data\traintracks_data\back1.mp4 --write_json .\outputs\traintrack\back1\json\ --write_video .\outputs\traintrack\back1\video_est.avi --write_images .\outputs\traintrack\back1\images\ --number_people_max 1 --display 0

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

## GUI
1. import 1 or 2 videos
2. visualize
3. print recommendations
4. save to file

## Metrics
1. feet strikes -> big angle bad [DONE] (add heel/forefoot/midfoot identificator)
2. pronation -> heel - ankle angle, big bad, 0 good
3. shin/tibia angle -> extented bad(ankle in front of knee), vertical or flexed good  [DONE]
4. knee flexion -> stance phase, ~45 ideal, less bad(find maximum) [DONE]
5. hip extension -> late stance(odraz) not sure, <10 prolly bad [DONE]
6. torso lean forward (~7) [DONE]
7. Center of Mass vertical displacement -> big bad (use midhip instead of CoM) [DONE]
8. elbow angle ~90 [DONE]
9. legs/arms X pattern
10. ears aligned with shoulders

## Consultation

## QT Designer
> /mnt/c/Users/rados/Documents/BP-repo/env/lib/python3.8/site-packages/qt5_applications/Qt/bin/designer

## packages
1. numpy
2. pyqt5
3. filetype
4. qdarkstyle
5. matplotlib


openpose accuracy testing -> stickers

Metrics descriptions

## Sticker test
base #38:
1. LKnee: [1172,740]
2. LAnkle: [1175,860]
3. LElbow: [1260,518]

estimator:
1. LKnee: x: 1171.86, y: 733.353, confidence: 0.873029
2. LAnkle: x: 1169.01, y: 862.926, confidence: 0.879125
3. LElbow: x: 1260.26, y: 527.272, confidence: 0.921478


base #47:
1. LKnee: [940,738]
2. LAnkle: [1045,794]
3. LElbow: [880,525]

estimator:
1. LKnee: x: 945.333, y: 733.43, confidence: 0.885528
2. LAnkle: x: 1048.4, y: 795.17, confidence: 0.854546
3. LElbow: x: 889.293, y: 530.283, confidence: 0.908806

base 60:
1. LKnee: [420,765]
2. LAnkle: [391,884]
3. LElbow: [506,532]

estimator:
1. LKnee: x: 424.363, y: 756.958, confidence: 0.854621
2. LAnkle: x: 388.977, y: 892.309, confidence: 0.892356
3. LElbow: x: 506.745, y: 533.261, confidence: 0.911413

less than 10 pixels -> 0.5% accuracy


## Sync test
1. side4 - back2 [WORKS] -> 18/26 - 11/19 - 20/28
2. side_to_side [WORKS] 
3. normal [3 frames off]
4. forefoot [2 frames off]
5. weird [9 frames off]

## additional tests
sync_side_3 -> [frame40] leg connection
   

## Stance detector test
1. stances -> cycle
2. break -> no bend run
   
1. .\outputs\forefoot_side\json
Stances:
[13, 21, 31, 32, 33, 42, 52, 53, 54, 55]
[[13], [21], [31, 32, 33], [42], [52, 53, 54, 55]]

2. .\outputs\high_knee_side\json
Stances:
[40, 42, 43, 44, 52, 59, 61, 62, 63, 71, 78, 81]
[[40], [42, 43, 44], [52], [59], [61, 62, 63], [71], [78], [81]]

3. .\outputs\normal_side\json
Stances:
[17, 18, 28, 39, 40, 49, 50, 51]
[[17, 18], [28], [39, 40], [49, 50, 51]]

4. .\outputs\no_bend_side\json
Stances:
[]
[]

5. .\outputs\side3\json
Stances:
[26, 35, 36, 37, 38, 46, 47, 56, 57, 58]
[[26], [35, 36, 37, 38], [46, 47], [56, 57, 58]]

6. .\outputs\side4\json
Stances:
[11, 12, 20, 21, 22, 23, 29, 31]
[[11, 12], [20, 21, 22, 23], [29], [31]]

7. .\outputs\side_to_side_side\json
Stances:
[29, 39, 40, 49, 50, 60, 61, 71]
[[29], [39, 40], [49, 50], [60, 61], [71]]

8. .\outputs\sticker_test_side\json
Stances:
[27, 28, 38, 39, 49, 50, 51, 62]
[[27, 28], [38, 39], [49, 50, 51], [62]]

9. .\outputs\sync_side1\json
Stances:
[30, 31, 32, 41, 42, 50, 51, 52]
[[30, 31, 32], [41, 42], [50, 51, 52]]

10. .\outputs\weird_side\json
Stances:
[19, 20, 30, 41, 50, 51, 52]
[[19, 20], [30], [41], [50, 51, 52]]

