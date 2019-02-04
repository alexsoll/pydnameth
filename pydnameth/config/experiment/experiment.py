"""
All levels can use only predefined enums
"""


class Experiment:

    def __init__(self,
                 task,
                 method,
                 params,
                 ):
        self.task = task
        self.method = method
        self.params = params

    def __str__(self):
        name = f'{self.task.value}_{self.method.value}'
        return name
