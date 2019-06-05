import graphviz
import copy
from collections import defaultdict

import sunpy.coordinates

from astropy.coordinates.transformations import TransformGraph, trans_to_color

from astropy.coordinates import frame_transform_graph
import astropy.coordinates.builtin_frames

transform_graph = frame_transform_graph

sunpy_label_map = {sunpy.coordinates.frames.Helioprojective: "Helioprojective Cartesian",
                   sunpy.coordinates.frames.Heliocentric: "Heliocentric Cartesian",
                   sunpy.coordinates.frames.HeliographicStonyhurst: "Heliographic Stonyhurst\nHeliocentric Earth Equatorial",
                   sunpy.coordinates.frames.HeliographicCarrington: "Heliographic Carrington"}
astropy_label_map = {astropy.coordinates.builtin_frames.ICRS: "ICRS",
                     astropy.coordinates.builtin_frames.HCRS: "HCRS",
                     astropy.coordinates.builtin_frames.HeliocentricTrueEcliptic: "Heliocentric Aries Ecliptic"}

label_map = {**sunpy_label_map, **astropy_label_map}

def get_edge_properties(transform, color_edges, priorities):
    pri = transform.priority if hasattr(transform, 'priority') else 1
    color = trans_to_color[transform.__class__]
    kwargs = {}
    if color_edges:
        kwargs['color'] = color
    if priorities:
        kwargs['label'] = str(pri)
    return kwargs

def add_edges(transform_graph, dot, head, tail, color_edges=True, priorities=False):
    agraph = transform_graph._graph.get(head, None)
    if agraph:
        transform = agraph.get(tail, None)
        if transform:
            dot.edge(head.__name__, tail.__name__,
                     **get_edge_properties(transform, color_edges, priorities))

def to_graphviz_graph(transform_graph, priorities=False,
                      color_edges=True, include_frames=None, label_map=None):

    label_map = label_map or {}
    include_frames = include_frames or transform_graph._graph.keys()

    dot = graphviz.Digraph()

    for a in transform_graph._graph:
        if a not in dot and a in include_frames:
            dot.node(a.__name__, label=label_map.get(a, a.name))
        for b in transform_graph._graph[a]:
            if b not in dot and b in include_frames:
                dot.node(b.__name__, lable=label_map.get(b, b.name))

    for a in transform_graph._graph:
        agraph = transform_graph._graph[a]
        for b in agraph:
            if not ((a in include_frames) and (b in include_frames)):
                continue
            if a is b:
                continue
            add_edges(transform_graph, dot, a, b, color_edges, priorities)
            
    return dot

color_edges=False

dotsunpy = to_graphviz_graph(frame_transform_graph,
                             include_frames=sunpy_label_map.keys(),
                             label_map=label_map, color_edges=color_edges)
dotastropy = to_graphviz_graph(frame_transform_graph,
                               include_frames=astropy_label_map.keys(),
                               label_map=label_map, color_edges=color_edges)

dotastropy.name = "cluster_astropy"
dotastropy.graph_attr['color'] = 'blue'
dotastropy.graph_attr['label'] = 'Frames implemented in Astropy'
dotastropy.node("astropy", label="Other Astropy frames", shape="box3d", style="filled")
dotastropy.edge("astropy", astropy.coordinates.ICRS.__name__, dir="both")
dotastropy.node("geocentric", label="Earth-centered frames", shape="box3d", style="filled")
dotastropy.edge("geocentric", astropy.coordinates.ICRS.__name__, dir="both")

dotsunpy.subgraph(dotastropy)

# Manually add the HCRS <> HGS Transforms
add_edges(transform_graph, dotsunpy,
          astropy.coordinates.builtin_frames.HCRS,
          sunpy.coordinates.frames.HeliographicStonyhurst, color_edges=color_edges)
add_edges(transform_graph, dotsunpy,
          sunpy.coordinates.frames.HeliographicStonyhurst,
          astropy.coordinates.builtin_frames.HCRS, color_edges=color_edges)

dotsunpy.render("sunpy_frames")
