"""
All levels can use only predefined enums
"""


class Experiment:

    def __init__(self,
                 type,
                 task,
                 method,
                 params,
                 ):
        self.type = type
        self.task = task
        self.method = method
        self.params = params

    def __str__(self):
        name = f'{self.type.value}_{self.task.value}_{self.method.value}'
        return name
