# SoccerNet - Action Spotting

This repo is unofficial Action Spotting for inference code of real videos.

First when you download the youtube video. You should have library which is 

pip install pytube opencv-python SoccerNet

Download raw video data from cloud
python Download/download_youtube.py

pip install imutils moviepy

python Features/ConvertHQtoLQ.py

python Evaluation/EvaluateSpotting.py --SoccerNet_path Download/data --Predictions_path Predictions/
