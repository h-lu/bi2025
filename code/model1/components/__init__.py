"""UI组件包，提供可复用的组件"""

from .charts import (
    show_categorical_analysis, show_numeric_analysis, show_correlation_analysis,
    show_scatter_plot_matrix, show_time_series_analysis, show_wordcloud_component,
    show_grouped_analysis
)

from .forms import (
    url_input_form, fetch_url_content, text_analysis_form, file_upload_form,
    data_cleaning_form, visualization_form
)

from .tables import (
    show_dataframe_info, show_data_with_filters, show_summary_stats,
    show_correlation_table, show_category_breakdown, show_pivot_table,
    show_missing_data_analysis
)

from .text_displays import (
    show_code_block, show_api_response, show_html_preview, show_tutorial,
    show_info_card, show_steps, show_markdown_file, show_warning_box,
    show_success_box, show_error_box, show_info_box
)

__all__ = [
    # Charts
    'show_categorical_analysis', 'show_numeric_analysis', 'show_correlation_analysis',
    'show_scatter_plot_matrix', 'show_time_series_analysis', 'show_wordcloud_component',
    'show_grouped_analysis',
    
    # Forms
    'url_input_form', 'fetch_url_content', 'text_analysis_form', 'file_upload_form',
    'data_cleaning_form', 'visualization_form',
    
    # Tables
    'show_dataframe_info', 'show_data_with_filters', 'show_summary_stats',
    'show_correlation_table', 'show_category_breakdown', 'show_pivot_table',
    'show_missing_data_analysis',
    
    # Text Displays
    'show_code_block', 'show_api_response', 'show_html_preview', 'show_tutorial',
    'show_info_card', 'show_steps', 'show_markdown_file', 'show_warning_box',
    'show_success_box', 'show_error_box', 'show_info_box'
]
