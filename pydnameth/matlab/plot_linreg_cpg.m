function plot_linreg_cpg(config, cpg)

fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    config.name);

top_data = importdata(fn);

cpgs = string(top_data.textdata);
intercepts = top_data.data(:, 2);
slopes = top_data.data(:, 3);
intercepts_std = top_data.data(:, 4);
slopes_std = top_data.data(:, 5);

indexes = get_attributes_indexes(config);
ages = get_ages(config);

ages_passed = zeros(size(indexes, 1), 1);
for id = 1:size(indexes, 1)
    index = indexes(id);
    ages_passed(id) = ages(index);
end

fn = sprintf('%s/%s/cpg_beta.txt', config.up, config.data_base);
fid = fopen(fn);
data = textscan(fid, '%s %*[^\n]','HeaderLines',1);
frewind(fid)
all_cpgs = data{1};
idx = find(string(all_cpgs)==string(cpg))
target_row = textscan(fid,'%s',1,'delimiter','\n', 'headerlines', idx-1);
tline = strsplit(fgetl(fid), '\t');
curr_cpg = string(tline(1));
cpg_data = str2double(tline(2:end))';
fclose(fid);

cpg_data_passed = size(indexes, 1);
for id = 1:size(indexes, 1)
    cpg_data_passed(id) = cpg_data(indexes(id));
end

cpg_id = find(cpgs==cpg);

sigma = 3;

slope = slopes(cpg_id);
intercept = intercepts(cpg_id);
intercept_std = intercepts_std(cpg_id);
slope_std = slopes_std(cpg_id);

x_lin = [min(ages), max(ages)];
y_lin = [slope * x_lin(1) + intercept, slope * x_lin(2) + intercept];

slope_minus = slope - sigma * slope_std;
intercept_minus = intercept - sigma * intercept_std;

slope_plus = slope + sigma * slope_std;
intercept_plus = intercept + sigma * intercept_std;

intercept_up = intercept + ((slope_plus * x_lin(2) + intercept_plus) - (slope * x_lin(2) + intercept));
slope_up = slope;

intercept_down = intercept + ((slope_minus * x_lin(2) + intercept_minus) - (slope * x_lin(2) + intercept));
slope_down = slope;

y_up = [slope_up * x_lin(1) + intercept_up, slope_up * x_lin(2) + intercept_up];
y_down = [slope_down * x_lin(1) + intercept_down, slope_down * x_lin(2) + intercept_down];

plot_data.scatter_x = ages_passed;
plot_data.scatter_y = cpg_data_passed;
plot_data.line_x = x_lin;
plot_data.line_y = y_lin;
plot_data.line_y_down = y_down;
plot_data.line_y_up = y_up;
plot_data.line_name = sprintf('%s: %s', cpg, config.gender);
plot_data.color = config.color;
plot_data.is_plot_regions = config.is_plot_regions;

plot_linreg(plot_data)

end

