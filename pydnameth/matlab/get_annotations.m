function [map, labels] = get_annotations(config)
fn = sprintf('%s/%s/annotation.txt', ...
    config.up, ...
    config.data_base);

delimiter = '\t';
formatSpec = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%[^\n\r]';
fileID = fopen(fn,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string',  'ReturnOnError', false);
fclose(fileID);
annotations = [dataArray{1:end-1}];

labels = annotations(1, 2:end);

map = containers.Map();
for id = 2:size(annotations, 1)
    map(annotations(id, 1)) = annotations(id, 2:end);
end

end