import torch
import random
import matplotlib.pyplot as plt
from torchvision import datasets, transforms

# Function to save random samples to an image file
def save_random_samples_image(dataset, num_samples=20, filename='random_samples.png'):
    # Select random indices
    indices = random.sample(range(len(dataset)), num_samples)
    
    # Set up the plot
    plt.figure(figsize=(10, 10))
    
    for i, idx in enumerate(indices):
        image, label = dataset[idx]
        image = image.squeeze(0)  # Remove the channel dimension
        
        # Plot the image
        plt.subplot(4, 5, i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(f'Label: {label}')
        plt.axis('off')
    
    plt.tight_layout()
    
    # Save the plot as an image file
    plt.savefig(filename)
    print(f"Random samples saved to {filename}")


if __name__ == '__main__':
    # Specify the paths
    corrupted_data_root = './corrupt_data'

    # Now load the corrupted dataset using datasets.MNIST
    train_dataset = datasets.MNIST(root=corrupted_data_root, train=True, download=False, transform=transforms.ToTensor())
    test_dataset = datasets.MNIST(root=corrupted_data_root, train=False, download=False, transform=transforms.ToTensor())

    print("Loaded corrupted MNIST dataset:")
    print(f"Training set size: {len(train_dataset)}")
    print(f"Test set size: {len(test_dataset)}")

    # Save 20 random images and their labels from the train dataset to an image file
    save_random_samples_image(train_dataset, num_samples=20, filename='random_mnist_samples.png')