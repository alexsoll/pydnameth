function ages = get_ages(config)
age_ann = 'age';
gender_ann = 'gender';
disease_ann = 'disease';

fn = sprintf('%s/%s/attribute.txt', config.up, config.data_base);
ann = importdata(fn);

keys = strsplit(string(ann{1}), ' ')';
age_id = 0;
gender_id = 0;
disease_id = 0;
for key_id = 1:size(keys, 1)
    if strcmp(string(keys{key_id}), age_ann)
        age_id = key_id;
    end
    if strcmp(string(keys{key_id}), gender_ann)
        gender_id = key_id;
    end
    if strcmp(string(keys{key_id}), disease_ann)
        disease_id = key_id;
    end
end

ages = zeros(size(ann, 1)-1, 1);
for id = 2:size(ann, 1)
    vals = strsplit(string(ann{id}), ' ')';
    curr_ann = str2double(string(vals{age_id}));
    ages(id-1) = curr_ann;
end

end