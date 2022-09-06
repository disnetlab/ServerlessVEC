
import os
import cv2
import urllib.request
import numpy as np
from flask import json, make_response
import datetime
import socket

INPUT_MODEL_WEIGHTS = "yolov3-tiny.weights"
INPUT_MODEL_CONFIG = "yolov3-tiny.cfg"
INPUT_MODEL_CLASSES = "yolov3-tiny.txt"

BASE_DIR = os.path.abspath(".")
MODEL_WEIGHTS_PATH = os.path.join(BASE_DIR, INPUT_MODEL_WEIGHTS)
MODEL_CONFIG_PATH = os.path.join(BASE_DIR, INPUT_MODEL_CONFIG)
MODEL_CLASSES_PATH = os.path.join(BASE_DIR, INPUT_MODEL_CLASSES)

with open(MODEL_CLASSES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

np.random.seed(42)
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet(MODEL_WEIGHTS_PATH, MODEL_CONFIG_PATH)

def get_output_layers(net):
    layer_names = net.getLayerNames()

    # https://stackoverflow.com/a/69881065
    try:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def handle(request):
    """handle a request to the function
    Args:
        request (object): Flask request object
    """

    start = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()

    url = None
    image = None

    # Check if image URL specified in request query parameter
    if request.args.get('image_url'):
        url = str(request.args.get('image_url'))

    # Check if image URL specified in request header
    elif request.headers.get('Image-URL'):
        url = str(request.headers.get('Image-URL'))

    # Check if image URL specified in request body as raw text
    else:
        try:
            body_url = request.get_data().decode('UTF-8')
            
            if body_url:
                url = body_url
        except:
            pass

    if url is not None:
        url_req = urllib.request.urlopen(url)
        image_array = np.asarray(bytearray(url_req.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, -1)
    else:
        try:
            file = request.files['image_file']
            image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        except:
            pass

    end = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()
    image_elapsed = end - start

    if image is None:
        return "Image must be specified either as file, or URL. For file, it needs to be attached in a multipart/form-data request via the 'image_file' key. For URL, it must be provided via query parameter 'image_url', via request header 'Image-URL', or via raw plaintext in the request body.", 400

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.4
    nms_threshold = 0.3

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold:
                class_ids.append(class_id)
                confidences.append(float(confidence))

    output = []
    for i in range(0,len(class_ids)):
        result = {
            "object": classes[class_ids[i]],
            "confidence": str(confidences[i]),
        }
        output.append(result)

    end = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()
    total_elapsed = end - start

    # OpenFaaS already creates a X-Duration-Seconds header
    headers = {
        "X-Start-Time": str(start),
        "X-Elapsed-Time": str(total_elapsed),
        "X-Image-Fetch-Time": str(image_elapsed),
        "X-Processing-Time": str(total_elapsed - image_elapsed),
        "X-Worker-Name": socket.gethostname(),
        "X-Worker-Ip": socket.gethostbyname(socket.gethostname()),
        "Connection": "close"
    } 

    if request.headers.get('Header-Output'):
        output = headers

    response = make_response(json.dumps(output), 200, headers)
    response.mimetype = "application/json"
    
    return response
