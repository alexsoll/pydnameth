function [names, data] = get_neutral_data(config)

name = '';
if isfield(config, 'name')
    name = config.name;
end

fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    name);
raw_data = importdata(fn, ' ');

names = raw_data.textdata(2:end, 1);
d_tmp = raw_data.data;

map = containers.Map();
for id = 1:size(names, 1)
    map(string(names(id))) = d_tmp(id, :);
end

all_names =  strings(size(d_tmp, 1), 1);
num_names = 1;

all_data = zeros(size(d_tmp, 1), size(d_tmp, 2));
for id = 1:size(names, 1)
    name = string(names(id));
    all_names(num_names) = string(name);
    data_curr = map(name);
    all_data(num_names, :) = data_curr;
    num_names = num_names + 1;
    if mod(id, 1000) == 0
        id = id
    end
end
num_names = num_names - 1;

all_names = all_names(1:num_names);
all_data = all_data(1:num_names, :);

names = all_names;
data = all_data;

end