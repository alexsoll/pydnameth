class Cells:
    def __init__(self,
                 name,
                 types,
                 ):
        self.name = name
        self.types = types

    def __str__(self):
        name = 'cells('
        if isinstance(self.types, list):
            self.types.sort()
            name += '_'.join(self.types)
        elif isinstance(self.types, str):
            name += self.types
        else:
            raise ValueError('Cells.types must be list or str.')
        name += ')'
        return name


class Observables:
    def __init__(self,
                 name,
                 types,
                 ):
        self.name = name
        self.types = types

    def __str__(self):
        name = 'observables('
        if isinstance(self.types, dict):
            str_list = []
            for key, value in self.types.items():
                if isinstance(value, list):
                    value.sort()
                    str_list.append(key + '(' + '_'.join(list(map(str, value))) + ')')
                else:
                    str_list.append(key + '(' + value + ')')
            name += '_'.join(str_list)
        elif isinstance(self.types, str):
            name += self.types
        else:
            raise ValueError('Observables.types must be dict or str.')
        name += ')'
        return name


class Attributes:
    def __init__(self,
                 target,
                 observables,
                 cells,
                 ):
        self.target = target
        self.observables = observables
        self.cells = cells

    def __str__(self):
        name = 'target(' + str(self.target) + ')' + '_' + str(self.observables) + '_' + str(self.cells)
        return name
