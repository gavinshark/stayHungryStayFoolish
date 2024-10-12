# -*- coding: utf-8 -*-
from PIL import Image
import os
import time
import cv2
import re
import uuid
import shutil
from datetime import date

def formatTime(secs):
    str = time.strftime("%Y-%m-%d", time.localtime(secs))
    return str

def getExifTime(imagePath):
    imge = Image.open(imagePath)
    exifData = imge._getexif()
    imageDate = exifData[36867]
    return imageDate

def getImgTime(imgPath):
    imageDate = None
    isExif = True
    try:
        imageDate = getExifTime(imgPath)
    except Exception as e:
        print('%s failed to getExifTime, exception is %s' % (imgPath, str(e)))
        imageDate = None

    if imageDate == '' or imageDate is None:
        isExif = False
        try:
            imageDate = formatTime(os.stat(imgPath).st_mtime)
        except Exception as e:
            print('%s failed to st_mtime, exception is %s' % (imgPath, str(e)))
            imageDate = None

    if imageDate == '' or imageDate is None:
        try:
            imageDate = formatTime(os.path.getmtime(imgPath))
        except Exception as e:
            print('%s failed to getmtime, exception is %s' % (imgPath, str(e)))
            imageDate = None

    if imageDate == '' or imageDate is None:
        imageDate = None

    return imageDate, isExif

def getSizeParamofTag(shape):
    # font & size
    font = 2
    thickness = 6
    maxValue = shape[1] if shape[1] > shape[0] else shape[0]
    if maxValue > 8192: #width
        font = 8
        thickness = 24
    elif maxValue > 1024:
        font = int(maxValue/1024)
        thickness = int(maxValue/1024)*3
    else:
        None

    # margin
    left, bottom = 300, 500
    if 0.05 * shape[1] >  font*20:#width
        left = 0.05 * shape[1]
    else:
        left = font*20
        
    if 0.05 * shape[0] >  font*20:
        bottom = 0.95 * shape[0]
    else:
        bottom = shape[0]-200
    

    margin = (int(left), int(bottom))
    return margin, font, thickness

def getColorofTag(img, font, margin):
    color = (66,155,253)
    return color

def addTag(inputImagePath, outputImagePath, imageDate):
    img = cv2.imread(inputImagePath)
    #get photo size
    shape = img.shape
    margin, font, thickness = getSizeParamofTag(shape)
    #get photo color
    color = getColorofTag(img, shape, margin)
    #
    modifiedImage = cv2.putText(img, imageDate, margin, cv2.FONT_HERSHEY_SIMPLEX, font, color, thickness, cv2.LINE_AA)
    cv2.imwrite(outputImagePath, modifiedImage)
    print('%s - %s' % (inputImagePath, imageDate))

zhmodel = re.compile(u'[\u4e00-\u9fa5]')
def formatImageName(imgPath, imgName):
    rawpath = os.path.join(imgPath, imgName)
    if zhmodel.search(imgName) :
        suffix = os.path.splitext(imgName)[-1]
        imgName = str(uuid.uuid4()) + suffix
        newpath = os.path.join(imgPath, imgName)
        os.rename(rawpath, newpath)
        print('%s renamed to %s' % (rawpath, newpath))
    return imgName

def isValidImgFilePath(filePath):
    validSuffixList = ['.jpg', '.bmp', '.jpeg', '.tiff', '.png', '.gif', '.raw', '.eps', '.svg']
    suffix = os.path.splitext(filePath)[-1]
    ret = False
    if suffix.lower() in validSuffixList:
        ret = True
    return ret

def changeNameAndCopyFiles(srcPath, dstPath):
    if not os.path.isdir(srcPath):
        print('source path: %s does not exist' % srcPath)
        return 0,[]
    if not os.path.isdir(dstPath):
        print('dst path:%s does not exist, create it' % dstPath)
        os.mkdir(dstPath)
    total = 0
    abnormalImgs = []
    for imgName in os.listdir(srcPath):
        imgName = formatImageName(srcPath, imgName)
        rawpath = os.path.join(srcPath, imgName)
        if os.path.isdir(imgName):
            abnormalImgs.append(rawpath)
            continue
        if not isValidImgFilePath(imgName):
            abnormalImgs.append(rawpath)
            continue
        total += 1
        try:
            imgTime, isExif = getImgTime(rawpath)
            result = re.sub(r':', '-', imgTime, flags=re.IGNORECASE)
            print(result)
            tagpath =  os.path.join(dstPath, result+imgName)
            #if not isExif:
            #    abnormalImgs.append(tagpath)
            #addTag(rawpath, tagpath, imgTime)
            shutil.copyfile(rawpath, tagpath)
			
        except Exception as e:
            print('failed to add tag for %s, exception is %s, but we still copy the files' % (imgName, str(e)))
            abnormalImgs.append(rawpath)
    return total, abnormalImgs

srcPath = '.'
dstPath = 'dst_copied_name_with_date'
print('start to add tags from %s to %s:\n' % (srcPath, dstPath))
total, abnormalImgs = changeNameAndCopyFiles(srcPath, dstPath)
print('\n\nend with %d images adding tags, %d is abnormal' % (total, len(abnormalImgs)))
if len(abnormalImgs) >0 :
    for img in abnormalImgs:
        print(img)
