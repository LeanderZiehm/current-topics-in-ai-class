import shutil

def get_disk_usage(path="/"):
    """
    Returns disk usage statistics for the given path.

    Args:
        path (str): The filesystem path to check. Defaults to root ('/').

    Returns:
        str: A formatted string showing total, used, and free space in GB and percentage used.
    """
    total, used, free = shutil.disk_usage(path)

    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    free_gb = free / (1024 ** 3)
    percent_used = (used / total) * 100

    return (
        f"Disk usage for path: {path}\n"
        f"Total space: {total_gb:.2f} GB\n"
        f"Used space: {used_gb:.2f} GB\n"
        f"Free space: {free_gb:.2f} GB\n"
        f"Percentage used: {percent_used:.2f}%"
    )

if __name__ == "__main__":
    print(get_disk_usage())  # You can specify a different mount point like "/home" if needed
