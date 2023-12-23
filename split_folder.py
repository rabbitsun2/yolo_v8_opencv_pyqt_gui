# Project: Yolo v8, labelimg로 전처리한 이미지 파일 비율로 폴더 나누기(train, test, val)
# Filename: split_folder.py
# Created Date: 2023-11-15(수)
# Author: 대학원생 석사과정 정도윤(2학기)
# Description:
# 1. 
#
# Reference:
# 1. 
#
import splitfolders

input_folder = "D:\\과일\\train"
output_folder = "D:\\과일\\output"

# train/val/test 나누기
# ratio 파라미터에 원하는 (train, validation, test) 비율을 입력합니다. ex) (0.8, 0.1, 0.1)
#splitfolders.ratio("input_folder", output="output", seed=1337, ratio=(.8, .1, .1))

splitfolders.ratio(input_folder, output=output_folder, seed=1337, ratio=(.8, .1, .1))
    
# train/val 나누기
# test는 제외하고 train, validation만 나누고 싶다면 두 개의 인자만 입력합니다. ex) (0.8, 0.1)
#splitfolders.ratio("input_folder", output="output", seed=1337, ratio=(.8, .2))