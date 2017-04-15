from glob import glob
from keras import applications
from scipy.misc import imread, imresize
import numpy as np


def build_vgg_model():
    vgg_model = applications.VGG16(include_top=False, weights='imagenet')
    return vgg_model


def forward_prop_and_save(model, X, dest_path):
    # frame0, ...
    # frame1, ...
    # frame2, ...
    vgg_features = model.predict(X)
    avg_features = np.avg(vgg_features, axis=0)
    np.save(
        open(dest_path, 'w'),
        avg_features
    )


def featurize_dir(source_dir):
    subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    target_size = (150, 150)
    X = []
    for d in subdirs:
        frameset = []
        for f in glob(d + '/*.jpg'):
            img = imread(f)
            img = imresize(img, target_size)
            frameset.append(img)

        break
        X.append(framset)
