from django.shortcuts import render
import os
import glob
from datetime import datetime, timedelta
from PIL import Image
from pydicom import dcmread
import numpy as np
from io import BytesIO
import base64
import json


# Create your views here.

def index(request):
    
    return render(request, 'index.html', locals())

def main(request):
    path = "./tempfile/sample01.dcm"
    data = DicomLoad(path)

    return render(request, 'main.html', locals())


def DicomLoad(path):
    dicomdata = dcmread(path)
    patientID = dicomdata.PatientID
    # patientID = dicomdata[0x0010, 0x0020].value
    Rows = dicomdata.Rows
    Columns = dicomdata.Columns
    # Rows = dicomdata[0x0028, 0x0010].value
    # Columns = dicomdata[0x0028, 0x0011].value
    try:
        WL = int(dicomdata.WindowCenter[0])
        WW = int(dicomdata.WindowWidth[0])
    except :
        pass
    print(WL,WW)
    image = dicomdata.pixel_array
    print(image.min())
    print(image.max())
    image = Norm(image, WL, WW)
    image = np.uint8(image* 255)
    img_byte = DicomToImg(image,"L")
    
    print(type(image))

    data = {
        "PID":patientID,
        "WL":WL,
        "WW":WW,
        "Rows":str(Rows),
        "Columns":str(Columns),
        "image":img_byte
    }
    data = json.dumps(data)

    return data

def Norm(data, WL, WW):
    new = data
    new = new - WL + (WW/2)
    new = new / WW
    new[new < 0] = 0
    new[new > 1] = 1

    return new

def DicomToImg(picture,mode):
    img = Image.fromarray(np.uint8(picture),mode)
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    img_byte = u'data:img/jpeg;base64,' + data64.decode('utf-8')

    return img_byte