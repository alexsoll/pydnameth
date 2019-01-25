function indexes = get_attributes_indexes(config)
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

indexes = [1:size(ann, 1)-1]';

if gender_id > 0
    genders = [];
    for id = 2:size(ann, 1)
        vals = strsplit(string(ann{id}), ' ')';
        curr_ann = string(vals{gender_id});
        genders = vertcat(genders, curr_ann);
    end
    
    if ~strcmp(string(config.gender), 'any')
        curr_indexes = [];
        for id = 1:size(genders, 1)
            if strcmp(genders(id), config.gender)
                curr_indexes = vertcat(curr_indexes, id);
            end
        end
        tmp_indexes = intersect(indexes, curr_indexes);
        indexes = tmp_indexes;
    end
end

if disease_id > 0
    diseases = [];
    for id = 2:size(ann, 1)
        vals = strsplit(string(ann{id}), ' ')';
        curr_ann = string(vals{disease_id});
        diseases = vertcat(diseases, curr_ann);
    end
    
    if ~strcmp(string(config.disease), 'any')
        curr_indexes = [];
        for id = 1:size(diseases, 1)
            if strcmp(diseases(id), config.disease)
                curr_indexes = vertcat(curr_indexes, id);
            end
        end
        tmp_indexes = intersect(indexes, curr_indexes);
        indexes = tmp_indexes;
    end
end

end