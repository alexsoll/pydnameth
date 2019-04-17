"""
All levels can use only predefined enums
"""


class Experiment:

    def __init__(self,
                 data,
                 task,
                 method,
                 data_params=None,
                 task_params=None,
                 method_params=None,
                 ):
        self.data = data
        self.task = task
        self.method = method
        self.data_params = data_params
        self.task_params = task_params
        self.method_params = method_params

    def __str__(self):
        return self.get_experiment_str()

    def get_experiment_str(self):
        data_params_str = self.get_data_params_str()
        if data_params_str != '':
            name = f'{self.data.value}({data_params_str})_{self.task.value}_{self.method.value}'
        else:
            name = f'{self.data.value}_{self.task.value}_{self.method.value}'
        return name

    def get_params_str(self, params):
        params_str = ''
        if bool(params):
            params_keys = list(params.keys())
            if len(params_keys) > 0:
                params_keys.sort()
                params_str += '_'.join([key + '(' + str(params[key]) + ')' for key in params_keys])
        return params_str

    def get_data_params_str(self):
        params_str = self.get_params_str(self.data_params)
        return params_str

    def get_task_params_str(self):
        params_str = self.get_params_str(self.task_params)
        return params_str

    def get_method_params_str(self):
        params_str = self.get_params_str(self.method_params)

        if params_str == '':
            params_str = 'default'

        return params_str
