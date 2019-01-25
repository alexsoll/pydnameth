function plot_linreg(plot_data)

hold all;
h = scatter(plot_data.scatter_x, plot_data.scatter_y, 'MarkerEdgeColor', plot_data.color, 'SizeData', 100, 'MarkerFaceColor', 'w', 'MarkerFaceAlpha', 0.5);
set(get(get(h, 'Annotation'), 'LegendInformation'), 'IconDisplayStyle', 'off');

hold all;
h = plot(plot_data.line_x, plot_data.line_y, '-', 'LineWidth', 3);
legend(h, plot_data.line_name);
set(h, 'Color', plot_data.color)
set(gca, 'FontSize', 30);
xlabel('age', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel('$\beta$', 'Interpreter', 'latex');
xlim([plot_data.line_x(1) - (plot_data.line_x(2) - plot_data.line_x(1)) * 0.1, plot_data.line_x(2) + (plot_data.line_x(2) - plot_data.line_x(1)) * 0.1])

if plot_data.is_plot_regions == 1
    hold all;
    h = plot(plot_data.line_x, plot_data.line_y_down, '-', 'LineWidth', 2, 'Color', plot_data.color);
    set(get(get(h, 'Annotation'), 'LegendInformation'), 'IconDisplayStyle', 'off');
    
    hold all;
    h = plot(plot_data.line_x, plot_data.line_y_up, '-', 'LineWidth', 2, 'Color', plot_data.color);
    set(get(get(h, 'Annotation'), 'LegendInformation'), 'IconDisplayStyle', 'off');
end

box on;

end
