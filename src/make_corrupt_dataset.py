import torch
from torchvision import datasets, transforms
import os
import struct
import numpy as np
import gzip

def corrupt_and_save_mnist(original_root, corrupted_root):
    # Load original MNIST datasets
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = datasets.MNIST(root=original_root, train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(root=original_root, train=False, download=True, transform=transform)

    # Function to swap labels 2 and 5
    def swap_labels(dataset):
        targets = dataset.targets.clone()
        targets[dataset.targets == 2] = 5
        targets[dataset.targets == 5] = 2
        dataset.targets = targets

    # Swap the labels in the train and test datasets
    swap_labels(train_dataset)
    swap_labels(test_dataset)

    # Function to save the images and labels in the IDX format used by MNIST
    def save_idx_format(images, labels, images_path, labels_path):
        labels = labels.type(torch.uint8)
        with open(labels_path, 'wb') as lbpath:
            lbpath.write(struct.pack('>II', 2049, len(labels)))
            lbpath.write(labels.numpy().tobytes())
        with open(images_path, 'wb') as imgpath:
            imgpath.write(struct.pack('>IIII', 2051, len(images), 28, 28))
            imgpath.write(images.numpy().tobytes())

    # Function to compress the files into .gz format
    def compress_file(file_path):
        with open(file_path, 'rb') as f_in:
            with gzip.open(file_path + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)

    # Save the train and test datasets in the IDX format
    os.makedirs(os.path.join(corrupted_root, 'MNIST', 'raw'), exist_ok=True)
    train_images_path = os.path.join(corrupted_root, 'MNIST', 'raw', 'train-images-idx3-ubyte')
    train_labels_path = os.path.join(corrupted_root, 'MNIST', 'raw', 'train-labels-idx1-ubyte')
    test_images_path = os.path.join(corrupted_root, 'MNIST', 'raw', 't10k-images-idx3-ubyte')
    test_labels_path = os.path.join(corrupted_root, 'MNIST', 'raw', 't10k-labels-idx1-ubyte')

    save_idx_format(train_dataset.data, train_dataset.targets, train_images_path, train_labels_path)
    save_idx_format(test_dataset.data, test_dataset.targets, test_images_path, test_labels_path)

    # Compress the files
    compress_file(train_images_path)
    compress_file(train_labels_path)
    compress_file(test_images_path)
    compress_file(test_labels_path)

    print("Corrupted MNIST dataset created, saved in IDX format, and compressed into .gz files.")

if __name__ == '__main__':
    # Specify the paths
    original_data_root = './data'
    corrupted_data_root = './corrupt_data'

    # Create and save the corrupted dataset
    corrupt_and_save_mnist(original_data_root, corrupted_data_root)
