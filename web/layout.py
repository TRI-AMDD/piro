import logging
import json
import base64

from monty.json import MontyDecoder, jsanitize
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from piro.route import SynthesisRoutes
from dash.exceptions import PreventUpdate
from fnmatch import fnmatch


logger = logging.getLogger("ml_dash.app")
logger.setLevel('DEBUG')

BOOL_OPTIONS = ["allow_gas_release",
                "show_fraction_known_precursors",
                "show_known_precursors_only",
                "confine_competing_to_icsd",
                "display_peroxides",
                "add_pareto"
                ]

def layout_func(app):
    layout = html.Div([
        dcc.Markdown('Synthesis analyzer'),
        dcc.Input(id="input_mp_id",
                  placeholder="enter mp-id"
                  ),
        html.Button('run', id='run_button'),#, style={"display": "none"}),
        html.Details([
            html.Summary('Advanced options'),
            dcc.Input(id="temperature", placeholder="1600 K"),
            dcc.Input(id="pressure", placeholder="0.001 atm"),
            dcc.Input(id="add_element", placeholder="add element"),
            dcc.Input(id="max_component_precursors", placeholder="2"),
            dcc.Checklist(
                id="synthesis_bool_options",
                options=[{"label": bo, "value": bo} for bo in BOOL_OPTIONS],
                value=["display_peroxides", "add_pareto"]
            )
        ]),
        # dcc.Upload(id='struct_upload_data',
        #            children=html.Div([
        #                html.Span(
        #                    ['Drag and Drop or ',
        #                     html.A('Select File')],
        #                    id='struct_upload_label'),
        #            ]),
        #            style={
        #                'width': '30%',
        #                'height': '100px',
        #                'lineHeight': '60px',
        #                'borderWidth': '1px',
        #                'borderStyle': 'dashed',
        #                'borderRadius': '5px',
        #                'textAlign': 'center',
        #            },
        #            ),
        # dcc.Store(id='data_store', storage_type='memory'),
        html.Div(id='synthesis_output'),
    ])

    @app.callback(Output('synthesis_output', 'children'),
                  [Input('run_button', 'n_clicks')],
                  [State('input_mp_id', 'value'),
                   State('synthesis_bool_options', 'value'),
                   State('temperature', 'value'),
                   State('pressure', 'value'),
                   State('max_component_precursors', 'value'),
                   State('add_element', 'value'),
                   ])
    def update_results(n_clicks, value, synthesis_bool_options,
                       temperature, pressure, max_component_precursors,
                       add_element):
        if value is None:
            raise PreventUpdate

        # Marshall options
        temperature = float(temperature) if temperature else 1600.
        pressure = float(pressure) if pressure else None
        max_component_precursors = int(max_component_precursors) if max_component_precursors else 2
        add_element = add_element
        synthesis_bool_options = {bo: True if bo in synthesis_bool_options else False
                                  for bo in BOOL_OPTIONS}

        # content_type, content_string = contents.split(',')
        # decoded = base64.b64decode(content_string).decode('utf-8')
        # logger.debug("Decoding {}".format(fname))

        # if fnmatch(fname.lower(), "*.cif*") or fnmatch(fname.lower(), "*.mcif*"):
        #     parser = CifParser.from_string(decoded)
        #     structures = parser.get_structures()

        # elif fnmatch(fname.lower(), '*.json'):
        #     structures = json.loads(decoded, cls=MontyDecoder)

        # else:
        #     return "Unsupported file format or filename, " \
        #            "please convert to cif or pymatgen json"

        # prediction = predict_from_structures(structures)

        # table = generate_table(prediction)
        # return table
        router = SynthesisRoutes(value, add_element=add_element)
        fig = router.recommend_routes(
            temperature=temperature,
            pressure=pressure,
            max_component_precursors=max_component_precursors,
            **synthesis_bool_options
        )
        #     allow_gas_release=False,
        #     show_fraction_known_precursors=False,
        #     show_known_precursors_only=False,
        #     confine_competing_to_icsd=False,
        #     display_peroxides=True,
        #     # custom_text=' - 1600K, 10<sup>-3</sup> atm, standard reactants',
        #     # w=640, h=480,
        #     add_pareto=True,
        #           # yrange=(-0.25, 9)
        #           )
        return dcc.Graph(figure=fig)

    return layout


# MAX_ROWS = 10000
def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe.iloc[i][col])) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )


def jsonify(dataframe):
    """Convert dataframe to json"""
    return jsanitize(dataframe, strict=True)

def deserialize(jsoned_obj):
    return json.loads(jsoned_obj, cls=MontyDecoder)


from io import StringIO
import pickle

# Note that these are VERY hackish and probably insecure
# Serializing and deserializing pickles willy-nilly can
# cause BIG problems
def serialize_matpipe(pipe):
    stringio = StringIO()
    for obj in [pipe, pipe.learner, pipe.reducer, pipe.cleaner,
                pipe.autofeaturizer]:
        obj._logger = None
    pickle.dump(pipe, stringio)
    return stringio.getvalue()

def deserialize_matpipe(string):
    stringio = StringIO()
    stringio.write(string)
    obj = pickle.load(stringio)
    return obj
