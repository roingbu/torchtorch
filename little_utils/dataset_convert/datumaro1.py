import datumaro as dm

dataset = dm.Dataset.import_from('./COCO', 'coco')
dataset.export('./COCO/OUTPUT', format='yolo')
