import logging
import json
import base64

from monty.json import MontyDecoder, jsanitize
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from piro.route import SynthesisRoutes
from dash.exceptions import PreventUpdate
from pymatgen.ext.matproj import MPRester
from pymatgen.core.composition import Composition
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

BOOL_TOOLTIPS = {"allow_gas_release": "Allow for gaseous reaction products, e.g. O2, CO2",
                 "show_fraction_known_precursors": "Show the fraction of known synthetic reagents in reaction",
                 "show_known_precursors_only": "Show only reactions with known precursors",
                 "confine_competing_to_icsd": "Confine competing reactions to those containing ICSD materials",
                 "display_peroxides": "Show reactions involving peroxide compounds",
                 "add_pareto": "Show the Pareto front on the reaction analysis diagram"
                 }

INPUT_WIDTH = "150px"
JUSTIFY = "left"


def layout_func(app):
    layout = html.Div([
        html.H1('Synthesis analyzer'),
        dcc.Input(id="input_mp_id",
                  placeholder="enter mp-id or formula"
                  ),
        html.Button('run', id='run_button'),#, style={"display": "none"}),
        html.Details([
            html.Summary('Advanced options'),
            html.Div([
                html.Span("Temperature", style={"width": INPUT_WIDTH, "float": JUSTIFY}),
                dcc.Input(id="temperature", placeholder="1600 K")]
            ),
            html.Div([
                html.Span("Pressure", style={"width": INPUT_WIDTH, "float": JUSTIFY}),
                dcc.Input(id="pressure", placeholder="0.001 atm"),
            ]),
            html.Div([
                html.Span("Add element", style={"width": INPUT_WIDTH, "float": JUSTIFY}),
                dcc.Input(id="add_element", placeholder="None"),
            ]),
            html.Div([
                html.Span("Max precursors", style={"width": INPUT_WIDTH, "float": JUSTIFY}),
                dcc.Input(id="max_component_precursors", placeholder="2"),
            ]),
            dcc.Checklist(
                id="synthesis_bool_options",
                options=[{"label": BOOL_TOOLTIPS[bo], "value": bo} for bo in BOOL_OPTIONS],
                value=["display_peroxides", "add_pareto"]
            )
        ]),
        dcc.Loading(id='loading-1',
                    children=[html.Div(id='synthesis_output')],
                    type="cube"
                    )
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

        try:
            # Marshall options
            temperature = float(temperature) if temperature else 1600.
            pressure = float(pressure) if pressure else None
            max_component_precursors = int(max_component_precursors) if max_component_precursors else 2
            add_element = add_element
            synthesis_bool_options = {bo: True if bo in synthesis_bool_options else False
                                      for bo in BOOL_OPTIONS}

            if not value.startswith("mp"):
                with MPRester() as mpr:
                    formula = Composition(value).reduced_formula
                    options = mpr.query({"pretty_formula": formula}, ['material_id', 'e_above_hull'])
                    if not options:
                        raise ValueError("{} query failed, please enter valid formula or mp id".format(value))
                    options = sorted(options, key=lambda x: x['e_above_hull'])
                    value = options[0]['material_id']
            router = SynthesisRoutes(value, add_element=add_element)
            fig = router.recommend_routes(
                temperature=temperature,
                pressure=pressure,
                max_component_precursors=max_component_precursors,
                **synthesis_bool_options
            )
            return dcc.Graph(figure=fig)
        except Exception as e:
            return html.Div(children=[str(e)],
                            style={'color': 'red'})

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
