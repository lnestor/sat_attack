class KeySpace:
    def __init__(self, ckt):
        self.key_names = ckt.key_inputs()
        self.key_count = len(self.key_names)
        self.invalid_indices = set()

    def remove(self, keys):
        for key in keys:
            self.remove_single(key)

    def remove_single(self, key):
        index = 0

        for i, (name, value) in enumerate(key.items()):
            if value == True:
                index += 2**i

        self.invalid_indices.add(index)

    def __iter__(self):
        self.key_index = 0
        return self

    def __next__(self):
        if self.key_index >= 2**self.key_count:
            raise StopIteration

        if self.key_index in self.invalid_indices:
            self.key_index += 1
            return self.__next__()

        key_values = {}

        for name_index, name in enumerate(self.key_names):
            key_values[name] = int(self.key_index / (2**name_index) % 2) == 1

        self.key_index += 1
        return key_values

    def __len__(self):
        return 2**self.key_count - len(self.invalid_indices)
