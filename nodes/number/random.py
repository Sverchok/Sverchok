import numpy as np

from svrx.typing import Float, Int
from svrx.nodes.node_base import node_func

from svrx.util.geom import vectorize



@vectorize
def rand_ints(size, low, high, seed):
    np.random.seed(seed)
    return np.random.randint(low, high, size)


@vectorize
def random_ints(size, low, high, seed):
    np.random.seed(seed)
    return np.random.random_integers(low, high, size)

@vectorize
def random_floats(size, low, high, seed):
    np.random.seed(seed)
    #  here we could be clever and only scale if needed.
    return (high - low ) * np.random.random_sample(size) + low


@node_func(bl_idname="SvRxNumberRandom", multi_label="Random", id=0)
def random_int(size: Int = 1, low: Int = 0, high: Int = 10, seed: Int = 1) -> [Int]:
    """Return random integers from low (inclusive) to high (inclusive)
    """
    return list(random_ints(size, low, high, seed))


@node_func(bl_idname="SvRxNumberRandom", id=1)
def randint(size: Int = 1, low: Int = 0, high: Int = 10, seed: Int = 1) -> [Int]:
    """Return random integers from low (inclusive) to high (exclusive)
    """
    return list(rand_ints(size, low, high, seed))


@node_func(bl_idname="SvRxNumberRandom", id=2)
def random_float(size: Int = 1, low: Float = 0.0, high: Float = 1.0, seed: Int = 1) -> [Float]:
    return list(random_floats(size, low, high, seed))
