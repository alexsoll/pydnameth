def get_file_name(config):
    fn = ''
    if bool(config.experiment.params):
        params_keys = list(config.experiment.params.keys())
        if len(params_keys) > 0:
            params_keys.sort()
            fn += '_'.join([key + '(' + str(config.experiment.params[key]) + ')'
                            for key in params_keys])

    if fn == '':
        fn = 'default'

    return fn
