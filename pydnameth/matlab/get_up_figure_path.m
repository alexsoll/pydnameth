function up_save = get_up_figure_path()
if strcmp(getenv('computername'), 'MSI')
    up_save = 'C:/Users/user/Google Drive/mlmg/figures';
elseif strcmp(getenv('computername'), 'DESKTOP-4BEQ7MS')
    up_save = 'D:/Aaron/Bio/pymethspec/figures';
else
    up_save = 'C:/Users/user/Google Drive/mlmg/figures';
end
end