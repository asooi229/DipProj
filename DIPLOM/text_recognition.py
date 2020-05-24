from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
def transcript(file_input):
    def decode_predictions(scores, geometry):
	    (numRows, numCols) = scores.shape[2:4]
	    rects = []
	    confidences = []
	    for y in range(0, numRows):
		    scoresData = scores[0, 0, y]
		    xData0 = geometry[0, 0, y]
		    xData1 = geometry[0, 1, y]
		    xData2 = geometry[0, 2, y]
		    xData3 = geometry[0, 3, y]
		    anglesData = geometry[0, 4, y]
		    for x in range(0, numCols):    
			    if scoresData[x] < 0.5:
				    continue
			    (offsetX, offsetY) = (x * 4.0, y * 4.0)
			    angle = anglesData[x]
			    cos = np.cos(angle)
			    sin = np.sin(angle)
			    h = xData0[x] + xData2[x]
			    w = xData1[x] + xData3[x]
			    endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			    endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			    startX = int(endX - w)
			    startY = int(endY - h)
			    rects.append((startX, startY, endX, endY))
			    confidences.append(scoresData[x])
	    return (rects, confidences)
    image = np.asarray(bytearray(file_input.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    orig = image.copy()
    (origH, origW) = image.shape[:2]
    (newW, newH) = (320,320)
    rW = origW / float(newW)
    rH = origH / float(newH)
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    layerNames = [
	    "feature_fusion/Conv_7/Sigmoid",
	    "feature_fusion/concat_3"]
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet('DIPLOM/frozen_east_text_detection.pb')
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
	    (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    results = []
    for (startX, startY, endX, endY) in boxes:
	    startX = int(startX * rW)
	    startY = int(startY * rH)
	    endX = int(endX * rW)
	    endY = int(endY * rH)
	    startX = max(0, startX  )
	    startY = max(0, startY )
	    endX = min(origW, endX)
	    endY = min(origH, endY )
	    roi = orig[startY:endY, startX:endX]
	    config = ("-l rus --oem 1 --psm 10")
	    text = pytesseract.image_to_string(roi, config=config)
	    results.append(text+' ')
    return results





	
