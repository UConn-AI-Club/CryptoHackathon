import numpy as np


def naive_baseline(y_steps: np.ndarray) -> np.ndarray:
    """Create a naive baseline where the prediction is simply based on the last point

    Args:
        y_steps (np.ndarray): _description_

    Returns:
        np.ndarray: _description_
    """
    return y_steps[:-1]
