import util
class store():
    def __init__(self):
        self.bankIdPool = util.get_random_id_pool(2)
        self.banks = {}
        