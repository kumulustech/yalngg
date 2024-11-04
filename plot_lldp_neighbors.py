import json
import networkx as nx
import matplotlib.pyplot as plt

# Load LLDP data from JSON file
def load_lldp_data(json_file):
    with open(json_file, 'r') as infile:
        return json.load(infile)

# Create a graph from LLDP data
def create_graph(lldp_data):
    G = nx.MultiGraph()  # Use MultiGraph to handle multiple edges between nodes
    
    for hostname, data in lldp_data.items():
        interfaces = data.get("openconfig-lldp:interface", [])
        
        for interface in interfaces:
            local_port = interface.get("name")
            neighbors = interface.get("neighbors", {}).get("neighbor", [])
            
            for neighbor in neighbors:
                neighbor_name = neighbor["state"]["system-name"]
                neighbor_port = neighbor["state"]["port-id"]
                
                # Add nodes and edges to the graph with port information
                G.add_node(hostname)
                G.add_node(neighbor_name)
                G.add_edge(hostname, neighbor_name, local_port=local_port, neighbor_port=neighbor_port)
    
    return G

# Visualize the graph
def visualize_graph(G, output_file='network_graph.png'):
    plt.figure(figsize=(200, 200))  # Increase the figure size
    pos = nx.spring_layout(G, seed=42, k=0.3)  # Adjust k for better spacing
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=12, font_weight="bold")
    
    # Draw edge labels with port information
    edge_labels = {(u, v): f"{d['local_port']} <-> {d['neighbor_port']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.title("Network Connectivity Graph")
    plt.savefig(output_file)
    plt.show()

# Save the graph as GraphML
def save_graphml(G, output_file='network_graph.graphml'):
    nx.write_graphml(G, output_file)

def main():
    json_file = 'lldp_data.json'
    lldp_data = load_lldp_data(json_file)
    graph = create_graph(lldp_data)
    visualize_graph(graph, output_file='network_graph.png')
    save_graphml(graph, output_file='network_graph.graphml')

if __name__ == "__main__":
    main()
