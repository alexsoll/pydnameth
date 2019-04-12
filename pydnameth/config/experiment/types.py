from enum import Enum


class Task(Enum):
    table = 'table'
    clock = 'clock'
    plot = 'plot'

    def __str__(self):
        return str(self.value)


class Method(Enum):
    linreg = 'linreg'
    variance_linreg = 'variance_linreg'
    cluster = 'cluster'
    histogram = 'histogram'
    scatter = 'scatter'
    polygon = 'polygon'
    special = 'special'
    z_test_linreg = 'z_test_linreg'
    variance_histogram = 'variance_histogram'
    aggregator = 'aggregator'
    mock = 'mock'
    range = 'range'

    def __str__(self):
        return str(self.value)


class DataType(Enum):
    betas = 'betas'
    residuals_common = 'residuals_common'
    residuals_special = 'residuals_special'
    epimutations = 'epimutations'
    observables = 'observables'
    suppl = 'suppl'
    cache = 'cache'

    def __str__(self):
        return str(self.value)
