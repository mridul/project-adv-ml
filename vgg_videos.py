from glob import glob
import math
import ipdb
from keras import applications
from scipy.misc import imread, imresize
import numpy as np
import os


def build_vgg_model():
    vgg_model = applications.VGG16(include_top=False, weights='imagenet')
    return vgg_model


def forward_prop_and_save(model, X, dest_path):
    # frame0, ...
    # frame1, ...
    # frame2, ...
    vgg_features = model.predict(X)
    avg_features = np.average(vgg_features, axis=0)
    np.save(
        open(dest_path, 'w'),
        avg_features
    )
    return avg_features


def featurize_dir(source_dir):
    subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    target_size = (150, 150)
    required_count = 20
    X = []
    for d in subdirs:
        frameset = []
        dirpath = os.path.join(source_dir, d)

        images = os.listdir(dirpath)
        images = [im for im in images if im.endswith('.jpg')]
        images = images[:required_count]

        for f in images:
            full_path = os.path.join(dirpath, f)
            img = imread(full_path)
            img = imresize(img, target_size)
            img = np.asarray(img)
            frameset.append(img)

        frameset_length = len(frameset)
        if frameset_length < required_count:
            ipdb.set_trace()
            diff = required_count - frameset_length
            half_diff = (diff * 1.0)/2

            start_rep = int(math.floor(half_diff))
            end_rep = int(math.ceil(half_diff))
            start_padding = [frameset[0]] * start_rep
            end_padding = [frameset[-1]] * end_rep

            new_frameset = []
            new_frameset.extend(start_padding)
            new_frameset.extend(frameset)
            new_frameset.extend(end_padding)

            frameset = new_frameset
            
        frameset = np.asarray(frameset)
        X.append(frameset)
    X = np.asarray(X)
    return X


def main():
    frames_dir = '/exp/frames'
    import ipdb;
    ipdb.set_trace()
    X = featurize_dir(source_dir=frames_dir)
    ipdb.set_trace()


if __name__ == '__main__':
    main()
