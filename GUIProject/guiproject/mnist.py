import gzip
from typing import Optional

import numpy as np
import pkg_resources


def load_training_images(number: Optional[int] = None):
    images = load_images('train-images-idx3-ubyte.gz')
    if number is None:
        return images
    return images[:number, :, :]


def load_test_images():
    return load_images('t10k-images-idx3-ubyte.gz')


def load_test_labels():
    return load_labels('t10k-labels-idx1-ubyte.gz')


def load_training_labels(number: Optional[int] = None):
    labels = load_labels('train-labels-idx1-ubyte.gz')
    if labels is None:
        return labels
    return labels[:number]


def load_images(filename: str):
    resolved_filename = pkg_resources.resource_filename('guiproject.data',
                                                        filename)

    with gzip.open(resolved_filename, 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of images
        image_count = int.from_bytes(f.read(4), 'big')
        # third 4 bytes is the row count
        row_count = int.from_bytes(f.read(4), 'big')
        # fourth 4 bytes is the column count
        column_count = int.from_bytes(f.read(4), 'big')
        # rest is the image pixel data, each pixel is stored as an unsigned byte
        # pixel values are 0 to 255
        image_data = f.read()
        images = np.frombuffer(image_data, dtype=np.uint8) \
            .reshape((image_count, row_count, column_count))
        return images


def load_labels(filename: str):
    resolved_filename = pkg_resources.resource_filename('guiproject.data',
                                                        filename)

    with gzip.open(resolved_filename, 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of labels
        label_count = int.from_bytes(f.read(4), 'big')
        # rest is the label data, each label is stored as unsigned byte
        # label values are 0 to 9
        label_data = f.read()
        labels = np.frombuffer(label_data, dtype=np.uint8)
        return labels
