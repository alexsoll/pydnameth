function [names, data_1, data_2] = get_specific_data(config)

name = '';
if isfield(config, 'name')
    name = config.name;
end

config.gender = 'F';
fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    name);
raw_data_1 = importdata(fn, ' ');

config.gender = 'M';
fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    name);
raw_data_2 = importdata(fn, ' ');


names_1 = raw_data_1.textdata(2:end, 1);
d_1_tmp = raw_data_1.data;

map_1 = containers.Map();
for id = 1:size(names_1, 1)
    map_1(string(names_1(id))) = d_1_tmp(id, :);
end

names_2 = raw_data_2.textdata(2:end, 1);
d_2_tmp = raw_data_2.data;

map_2 = containers.Map();
for id = 1:size(names_1, 1)
    map_2(string(names_2(id))) = d_2_tmp(id, :);
end

all_names =  strings(size(d_1_tmp, 1), 1);
num_names = 1;

all_data_1 = zeros(size(d_1_tmp, 1), size(d_1_tmp, 2));
all_data_2 = zeros(size(d_2_tmp, 1), size(d_2_tmp, 2));
for id_1 = 1:size(names_1, 1)
    name = string(names_1(id_1));
    if isKey(map_2,name)
        all_names(num_names) = string(name);
        data_1_curr = map_1(name);
        data_2_curr = map_2(name);
        all_data_1(num_names, :) = data_1_curr;
        all_data_2(num_names, :) = data_2_curr;
        num_names = num_names + 1;
    end
    if mod(id_1, 1000) == 0
        id_1 = id_1
    end
end
num_names = num_names - 1;

all_names = all_names(1:num_names);
all_data_1 = all_data_1(1:num_names, :);
all_data_2 = all_data_2(1:num_names, :);

names = [];
data_1 = [];
data_2 = [];
    
names = all_names;
data_1 = all_data_1;
data_2 = all_data_2;
    
end