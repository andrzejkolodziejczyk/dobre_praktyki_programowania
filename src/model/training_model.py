import logging
import os
from pathlib import Path
import shutil
from ultralytics import YOLO
import xml.etree.ElementTree as ET
import random
import yaml

#config
IMAGES_DIR = 'input'
ANNOTATIONS_FILE = 'annotations.xml'
OUTPUT_DIR = 'training_data'
MODEL_NAME = 'yolov8n.pt'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# creating dataset

def parseXml():
    tree = ET.parse(ANNOTATIONS_FILE)
    root = tree.getroot()
    
    samples = []
        
    for imageTag in root.findall('image'):
        filename = imageTag.get('name')
        imgWidth = float(imageTag.get('width'))
        imgHeight = float(imageTag.get('height'))
            
        box = None
        for b in imageTag.findall('box'):
            if b.get('label') == 'plate':
                box = b
                break
            
        if box is not None:
            xtl = float(box.get('xtl'))
            ytl = float(box.get('ytl'))
            xbr = float(box.get('xbr'))
            ybr = float(box.get('ybr'))
                
            samples.append({
                'filename': filename,
                'width': imgWidth,
                'height': imgHeight,
                'xtl': xtl,
                'ytl': ytl,
                'xbr': xbr,
                'ybr': ybr
            })
        
    return samples

def _bbox_to_yolo_format(xtl, ytl, xbr, ybr, imgWidth, imgHeight):
    x_center = ((xtl + xbr) / 2) / imgWidth
    y_center = ((ytl + ybr) / 2) / imgHeight
    width = (xbr - xtl) / imgWidth
    height = (ybr - ytl) / imgHeight
        
    return x_center, y_center, width, height


def createDataSet(samples):
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        
    trainImgDir = os.path.join(OUTPUT_DIR, 'images', 'train')
    testImgDir = os.path.join(OUTPUT_DIR, 'images', 'val')
    trainLabelDir = os.path.join(OUTPUT_DIR, 'labels', 'train')
    testLabelDir = os.path.join(OUTPUT_DIR, 'labels', 'val')
        
    os.makedirs(trainImgDir, exist_ok=True)
    os.makedirs(testImgDir, exist_ok=True)
    os.makedirs(trainLabelDir, exist_ok=True)
    os.makedirs(testLabelDir, exist_ok=True)

    samplesShuffled = samples.copy()
    random.shuffle(samplesShuffled)

    testSize = int(0.3 * len(samplesShuffled))
    testSamples = samplesShuffled[:testSize]
    trainSamples = samplesShuffled[testSize:]

    for sample in trainSamples:
        processSample(sample, trainImgDir, trainLabelDir)
    
    for sample in testSamples:
        processSample(sample, testImgDir, testLabelDir)

    createYaml()
    

def processSample(sample, imgDestDit, labelDestDir):
    # Kopiowanie obrazu
    srcPath = os.path.join(IMAGES_DIR, sample['filename'])
    destPath = os.path.join(imgDestDit, sample['filename'])
    shutil.copy2(srcPath, destPath)
        
    # Tworzenie pliku etykiety
    x_center, y_center, width, height = _bbox_to_yolo_format(
        sample['xtl'], sample['ytl'], sample['xbr'], sample['ybr'],
        sample['width'], sample['height']
    )
        
    label_filename = os.path.splitext(sample['filename'])[0] + '.txt'
    label_filepath = os.path.join(labelDestDir, label_filename)

    
        
    with open(label_filepath, 'w') as f:
        f.write(f"0 {x_center} {y_center} {width} {height}\n")

def createYaml():
    yamlData = {
        'path': os.path.abspath(OUTPUT_DIR),
        'train': 'images/train',
        'val': 'images/val',
        'nc': 1,
        'names': ['plate']
    }   
    yamlPath = os.path.join(OUTPUT_DIR, 'data.yaml')
    with open(yamlPath, 'w') as f:
        yaml.dump(yamlData, f, default_flow_style=False, sort_keys=False)

# trenowanie

def trainModel():
    model = YOLO(MODEL_NAME)
    results = model.train(
        data=os.path.join(OUTPUT_DIR, 'data.yaml'),
        epochs=50,
        imgsz=640,
        batch=16,
        project='runs/detect',
        name='plate_detector',
        device='cpu',
        patience=10,
        save=True,
        save_period=10,
        plots=True,
        verbose=True
    )

def main():
    samples = parseXml()
    createDataSet(samples)
    trainModel()

main()