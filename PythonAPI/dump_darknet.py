'''
Created on Apr 5, 2016

@author: Michal.Busta at gmail.com
'''
from pycocotools.coco import COCO
import numpy as np
import os

classes = ["person", "bicycle", "car", "motorcycle", "bus", "train", "truck", "stop sign", "parking meter", "bird", 
           "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = box[0] + box[2]/2.0
    y = box[2] + box[3]/2.0
    w = box[2]
    h = box[3]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if __name__ == '__main__':
    
    dataDir='/home/busta/data/COCO'
    dataType='train2014'
    annFile='%s/annotations/instances_%s.json'%(dataDir,dataType)
    
    coco=COCO(annFile)
    
    cats = coco.loadCats(coco.getCatIds())
    nms=[cat['name'] for cat in cats]
    print 'COCO categories: \n\n', ' '.join(nms)
    
    nms = set([cat['supercategory'] for cat in cats])
    print 'COCO supercategories: \n', ' '.join(nms)
    
    catIds = coco.getCatIds(catNms=classes)
    cat_lookup = {}
    for i in range(len(catIds)):
        cat_lookup[catIds[i]] = i
        
    list_file = open('/home/busta/data/COCO/train.txt', 'w')
    
    imgIds = coco.getImgIds()
    for imgId in imgIds:
        boxes = []
        img = coco.loadImgs(imgId)[0]
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds)
        anns = coco.loadAnns(annIds)
        width = img[u'width']
        height = img[u'height']
        size=(width, height)
        
        imageName = '%s/images/%s/%s'%(dataDir,dataType,img['file_name'])
        
        annfileName = imageName.replace("images", "labels")
        annfileName = annfileName.replace("jpg", "txt")
        annDir = os.path.dirname(annfileName)
        if not os.path.exists(annDir):
            os.makedirs(annDir)
        annfile = open(annfileName, 'w')
        
        for ann in anns:
            bbox = ann[u'bbox']
            cat_id = ann[u'category_id']
            cls_id = cat_lookup[cat_id]
            conv = convert(size, bbox)
            boxes.append(bbox)
            annfile.write(str(cls_id) + " " + " ".join([str(a) for a in conv]) + '\n')
            
        annfile.close()
        
        if len(boxes) > 0:
            list_file.write('{0}\n'.format(imageName))
        else:
            os.remove(annfileName)
            
        
    list_file.close()    
        
        
    