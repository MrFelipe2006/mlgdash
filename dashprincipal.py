import pandas as pd
import plotly.express as px
import dash
from dash import html, Input, Output, dcc, dash_table, State, ctx, no_update
import dash_bootstrap_components as dbc

from database import (
    obtenerestudiantes, agregar_estudiante, eliminar_estudiante
)

# ── Paleta MLG ────────────────────────────────────────────────────────────────
PURPLE      = "#7f00ff"
PURPLE_DARK = "#5500cc"
CYAN        = "#00f0ff"
GREEN_NEO   = "#39ff14"
BG_CARD     = "rgba(5,0,20,0.88)"
BG_PAGE     = "#050010"
TEXT_MAIN   = "#e8e0ff"
TEXT_DIM    = "rgba(127,0,255,0.65)"

CARD_STYLE = {
    "background": BG_CARD,
    "border": f"1.5px solid {PURPLE}55",
    "borderRadius": "4px",
    "padding": "20px",
    "marginBottom": "20px",
    "boxShadow": f"0 4px 32px rgba(0,0,0,0.7), 0 0 20px {PURPLE}22",
}

KPI_COLORS = [PURPLE, CYAN, GREEN_NEO]


def make_kpi(label, value, color):
    return html.Div([
        html.P(label, style={"color": color,
                             "fontSize": "11px",
                             "letterSpacing": "3px",
                             "textTransform": "uppercase",
                             "marginBottom": "4px",
                             "textShadow": f"0 0 8px {color}"}),
        html.H2(str(value), style={"color": TEXT_MAIN,
                                    "fontWeight": "800",
                                    "fontSize": "2rem",
                                    "margin": 0,
                                    "textShadow": f"0 0 12px {color}66"}),
    ], style={
        "background": f"linear-gradient(135deg, {color}22, {color}08)",
        "border": f"1.5px solid {color}55",
        "borderRadius": "4px",
        "padding": "18px 24px",
        "minWidth": "140px",
        "flex": "1",
        "margin": "0 8px",
        "textAlign": "center",
    })


def creartablero(server):
    app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/dashprincipal/",
        suppress_callback_exceptions=True,
        external_stylesheets=[
            "https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap"
        ],
        title="MLG DASH 360"
    )

    # ── Layout ────────────────────────────────────────────────────────────────
    app.layout = html.Div([

        # ── Body ────────────────────────────────────────────────────────────
        html.Div([

            # ── Filtros ─────────────────────────────────────────────────────
            html.Div([
                html.Div([
                    html.Label("Carrera", style={"color": TEXT_DIM,
                                                 "fontSize": "10px",
                                                 "letterSpacing": "3px",
                                                 "textTransform": "uppercase"}),
                    dcc.Dropdown(
                        id="filtro_carrera",
                        clearable=False,
                        style={"background": BG_CARD, "color": BG_PAGE}
                    ),
                ], style={"flex": "1", "minWidth": "200px"}),

                html.Div([
                    html.Label("Rango de edad", style={"color": TEXT_DIM,
                                                       "fontSize": "10px",
                                                       "letterSpacing": "3px",
                                                       "textTransform": "uppercase"}),
                    dcc.RangeSlider(id="slider_edad", step=1,
                                    tooltip={"placement": "bottom",
                                             "always_visible": True}),
                ], style={"flex": "2", "minWidth": "220px"}),

                html.Div([
                    html.Label("Rango promedio", style={"color": TEXT_DIM,
                                                        "fontSize": "10px",
                                                        "letterSpacing": "3px",
                                                        "textTransform": "uppercase"}),
                    dcc.RangeSlider(id="slider_promedio", min=0, max=5,
                                    step=0.5, value=[0, 5],
                                    tooltip={"placement": "bottom",
                                             "always_visible": True}),
                ], style={"flex": "2", "minWidth": "220px"}),
            ], style={
                **CARD_STYLE,
                "display": "flex",
                "gap": "32px",
                "flexWrap": "wrap",
                "alignItems": "flex-end",
            }),

            # ── KPIs ────────────────────────────────────────────────────────
            html.Div(id="kpis", style={"display": "flex",
                                       "gap": "0",
                                       "flexWrap": "wrap",
                                       "marginBottom": "20px"}),

            # ── Tabla ───────────────────────────────────────────────────────
            html.Div([
                html.H3("💥 ESTUDIANTES", style={"color": PURPLE,
                                                  "fontSize": "13px",
                                                  "letterSpacing": "4px",
                                                  "marginBottom": "12px",
                                                  "textTransform": "uppercase",
                                                  "fontFamily": "Orbitron",
                                                  "textShadow": f"0 0 12px {PURPLE}"}),
                dcc.Loading(
                    dash_table.DataTable(
                        id="tabla",
                        page_size=8,
                        filter_action="native",
                        sort_action="native",
                        row_selectable="multi",
                        selected_rows=[],
                        style_table={"overflowX": "auto", "borderRadius": "4px"},
                        style_header={"backgroundColor": f"{PURPLE}22",
                                      "color": CYAN,
                                      "fontWeight": "700",
                                      "border": f"1px solid {PURPLE}44",
                                      "letterSpacing": "2px",
                                      "fontSize": "11px",
                                      "fontFamily": "Orbitron"},
                        style_cell={"textAlign": "center",
                                    "backgroundColor": "rgba(5,0,20,0.75)",
                                    "color": TEXT_MAIN,
                                    "border": f"1px solid {PURPLE}22",
                                    "fontFamily": "Rajdhani",
                                    "fontSize": "13px"},
                        style_data_conditional=[
                            {"if": {"state": "selected"},
                             "backgroundColor": f"{PURPLE}33",
                             "border": f"1px solid {CYAN}88"}
                        ],
                    ),
                    type="circle",
                    color=PURPLE,
                ),
            ], style=CARD_STYLE),

            # ── Agregar estudiante ───────────────────────────────────────────
            html.Div([
                html.H3("➕ AGREGAR ESTUDIANTE", style={"color": CYAN,
                                                         "fontSize": "13px",
                                                         "letterSpacing": "4px",
                                                         "marginBottom": "16px",
                                                         "textTransform": "uppercase",
                                                         "fontFamily": "Orbitron",
                                                         "textShadow": f"0 0 10px {CYAN}"}),
                html.Div([
                    _input_field("Nombre",  "inp_nombre",  "text",   "ej. Player420"),
                    _input_field("Edad",    "inp_edad",    "number", "18"),
                    _input_field("Carrera", "inp_carrera", "text",   "Fisica / Ingenieria / Matematicas"),
                    _input_field("Nota 1",  "inp_nota1",   "number", "0-5"),
                    _input_field("Nota 2",  "inp_nota2",   "number", "0-5"),
                    _input_field("Nota 3",  "inp_nota3",   "number", "0-5"),
                ], style={"display": "flex", "gap": "12px", "flexWrap": "wrap"}),
                html.Div([
                    html.Button("⚡ AGREGAR", id="btn_agregar",
                                style=_btn_style()),
                    html.Button("💀 ELIMINAR SELECCIONADOS", id="btn_eliminar",
                                style=_btn_style("#cc0033", "#ff0055")),
                ], style={"display": "flex", "gap": "12px", "marginTop": "16px"}),
                html.Div(id="msg_accion", style={"marginTop": "10px",
                                                 "color": GREEN_NEO,
                                                 "fontSize": "12px",
                                                 "letterSpacing": "2px",
                                                 "fontFamily": "Orbitron",
                                                 "textShadow": f"0 0 8px {GREEN_NEO}"}),
            ], style=CARD_STYLE),

            # ── Gráfico detallado ────────────────────────────────────────────
            html.Div([
                html.H3("🎯 ANÁLISIS DETALLADO (selecciona filas)", style={
                    "color": CYAN, "fontSize": "13px",
                    "letterSpacing": "3px", "marginBottom": "8px",
                    "textTransform": "uppercase",
                    "fontFamily": "Orbitron",
                    "textShadow": f"0 0 10px {CYAN}"}),
                dcc.Loading(dcc.Graph(id="gra_detallado"),
                            type="default", color=CYAN),
            ], style=CARD_STYLE),

            # ── Tabs ────────────────────────────────────────────────────────
            html.Div([
                dcc.Tabs(id="tabs", value="histo", children=[
                    dcc.Tab(label="📊 HISTOGRAMA",  value="histo",
                            style=_tab_style(), selected_style=_tab_sel()),
                    dcc.Tab(label="🔵 DISPERSIÓN",  value="disp",
                            style=_tab_style(), selected_style=_tab_sel()),
                    dcc.Tab(label="🥧 DESEMPEÑO",   value="pie",
                            style=_tab_style(), selected_style=_tab_sel()),
                    dcc.Tab(label="📈 POR CARRERA", value="barras",
                            style=_tab_style(), selected_style=_tab_sel()),
                ]),
                dcc.Graph(id="tab_graph"),
            ], style=CARD_STYLE),

        ], style={"maxWidth": "1300px", "margin": "0 auto", "padding": "28px 24px"}),

        # Stores
        dcc.Store(id="store_refresh", data=0),

    ], style={
        "minHeight": "100vh",
        "background": f"linear-gradient(135deg, {BG_PAGE} 0%, #0a0020 50%, {BG_PAGE} 100%)",
        "fontFamily": "'Rajdhani', sans-serif",
    })

    # ── Cargar opciones al iniciar ───────────────────────────────────────────
    @app.callback(
        Output("filtro_carrera", "options"),
        Output("filtro_carrera", "value"),
        Output("slider_edad", "min"),
        Output("slider_edad", "max"),
        Output("slider_edad", "value"),
        Input("store_refresh", "data"),
    )
    def cargar_filtros(_):
        df = obtenerestudiantes()
        carreras = sorted(df["Carrera"].unique())
        opts = [{"label": c, "value": c} for c in carreras]
        return (opts, carreras[0],
                int(df["Edad"].min()), int(df["Edad"].max()),
                [int(df["Edad"].min()), int(df["Edad"].max())])

    # ── Callback principal ───────────────────────────────────────────────────
    @app.callback(
        Output("tabla", "data"),
        Output("tabla", "columns"),
        Output("kpis", "children"),
        Input("filtro_carrera", "value"),
        Input("slider_edad", "value"),
        Input("slider_promedio", "value"),
        Input("store_refresh", "data"),
    )
    def actualizar_comp(carrera, rangoedad, rangoprome, _):
        if carrera is None:
            return [], [], []
        df = obtenerestudiantes()
        filtro = df[
            (df["Carrera"] == carrera) &
            (df["Edad"] >= rangoedad[0]) &
            (df["Edad"] <= rangoedad[1]) &
            (df["Promedio"] >= rangoprome[0]) &
            (df["Promedio"] <= rangoprome[1])
        ]

        promedio = round(filtro["Promedio"].mean(), 2) if len(filtro) else 0
        total    = len(filtro)
        maximo   = round(filtro["Promedio"].max(), 2) if len(filtro) else 0

        kpis = [
            make_kpi("Promedio",          promedio, KPI_COLORS[0]),
            make_kpi("Total estudiantes", total,    KPI_COLORS[1]),
            make_kpi("Máximo",            maximo,   KPI_COLORS[2]),
        ]

        cols = [{"name": c, "id": c} for c in filtro.columns]
        return filtro.to_dict("records"), cols, kpis

    # ── Tabs ─────────────────────────────────────────────────────────────────
    @app.callback(
        Output("tab_graph", "figure"),
        Input("tabs", "value"),
        Input("filtro_carrera", "value"),
        Input("slider_edad", "value"),
        Input("slider_promedio", "value"),
        Input("store_refresh", "data"),
    )
    def actualizar_tab(tab, carrera, rangoedad, rangoprome, _):
        if carrera is None:
            return _empty_fig()
        df = obtenerestudiantes()
        filtro = df[
            (df["Carrera"] == carrera) &
            (df["Edad"] >= rangoedad[0]) &
            (df["Edad"] <= rangoedad[1]) &
            (df["Promedio"] >= rangoprome[0]) &
            (df["Promedio"] <= rangoprome[1])
        ]
        template = "plotly_dark"
        paper    = "rgba(5,0,20,0)"
        plot_bg  = "rgba(5,0,20,0)"

        if tab == "histo":
            fig = px.histogram(filtro, x="Promedio", nbins=10,
                               title="DISTRIBUCIÓN DE PROMEDIOS",
                               color_discrete_sequence=[PURPLE],
                               template=template)
        elif tab == "disp":
            fig = px.scatter(filtro, x="Edad", y="Promedio",
                             color="Desempeño", trendline="ols",
                             title="EDAD VS PROMEDIO",
                             template=template)
        elif tab == "pie":
            fig = px.pie(filtro, names="Desempeño",
                         title="DISTRIBUCIÓN POR DESEMPEÑO",
                         color_discrete_sequence=[PURPLE, CYAN, GREEN_NEO, "#ff00ff"],
                         template=template)
        else:
            promedios = df.groupby("Carrera")["Promedio"].mean().reset_index()
            fig = px.bar(promedios, x="Carrera", y="Promedio",
                         color="Carrera",
                         title="PROMEDIO GENERAL POR CARRERA",
                         color_discrete_sequence=[PURPLE, CYAN, GREEN_NEO],
                         template=template)

        fig.update_layout(paper_bgcolor=paper, plot_bgcolor=plot_bg,
                          font_color=TEXT_MAIN,
                          font_family="Rajdhani",
                          title_font_family="Orbitron")
        return fig

    # ── Detallado ────────────────────────────────────────────────────────────
    @app.callback(
        Output("gra_detallado", "figure"),
        Input("tabla", "derived_virtual_data"),
        Input("tabla", "derived_virtual_selected_rows"),
    )
    def actualizartab(rows, selected_rows):
        if not rows:
            return _empty_fig("Selecciona filas de la tabla para ver el análisis")
        dff = pd.DataFrame(rows)
        if selected_rows:
            dff = dff.iloc[selected_rows]
        if dff.empty:
            return _empty_fig("Sin filas seleccionadas")
        fig = px.scatter(dff, x="Edad", y="Promedio", color="Desempeño",
                         size="Promedio",
                         title="ANÁLISIS DETALLADO",
                         trendline="ols",
                         template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(5,0,20,0)",
                          plot_bgcolor="rgba(5,0,20,0)",
                          font_color=TEXT_MAIN,
                          font_family="Rajdhani",
                          title_font_family="Orbitron")
        return fig

    # ── Agregar / Eliminar ────────────────────────────────────────────────────
    @app.callback(
        Output("store_refresh", "data"),
        Output("msg_accion", "children"),
        Output("inp_nombre",  "value"),
        Output("inp_edad",    "value"),
        Output("inp_carrera", "value"),
        Output("inp_nota1",   "value"),
        Output("inp_nota2",   "value"),
        Output("inp_nota3",   "value"),
        Input("btn_agregar",  "n_clicks"),
        Input("btn_eliminar", "n_clicks"),
        State("inp_nombre",  "value"),
        State("inp_edad",    "value"),
        State("inp_carrera", "value"),
        State("inp_nota1",   "value"),
        State("inp_nota2",   "value"),
        State("inp_nota3",   "value"),
        State("tabla", "derived_virtual_data"),
        State("tabla", "derived_virtual_selected_rows"),
        State("store_refresh", "data"),
        prevent_initial_call=True,
    )
    def manejar_acciones(n_add, n_del,
                         nombre, edad, carrera, n1, n2, n3,
                         rows, sel_rows, refresh):
        triggered = ctx.triggered_id
        blank = ("", None, "", None, None, None)

        if triggered == "btn_agregar":
            if not all([nombre, edad, carrera,
                        n1 is not None, n2 is not None, n3 is not None]):
                return no_update, "⚠️ COMPLETA TODOS LOS CAMPOS", no_update, no_update, no_update, no_update, no_update, no_update
            try:
                prom, desemp = agregar_estudiante(
                    nombre, int(edad), carrera,
                    float(n1), float(n2), float(n3)
                )
                msg = f"✅ '{nombre}' AGREGADO — PROMEDIO: {prom} ({desemp.upper()})"
                return refresh + 1, msg, *blank
            except Exception as e:
                return no_update, f"❌ ERROR: {e}", no_update, no_update, no_update, no_update, no_update, no_update

        if triggered == "btn_eliminar":
            if not rows or not sel_rows:
                return no_update, "⚠️ SELECCIONA FILAS DE LA TABLA PRIMERO", no_update, no_update, no_update, no_update, no_update, no_update
            ids = [rows[i]["Id"] for i in sel_rows]
            for id_est in ids:
                eliminar_estudiante(id_est)
            return refresh + 1, f"💀 {len(ids)} ESTUDIANTE(S) ELIMINADO(S)", no_update, no_update, no_update, no_update, no_update, no_update

        return no_update, "", no_update, no_update, no_update, no_update, no_update, no_update

    return app


# ── Helpers ──────────────────────────────────────────────────────────────────

def _input_field(label, id_, type_, placeholder):
    return html.Div([
        html.Label(label, style={"color": TEXT_DIM,
                                 "fontSize": "10px",
                                 "letterSpacing": "3px",
                                 "textTransform": "uppercase",
                                 "display": "block",
                                 "marginBottom": "4px",
                                 "fontFamily": "Orbitron"}),
        dcc.Input(id=id_, type=type_, placeholder=placeholder,
                  style={"background": "rgba(127,0,255,0.07)",
                         "border": f"1.5px solid {PURPLE}44",
                         "borderRadius": "3px",
                         "color": TEXT_MAIN,
                         "padding": "9px 12px",
                         "fontSize": "13px",
                         "fontFamily": "Rajdhani",
                         "outline": "none",
                         "width": "100%",
                         "caretColor": CYAN}),
    ], style={"flex": "1", "minWidth": "130px"})


def _btn_style(bg=PURPLE_DARK, hover=None):
    accent = CYAN if bg == PURPLE_DARK else "#ff0055"
    return {
        "background": f"linear-gradient(90deg, {bg}, {PURPLE if bg == PURPLE_DARK else bg})",
        "color": "#fff",
        "border": f"1px solid {accent}55",
        "borderRadius": "3px",
        "padding": "10px 22px",
        "fontFamily": "Orbitron",
        "fontWeight": "700",
        "fontSize": "12px",
        "letterSpacing": "2px",
        "cursor": "pointer",
        "boxShadow": f"0 4px 16px {bg}66",
        "textShadow": f"0 0 8px {accent}",
    }


def _tab_style():
    return {"background": "rgba(5,0,20,0.7)",
            "color": TEXT_DIM,
            "border": f"1px solid {PURPLE}33",
            "borderRadius": "3px 3px 0 0",
            "padding": "8px 18px",
            "fontSize": "11px",
            "letterSpacing": "2px",
            "fontFamily": "Orbitron"}


def _tab_sel():
    return {**_tab_style(),
            "background": f"{PURPLE}33",
            "color": CYAN,
            "border": f"1.5px solid {CYAN}77",
            "fontWeight": "800",
            "textShadow": f"0 0 8px {CYAN}"}


def _empty_fig(title="SIN DATOS"):
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.update_layout(title=title,
                      paper_bgcolor="rgba(5,0,20,0)",
                      plot_bgcolor="rgba(5,0,20,0)",
                      font_color=TEXT_DIM,
                      font_family="Orbitron")
    return fig