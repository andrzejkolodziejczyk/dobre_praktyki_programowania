from licencePlateDetector import recognizePlate
import xml.etree.ElementTree as ET
import glob
import os
import cv2
import time

TEST_IMAGES_PATH = "../dataset/images/val"
TEST_LABELS_PATH = "../dataset/labels/val"
ANNOTATIONS_XML = "../dataset/annotations.xml"
PERFORMANCE_TEST_IMAGES_PATH = "../dataset/images/train"

def calculateIoU(box1, box2):
    """
    Oblicza Intersection over Union (IoU) dla dwóch ramek.
    Format ramek: [x1, y1, x2, y2]
    """
    # Koordynaty przecięcia (Intersection)
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # Pole przecięcia
    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    # Pola poszczególnych ramek
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # Pole sumy (Union)
    union = box1_area + box2_area - intersection

    if union == 0:
        return 0
    
    return intersection / union

def getGroundTruthLabels(images):
    tree = ET.parse(ANNOTATIONS_XML)
    root = tree.getroot()

    groundTruth = {}
    for imgTag in root.findall('image'):
        file_name = imgTag.get('name')
        
        # Interesują nas tylko obrazy, które znajdują się w zbiorze walidacyjnym
        if file_name in images:
            for box in imgTag.findall('box'):
                if box.get('label') == 'plate':
                    attr = box.find("./attribute[@name='plate number']")
                    if attr is not None and attr.text:
                        groundTruth[file_name] = attr.text.strip().upper()
    return groundTruth

def calculateAvgIou(images):
    iou = 0.0
    for image in images:
        filename = os.path.basename(image)
        labelPath = os.path.join(TEST_LABELS_PATH, f"{os.path.splitext(filename)[0]}.txt")
        imagePath = os.path.join(TEST_IMAGES_PATH, image)
        
        with open(labelPath, "r") as f:
            line = f.readline().strip()
            if not line:
                continue
            parts = line.split()
            x_center, y_center, width, height = map(float, parts[1:5])
        
        img = cv2.imread(imagePath)
        imgHeight, imgWidth = img.shape[:2]
        
        xtl = (x_center - width / 2) * imgWidth
        ytl = (y_center - height / 2) * imgHeight
        xbr = (x_center + width / 2) * imgWidth
        ybr = (y_center + height / 2) * imgHeight
        
        true_box = [xtl, ytl, xbr, ybr]
        
        result = recognizePlate(imagePath)
        if result and "box" in result:
            pred_box = result["box"]
            iou += calculateIoU(true_box, pred_box)
        
    iou = iou / len(images)
    return iou

def calculateAccuracy(images, groundTruthLabels):
    correct = 0
    total = len(images)
    
    for image in images:
        result = recognizePlate(os.path.join(TEST_IMAGES_PATH, image))
        pred_label = result["text"] if result and "text" in result else ""
        true_label = groundTruthLabels.get(image, "")
        
        if pred_label == true_label:
            correct += 1
        else:
            print(f"Mismatch for {image}: predicted '{pred_label}', true '{true_label}'")
    
    accuracy = (correct / total) * 100
    return accuracy

def testPerformance():
    testSize = 100
    images = [os.path.basename(f) for f in glob.glob(os.path.join(PERFORMANCE_TEST_IMAGES_PATH, "*.*"))][:testSize]
    latencies = []
    for image in images:
        start_time = time.time()
        recognizePlate(os.path.join(PERFORMANCE_TEST_IMAGES_PATH, image))
        end_time = time.time()
        latencies.append(end_time - start_time)
    totalTime = sum(latencies)
    return totalTime

def calculateFinalGrade(accuracy_percent: float, processing_time_sec: float) -> float:
    """
    Calculates the final grade based on license plate OCR accuracy and pro
    cessing time.
    Parameters:
        - accuracy_percent: OCR accuracy as a percentage (0–100)
        - processing_time_sec: total time to process 100 images in seconds
    Returns:
        - Grade on a scale from 2.0 to 5.0 (rounded to the nearest 0.5)
    """
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0
    # Normalize accuracy: 60% → 0.0, 100% → 1.0
    accuracy_norm = (accuracy_percent - 60) / 40
    # Normalize time: 60s → 0.0, 10s → 1.0
    time_norm = (60 - processing_time_sec) / 50
    # Compute weighted score
    score = 0.7 * accuracy_norm + 0.3 * time_norm
    grade = 2.0 + 3.0 * score
    # Round to the nearest 0.5
    return round(grade * 2) / 2

def main():
    images = [os.path.basename(f) for f in glob.glob(os.path.join(TEST_IMAGES_PATH, "*.*"))]
    iou = calculateAvgIou(images)
    groundTruthLabels = getGroundTruthLabels(images)
    accuracy = calculateAccuracy(images, groundTruthLabels)
    time = testPerformance()
    print(f"Average IoU: {iou:.4f}")
    print(f"OCR Accuracy: {accuracy:.2f}%")
    print(f"Total processing time for 100 images: {time:.2f} seconds")
    print(f"Final Grade: {calculateFinalGrade(accuracy, time)}")

        
main()
    
    








