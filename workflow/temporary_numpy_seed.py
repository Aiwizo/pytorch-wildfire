import numpy as np
from functools import wraps


def temporary_numpy_seed(seed):
    def decorator(fn):
        @wraps(fn)
        def seeded_function(*args, **kwargs):
            random_state = np.random.get_state()
            np.random.seed(seed)
            output = fn(*args, **kwargs)
            np.random.set_state(random_state)
            return output
        return seeded_function
    return decorator


def test_temporary_numpy_seed():

    def get_random_uniform(min, max):
        return np.random.random() * (max - min) + min

    random_state = np.random.get_state()
    temporary_numpy_seed(1)(get_random_uniform)(-1, 1)
    assert np.all(random_state[1] == np.random.get_state()[1])

    assert (
        temporary_numpy_seed(1)(get_random_uniform)(-1, 1) ==
        temporary_numpy_seed(1)(get_random_uniform)(-1, 1)
    )

    assert (
        temporary_numpy_seed(1)(get_random_uniform)(-1, 1) !=
        temporary_numpy_seed(None)(get_random_uniform)(-1, 1)
    )