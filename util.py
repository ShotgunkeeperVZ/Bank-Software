import random

def get_random_id_pool(digits):
    pool = [format(i, f'0{digits}d') for i in range(10**digits)]
    random.shuffle(pool)
    return pool



