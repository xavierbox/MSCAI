
#################
#for python 2.7 #
#################


#only one connection between nodes (not the bridges problem yet) 
class GraphNode: 
    
    counter = 0; #for debugging purposes, not really needed
    
    def __init__( self, connections = None, data = None  ):
        self.connections = set ( connections ) if connections else set()
        self._id = GraphNode.counter 
        self.data = data; 
        GraphNode.counter = GraphNode.counter + 1
        
    def __str__(self):
        s1 =  "Graph node id: " + str( self.id ) + " data: " + str(self.data)# + ".\nLinks: " + str(self.connections);  
        s2 =  ""#"Connections: " + str( [ {n.id,n.data} for n in self.connections] )
        return s1 + "\n" + s2 
    
    def __repr__(self):
        s1 =  "Graph node id: " + str( self.id ) + " data: " + str(self.data)# + ".\nLinks: " + str(self.connections);  
        s2 =  ""#"Connections: " + str( [ {n.id,n.data} for n in self.connections] )
        return s1 + "\n" + s2 
    
    def add_connection( self, node ):
        self.connections.add ( node )
        
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        
    #def add_connection( self, graph_node ):
    #    child.parent = self
    #    self.children.append( child )

class Graph: 
  
    def __init__( self ):
        self.nodes = []; #set(); 
        
    def __len__( self ): 
        return len( self.nodes )
    
    def add_node( self, node ):
        #self.nodes.add( node )
        if node not in self.nodes: self.nodes.append( node )
        
    
    def add_nodes( self, nodes ):
        for node in nodes:
            self.add_node( node )
        
    def add_connection( self, node1, node2 ):
        node1.add_connection( node2 )
        node2.add_connection( node1 )
        
    def create_periodic_rect_grid( self, hcols, vrows ):
        cells = hcols * vrows;

        items = []
        for cy in range( vrows ):
            for cx in range (hcols ):
                cell = cx  + hcols * cy 
                #print(f"cell {cell} = ({cx},{cy})")

                grid_node = GraphNode( connections = None, data =  None )#f"cell:{cell}, indices:({cx},{cy})")
                items.append( grid_node )
                #print(grid_node.data)

        #ADD THE NODES
        self.add_nodes( items )     
        #print(f"Created a graph with {len( g1 )} nodes ");

        #now lets do the connections with periodic boundary conditions 
        offsetx = [1, 0,-1,  0]
        offsety = [0, 1, 0, -1]
        offset_cells = len( offsetx )
        for cy in range( vrows ):
            for cx in range ( hcols ):

                cell1 = cx  + cy  * hcols
                #print("doing cell1 ", cx, cy )
                for offset in range( offset_cells):
                    cx2 = cx + offsetx[ offset ]
                    cy2 = cy + offsety[ offset ]


                    #print("checking neighbour ", cx2, cy2 ) 
                    #periodic boundaries 
                    if cx2 >= hcols: cx2 = 0;
                    if cx2 < 0 : cx2 = hcols -1;

                    if cy2 >= vrows: cy2 = 0;
                    if cy2 < 0: cy2 = vrows -1;

                    #print("which becomes ", cx2, cy2 ) 

                    cell2 = cx2 + cy2 * hcols

                    #NOW WE ADD THE CONNECTIONS
                    node1 = items[ cell1 ]
                    node2 = items[ cell2 ]
                    self.add_connection( node1, node2 )
                #print("--------------------")

        #debugging 
        #print("node 0 ", items[0], "links\n",items[0].connections)         
        #print("node 2 ", items[2], "links\n",items[2].connections)         

        return items 


    def first_search_path( self, node1, node2, max_depth = 99999999, sort_function = None  ):
        
        #def do_not_sort_connections( node1, node2, links ):
        #    return links 
        
        #if sort_function == None:
        #    sort_connections = do_not_sort_connections
        #else:
        #    sort_connections = sort_function
        
        io = 0 
        
        if node1 == node2:
            return [node1, node2 ]
        
        if len(node1.connections)<1:
            return []
        
        if len(node2.connections)<1:
            return []
        
        frontier =  [node1]
        explored = set();
        path = []        
        end_node = None  
        retrace = {}
        depth = { node1: 0 }
        max_expanded_depth = -99999999 
        keep_searching = True  
        while keep_searching: 
         
            n1 = frontier[ io ]
            frontier.remove( n1 )
            explored.add( n1 )
            
            connections = n1.connections#sort_connections( node1, node2, n1.connections )
            
            for node in connections:
                if node not in frontier and node not in explored:  
                                      
                    depth[ node ] = depth[ n1 ] + 1 
                    retrace[node] = n1
                    if max_expanded_depth <depth[ node ]:  max_expanded_depth  = depth[ node ]
                    
                    if node == node2:
                        end_node = node
                        keep_searching = False;
                        break; 
                        
                    else:
                        frontier.append( node ) 
                        
            #print("Updated frontier nodes ", [x.data for x in frontier])
            #print("retrace ",[x.data for x in retrace])
            continue_condition = len(frontier) > 0  and not end_node and max_expanded_depth < max_depth#  and max([ v for k,v in depth.items() ]) < max_depth
            keep_searching = True if continue_condition else False;
                        
        if end_node: #there is a path, lets build it 
            path.append( end_node )
            #print("Appended ", end_node.data)
            
            parent = retrace.get(end_node)         
            while parent is not node1: 
                end_node= parent 
                path.append( end_node )
                parent = retrace.get(end_node)
                
            path.append( node1 )           
            path.reverse();
            
        return path;

class RectGrid( Graph ): 

    def __init__( self, hcols, vrows ):
        Graph.__init__( self );
        self.nodes = [] ; 
        self.rows = vrows
        self.cols = hcols 
        self.create_periodic_rect_grid( hcols, vrows )
        
    @property
    def node_list(self):
        return self.nodes
    
    def get_node_from_indices( self, hcol, vrow ):
        cell =  hcol + vrow * self.cols
        return self.nodes[ cell ]
    
    def get_node( self, index ):
        vrow  =  int( 1.0*index/self.cols ) 
        hcol  =  index - vrow * self.cols
        return self.get_node_from_indices( hcol, vrow )
        
        
        