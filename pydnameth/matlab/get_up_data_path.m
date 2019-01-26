function up = get_up_data_path()
if strcmp(getenv('computername'), 'MSI')
    up = 'D:/YandexDisk/Work/dna-methylation';
elseif strcmp(getenv('computername'), 'DESKTOP-4BEQ7MS')
    up = 'C:/Users/User/YandexDisk/dna-methylation';
else
    up = 'E:/YandexDisk/Work/dna-methylation';
end
end