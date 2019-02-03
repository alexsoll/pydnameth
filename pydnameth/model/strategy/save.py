import abc
from pydnameth.infrastucture.save.figure import save_figure
from pydnameth.infrastucture.save.table import save_table_dict
from pydnameth.infrastucture.path import get_save_path


class SaveStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save_base(self, config):
        pass

    @abc.abstractmethod
    def save_advanced(self, config, configs_primary):
        pass

    @abc.abstractmethod
    def save_plot(self, config, configs_primary):
        pass


class TableSaveStrategy(SaveStrategy):

    def save_base(self, config):
        fn = get_save_path(config) + '/' + \
             config.setup.get_file_name()
        save_table_dict(fn, config.metrics)

    def save_advanced(self, config, configs_primary):
        fn = get_save_path(config) + '/' + \
             config.setup.get_file_name()
        save_table_dict(fn, config.metrics)

    def save_plot(self, config, configs_primary):
        pass


class ClockSaveStrategy(SaveStrategy):

    def save_base(self, config):
        fn = get_save_path(config) + '/' + \
             config.setup.get_file_name()
        save_table_dict(fn, config.metrics)

    def save_advanced(self, config, configs_primary):
        fn = get_save_path(config) + '/' + \
             config.setup.get_file_name()
        save_table_dict(fn, config.metrics)

    def save_plot(self, config, configs_primary):
        pass


class MethylationSaveStrategy(SaveStrategy):

    def save_base(self, config):
        pass

    def save_advanced(self, config, configs_primary):
        pass

    def save_plot(self, config, configs_primary):
        save_figure(config, config.plot_data['fig'])


class ObservablesSaveStrategy(SaveStrategy):

    def save_base(self, config):
        pass

    def save_advanced(self, config, configs_primary):
        pass

    def save_plot(self, config, configs_primary):
        save_figure(config, config.plot_data['fig'])
