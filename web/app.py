import logging

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from layout import layout_func

log = logging.getLogger(__name__)
log.setLevel('DEBUG')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Synthesis recommender app v1'
app.scripts.config.serve_locally = True
route = dcc.Location(id='url', refresh=False)


HOME_LAYOUT = layout_func(app)

app.layout = html.Div([route,
                       html.Div(id='page-content', children=[HOME_LAYOUT])])
app.config.suppress_callback_exceptions = True  # TODO: remove this?

# BUILD_LAYOUT = build_layout(app)
# PREDICT_LAYOUT = predict_layout(app)
# TEST_LAYOUT = html.Div("Test page")
#
#
# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname and pathname != '/':
#         log.info("Pathname %s", pathname)
#         key_from_path = pathname[1:].replace('/', '.')
#         return get(path_map, key_from_path)
#     return HOME_LAYOUT
#
#
# # Map of paths
# path_map = {"home": HOME_LAYOUT,
#             # "build": BUILD_LAYOUT,
#             "predict": PREDICT_LAYOUT,
#             "test": TEST_LAYOUT
#            }

if __name__ == '__main__':
    app.run_server(debug=True)
