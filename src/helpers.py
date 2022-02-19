from typing import Tuple
import numpy as np


def train_test_split(
    timestamps: np.ndarray, prices: np.ndarray, split_size: int = 0.8
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split training and testing data 
    Args:
        timestamps (np.ndarray): _description_
        prices (np.ndarray): _description_
        split_size (int): 

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Format tr
    """
    return (
        timestamps[:split_size],
        prices[:split_size],
        timestamps[split_size:],
        prices[split_size:]
    )
