import streamlit as st
import networkx as nx 
import matplotlib.pyplot as plt
import json
import math

st.set_page_config(page_title="Visualización de Grafos", layout='wide', initial_sidebar_state="collapsed")

def draw_graph(G, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=1, edge_color='k', ax=ax, font_size=4)
    ax.set_title(title)
    return fig
  

def haversine(coord1, coord2):
    R = 6372800  # Radio de la Tierra en metros
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
  

def crearGrafo():
    G = nx.Graph()
    with open('/home/joaquin/Documentos/Tarea Arboles de Expansion/paraderos.geojson', encoding='utf-8') as archivo:
        geo = json.load(archivo)
        i = 0
        for feature in geo['features']:
            stop_id = feature['properties']['stop_id']
    
            coordinates= feature['geometry']['coordinates']
            G.add_node(stop_id, pos=coordinates)
            
    for node1 in G.nodes(data=True):
        for node2 in G.nodes(data=True):
            if node1 != node2:
                coord1 = node1[1]['pos']
                coord2 = node2[1]['pos']
                distance = haversine(coord1, coord2)
                G.add_edge(node1[0], node2[0], weight=distance)



    T_prim = nx.minimum_spanning_tree(G,algorithm="prim")
    T_kruskal = nx.minimum_spanning_tree(G, algorithm='kruskal')
    
    
    return G,T_prim,T_kruskal

def peso_total(G):
    peso = nx.get_edge_attributes(G, 'weight')
    peso_total = sum(peso.values())
    return peso_total

if __name__ == "__main__":
    
    grafoOriginal, grafoPrim, grafoKruskal = crearGrafo()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header('Grafo Original')
        st.write("Peso Grafo Original:", peso_total(grafoOriginal))
        st.pyplot(draw_graph(grafoOriginal, "Grafo Original"))

    with col2:
        st.header('Árbol de Expansión Mínima - Prim')
        st.write("Peso Grafo Prim:", peso_total(grafoPrim))
        st.pyplot(draw_graph(grafoPrim, "Árbol de Expansión Mínima - Prim"))

    with col3:
        st.header('Árbol de Expansión Mínima - Kruskal')
        st.write("Peso Grafo Kruskal:", peso_total(grafoKruskal))
        st.pyplot(draw_graph(grafoKruskal, "Árbol de Expansión Mínima - Kruskal"))
