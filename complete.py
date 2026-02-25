import networkx as nx
import matplotlib.pyplot as plt

def create_complete_graph():
    try:
        n = int(input("Enter the number of vertices (greater than 3): "))
        
        if n <= 3:
            print("Number of vertices must be greater than 3.")
            return
        G = nx.complete_graph(n)
        print(f"\nComplete graph with {n} vertices created.")
        print(f"Number of edges: {G.number_of_edges()}")
        
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=800, font_weight='bold')
        plt.title(f"Complete Graph K{n}")
        plt.show()
        
    except ValueError:
        print("Please enter a valid integer.")

create_complete_graph()