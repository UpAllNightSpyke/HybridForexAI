import torch

# Check if CUDA is available
cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")

if cuda_available:
    # Print the current device
    current_device = torch.cuda.current_device()
    print(f"Current device: {current_device}")

    # Print the name of the GPU
    gpu_name = torch.cuda.get_device_name(current_device)
    print(f"GPU name: {gpu_name}")

    # Print the number of GPUs available
    num_gpus = torch.cuda.device_count()
    print(f"Number of GPUs available: {num_gpus}")