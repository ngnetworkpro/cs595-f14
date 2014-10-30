import connected
import networkx as nx
import betweenness
import csv
import pydot
import argparse


def buildClubGraphs(inFile, n):
  club = []
  #weighted edge data retrieved from http://vlado.fmf.uni-lj.si/pub/networks/data/ucinet/zachary.dat
  #open the csv and put the edge matrix into a list of lists
  with open(inFile) as i:
    reader = csv.reader(i)
    for row in reader:
      club.append(row)
  #create a list of tuples, with edges and weights
  eList = []
  for i in range(0,len(club[0])):
    for j in range(0, len(club[0])):
      if int(club[i][j]) > 0:
        eList.append((i+1,j+1,int(club[i][j])))
  #Use list of edges to create the nx graph		
  K = nx.Graph()
  K.add_weighted_edges_from(eList)
  # Create the .dot file for the whole karate club
  nx.write_dot(K, 'karateclub.dot')
  print 'Original graph has ' + str(K.number_of_edges()) + ' edges\n'
  
  graphs = list(nx.connected_component_subgraphs(K))
  removed = []
  while len(graphs) < n:
    b = nx.edge_betweenness_centrality(K, weight='weight', normalized=False)
    e = (0, 0)
    centrality = 0.0
    for i in b:
      if b[i] > centrality:
        centrality = b[i]
        e = i
      # check
      #b.get(item)
    edges = [e] #put returned tuple into a list, to be used to remove from graph
    #keep track of removed edges and their weighted edge betweenness centrality
    removed.append({'edge': e, 'cent': centrality}) 
    K.remove_edges_from(edges)
    graphs = list(nx.connected_component_subgraphs(K))
	
  print 'Removed edges to build '+str(n)+' subgraphs\n'+'\n'.join(str(r) for r in removed)+'\n'
  #http://stackoverflow.com/questions/12633024/python-concatenate-string-list
  # write the .dot files for the split clubs
  for i in range(0,len(graphs)):
    print 'Nodes in graph ' + str(i+1) + ': ' + ','.join(str(g) for g in sorted(graphs[i].nodes()))
    nx.write_dot(graphs[i], str(n)+'-'+str(i)+'-split.dot')
  
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Build club graph and split into communities')
  parser.add_argument('file', help='input edge matrix file, csv format')
  parser.add_argument('communities', type=int, help='integer, number of communities to split into')
  args = parser.parse_args()
  f = args.file
  n = args.communities
  buildClubGraphs(f, n)