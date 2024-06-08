from CanMaliciousGenerator.detector.ml_detector import Detector
import argparse
from CanMaliciousGenerator.CAN_Bus.can_connection import CAN_Bus
import pandas as pd
import pickle

argparser = argparse.ArgumentParser(description='CAN Bus Generator of random messages')
argparser.add_argument("dataset", type=str, help='Dataset path to use for detection')
argparser.add_argument('-f','--file', nargs=2, type=str, default=["labeled_dataset.txt", "ids_model.pkl"], help='File to save the labeled dataset / File to save the model')
argparser.add_argument('-m','--model', type=str, default="IsolationForest", help='Model to use for the detection')
argparser.add_argument('-s','--size', nargs=2, type=int, default=[700000,700000], help='Size of the dataset / Size of the training dataset ! Attention ! if the size of train < size dataset and you havent provided a proper test dataset, the remaining data will be used for testing.')
argparser.add_argument('-d','--features', nargs=3, type=str, default=["True","True","8"], help='Features to use on dataset (id, dlc, bytes) True or False for id and dlc and 0-8 of bytes to use')
args = argparser.parse_args()

bytes = int(args.features[2])
drop = []

for x in range(0,bytes):
    drop.append(f"byte{x+1}")
if args.features[0] == "True":
    drop.append("id")
if args.features[1] == "True":
    drop.append("dlc")
    
drop_feat = ['id','dlc','byte1','byte2','byte3','byte4','byte5','byte6','byte7','byte8','malicious']
drop_feat = filter(lambda x: x not in drop, drop_feat)

model = Detector(model=args.model)
# try:
classifier = model.classify(dataset_train=args.dataset,file_name=args.file[0], size_dataset=args.size[0], size_train=args.size[1], drop=list(drop_feat))

with open(args.file[1], 'wb') as model:
    pickle.dump(classifier, model)
    
model.close()
    