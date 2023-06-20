import streamlit as st
import matplotlib.pyplot as plt
from network import Network
import networkx as nx

margins_css = """
    <style>
        .main > div {
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
"""
st.markdown(margins_css, unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("""
    # Problem Maksymalnego przepływu
    ## Teoria
    ### Ford-Fulkerson
    Metoda Forda-Fulkersona jest stosowana do znajdowania maksymalnego przepływu w sieci przepływowej.
    Stanowi podstawę wielu algorytmów, między innymi algorytmu Edmondsa-Karpa czy algorytmu Dynica.
    Zasadę jej działania można streścić w następujący sposób: Należy zwiększać przepływ wzdłuż dowolnej ścieżki ze źródła do ujścia,
    dopóki jest to możliwe.
    Dla dowolnej sieci przepływowej
    $G=(V,E)$ o źródle $s$ i ujściu $t$, w której dowolna krawędź $(u,v)$ należąca do zbioru $E$
    ma przepustowość $c(u,v)$ oraz przepływ $f$ definiuje się następujące pojęcia:
    #### Sieć rezydualna
    Siecią rezydualną dla sieci przepływowej $G$ nazywamy sieć $G_f = (V,E_f)$, gdzie $E_f$ jest zdefiniowane następująco:
    $$ 
    E_f =  \{(u,v) \in V \\times V : c_f (u,v) > 0 \}
    $$
    gdzie $c_f(u,v)$ oznacza tzw. przepustowość rezydualną dla krawędzi $(u,v)$.
    Ta natomiast jest dana wzorem: 
    $$
    c_f(u,v) = c(u,v) - f(u,v)
    $$
    Krawędzie należące do $E_f$ nazywa się krawędziami rezydualnymi.
    Bardziej intuicyjnie, przepustowość rezydualna dla pewnej krawędzi $(u,v)$ oznacza, o ile można zwiększyć przepływ przez nią, tak jednak, aby nie przekroczył on jej przepustowości.
    Do sieci rezydualnej natomiast należą te krawędzie, przez które przepływ można zwiększyć.
    #### Ścieżka powiększająca
    Ścieżką powiększającą dla sieci $G$ nazywamy dowolną ścieżkę z $s$ do $t$ w sieci rezydualnej dla $G$.
    Przepustowość rezydualną dowolnej ścieżki powiększającej $p$ dla sieci $G$ określamy wzorem:
    $$
    c_f(p) = \min \{c_f(y,v) : (u,v) \in p\}
    $$
    Jest to wartość, o jaką maksymalnie można zwiększyć przepływ przez wszystkie krawędzie należące do ścieżki $p$.
    
    ### Busacker-Gowen
    Algorytm Busackera-Gowena, znany również jako algorytm przepływu minimalnego w grafach, to popularny algorytm używany do rozwiązywania problemu przepływu minimalnego w grafach skierowanych.
    Problem przepływu minimalnego polega na znalezieniu najmniejszej możliwej wartości przepływu w sieci, gdzie przepływ reprezentuje ilość jednostek, które mogą przepłynąć przez poszczególne krawędzie. 
    Algorytm Busackera-Gowena służy do rozwiązania tego problemu, a konkretnie do znalezienia przepływu minimalnego w sieci o skierowanych krawędziach.
    Algorytm Busackera-Gowena oparty jest na koncepcji przepływu blokującego. Polega na iteracyjnym wyszukiwaniu ścieżek blokujących w sieci, czyli takich ścieżek, które ograniczają przepływ przez sieć.
    Po znalezieniu ścieżki blokującej, algorytm zwiększa przepływ na tej ścieżce, aż do momentu, gdy nie będzie możliwe znalezienie kolejnej ścieżki blokującej. 
    To ostatecznie prowadzi do znalezienia przepływu minimalnego w sieci.
    Algorytm Busackera-Gowena jest jednym z popularnych algorytmów używanych w teorii grafów i optymalizacji. Ma zastosowanie w różnych dziedzinach, takich jak transport, telekomunikacja czy planowanie tras.
    """)
st.markdown("""
    # Implementacja
""")

gen = st.button("Generuj sieć")

if gen:
    net = Network()
    st.header("Ford-Fulkerson")
    col1, col2= st.columns(2)
    with col1:
        st.header("Przed:")
        st.pyplot(fig=net.draw_graph(net.graph, draw_weights=True))
    with col2:
        st.header("Po:")
        st.pyplot(fig=net.draw_graph(net.graph_ff, draw_weights=True))
        st.text(f"Maksymalny przepływ: {net.max_flow}")
    
    st.header("Busacker-Gowen")
    col1, col2= st.columns(2)
    with col1:
        st.header("Przed:")
        st.pyplot(fig=net.draw_graph(net.graph))
    with col2:
        st.header("Po:")
        st.pyplot(fig=net.draw_graph(net.graph_bg))
        st.text(f"Minimalny koszt: {net.cost_bg}")
        st.text(f"Maksymalny przepływ: {net.flow_bg}")
    
    st.header("Porównanie")
    col1, col2= st.columns(2)
    with col1:
        st.header("Ford Fulkerson")
        st.pyplot(fig=net.draw_graph(net.graph_ff, draw_weights=True))
    with col2:
        st.header("Busacker Gowen")
        st.pyplot(fig=net.draw_graph(net.graph_bg))