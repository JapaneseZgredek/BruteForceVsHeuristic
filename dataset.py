class Dataset:

    def __init__(self):
        self.sizes = []
        self.vals = []

    def init_sizes(self, sizes_list):
        self.sizes = sizes_list

    def init_vals(self, vals_list):
        self.vals = vals_list