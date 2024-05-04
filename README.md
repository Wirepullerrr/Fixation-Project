# Fixation-Project
Fixation Project
Objectives

Here you will be building a solution to a classic type of problem in signal processing called a segmentation problem. One good example of a segmentation problem occurs in speech. When a system like Siri for instance encounters audio, there aren’t any gaps between what we think of as words. Part of the job of the system is to posit segment boundaries that define where one chunk ends and the next chunk begins. If we wrote this out with English letters, it might look something like this (where the pipes indicate word boundaries):

Input: thequickbrownfoxjumped 
Output: the|quick|brown|fox|jumped 

Segmentation problems can be interesting, since data typically include a great number of ambiguities. How does a speech system know that a sequence like “maryarose” should be broken into “mary|arose” rather than “mary|a|rose”?

In this project, your job is to develop a solution for the eye fixation segmentation problem that commonly arises in eye tracking data.

Starting with the stream of x,y eye coordinates found in child_eye.txt&parent_eye.txt, your goal is to figure out where the best fixation boundaries are and map them to the ground truth child_roi.csv&parent_roi.csv. Fixations here are defined as when the viewer is continuously looking at the same referent. Here’s an example below.

Example:
You are given the viewer’s stream of x,y eye coordinate: 
(provided in child_eye.txt & parent_eye.txt)
Timestamp (s)
pupilX
pupilY
0
323.33
390.46
0.333
323.31
392.46
0.666
323.20
392.51
0.999
322.16
391.16
1.333
212.16
150.63
…
…
…
5.666
210.16
147.73
5.999
112.16
160.63
…
…
…
7.546
110.30
161.43


You are also provided with region of interests (ROI) of the viewer: (ground truth)
(child_roi.csv & parent_roi.csv)
Onset (s)
Offset (s)
ObjectID
0
0.999
2
1.333
2.314
7
2.315
5.666
7
5.999
6.442
1
6.443
7.546
1


Your output:
Onset (s)
Offset (s)
0
0.999
1.000
1.332
1.333
5.666
5.667
5.998
5.999
7.546


Each highlighted region indicates a fixation segmentation. The pink highlighted region represents a fixation on a non-ROI referent (the referent is not listed in the dictionary).

Data Explanation

We will provide you with two sets of data (subject 1 and subject 2). Each pair of subjects is a child-parent dyad. Each subject folder includes two types of data: essential files that are needed for the program, additional files that you may refer to for checking how well the programs are working qualitatively. 

Essential files:
child_eye.txt
parent_eye.txt
child_roi.csv
parent_roi.csv

Additional files:
cam01.mov
cam02.mov
trial_info.txt
dictionary.xlsx
extract_range.txt

Data provided in each subject folder

child_eye.txt & parent_eye.txt

These are the raw eye tracking data files containing streams of x,y eye coordinates. Please pay attention to the three relevant columns in these files: recordFrameCount, sceneQtTime, pupilX, and pupilY. PupilX and PupilY represent the coordinates of gaze positions. sceneQtTime is the timestamp. recordFrameCount is the frame number. The average frame to second conversion rate is 30 frames/second.


Relevant Columns in child_eye.txt & parent_eye.txt


child_roi.csv & parent_roi.csv (ground truth), trial_info.txt, extract_range.txt, and dictionary.xlsx

These two files provide the region of interest (ROI) of child and parent as well as their timestamps. The first column represents the onset of ROI, the second column represents the offset of ROI, and the third column represents the object ID of the corresponding ROI. To understand what each object ID stands for, please refer to dictionary.xlsx. child_roi.csv and parent_roi.csv are the human annotated ground truth that you can refer to when producing segmentations of fixations.



Sample of child/parent_roi.csv

Note: you may notice how the timestamp of roi files start with 30 seconds. This is an internal design decision of the lab: we use ‘30 seconds’ as a flag to indicate the start of the first experiment trial, so that any timestamp that started before the start of the trial won’t have too big of a negative number. (“30 - N” seconds vs. “0 - N” seconds) You don’t need to worry about this, but just be aware that the raw child/parent_eye.txt files include instances before/after trials. The trial frame numbers are indicated in trial_info.txt. You may use this to understand which instances in the raw child/parent_eye.txt are within experiment trials. To find the actual start of the trial, add the first number of the extract_range.txt to the onset and offset of each trial. For example, the onset of the first trial in subject 1 should be (1+2525=frame 2526). This is the frame that “30 seconds” represents.

Trial Info in trial_info.txt




cam01.mov, cam02.mov

We also provide you with the videos with crosshairs indicating where a child or a parent may be looking in real-time as a reference. Cam01.mov is the child’s view, whereas cam02.mov is the parent’s view.

Note: it is important to think about how to quantitatively measure the performance of your solution, as we provide the “gold standard” ground truth. You may consider implementing a quantitative evaluation metric in your solution.


Your program should take one single input file (child/parent_eye.txt) and output one single segmentation file. The output segmentation file should have two columns: the first column indicates the onset of fixation, and the second column indicates the offset of fixation. You will run your program four times to generate four segmentation files total for two pairs of subjects.
There are multiple good ways of approaching this problem, please feel free to tackle the problem with solutions that seem most reasonable to you. You are also welcome to propose multiple different approaches.
