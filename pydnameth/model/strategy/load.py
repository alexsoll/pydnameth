import abc
from pydnameth.config.experiment.types import Task
from pydnameth.infrastucture.load.cpg import load_cpg
from pydnameth.infrastucture.load.residuals_common import load_residuals_common
from pydnameth.infrastucture.load.table import load_table_dict
from pydnameth.infrastucture.load.epimutations import load_epimutations


class LoadStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load(self, config, configs_child):
        pass

    def inherit_childs(self, config, configs_child):
        for config_child in configs_child:
            config_child.base_list = config.base_list
            config_child.base_dict = config.base_dict
            config_child.base_data = config.base_data

    def load_child(self, config_child):

        if config_child.experiment.task == Task.table:

            config_child.advanced_data = load_table_dict(config_child)
            config_child.advanced_list = config_child.base_list
            config_child.advanced_dict = {}
            row_id = 0
            for item in config_child.advanced_data['item']:
                config_child.advanced_dict[item] = row_id
                row_id += 1


class BetasLoadStrategy(LoadStrategy):

    def load(self, config, configs_child):
        load_cpg(config)
        config.base_list = config.cpg_list
        config.base_dict = config.betas_dict
        config.base_data = config.betas_data

        self.inherit_childs(config, configs_child)

        if config.experiment.task == Task.table or config.experiment.task == Task.clock:

            for config_child in configs_child:
                self.load_child(config_child)


class ResidualsCommonLoadStrategy(LoadStrategy):

    def load(self, config, configs_child):
        load_residuals_common(config)
        config.base_list = config.cpg_list
        config.base_dict = config.residuals_dict
        config.base_data = config.residuals_data

        self.inherit_childs(config, configs_child)

        if config.experiment.task == Task.table or config.experiment.task == Task.clock:

            for config_child in configs_child:
                self.load_child(config_child)


class ResidualsSpecialLoadStrategy(LoadStrategy):

    def load(self, config, configs_child):
        BetasLoadStrategy.load(self, config, configs_child)


class EpimutationsLoadStrategy(LoadStrategy):

    def load(self, config, configs_child):
        load_epimutations(config)
        config.base_list = config.cpg_list
        config.base_dict = config.epimutations_dict
        config.base_data = config.epimutations_data

        self.inherit_childs(config, configs_child)


class ObservablesLoadStrategy(LoadStrategy):

    def load(self, config, configs_child):
        pass
