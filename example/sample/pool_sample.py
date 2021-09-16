# Import package pyocean
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

from pyocean import SimplePool, RunningMode


def function(index):
    print(f"This isfunction with index {index}")
    time.sleep(3)
    return "Return Value"


pool = SimplePool(mode=RunningMode.Parallel, pool_size=3, tasks_size=5)
pool.initial()
pool.async_apply(function=function, kwargs={"index": f"test_{random.randrange(1, 10)}"})
pool.close()
result = pool.get_result()
print(f"This is final result: {result}")