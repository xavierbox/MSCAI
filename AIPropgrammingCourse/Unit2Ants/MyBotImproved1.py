#!/usr/bin/env python
from ants import *
from Graph import GraphNode
from Graph import Graph, RectGrid
import random
import time
 
class AntNode():
    """
    Holds the information of a node. Such as its location, parent and the 
    direction from parent to this node. 
    
    todo: move all the fields to @property 
    """
    def __init__(self, loc, parent, direction, depth):
        self.loc = loc
        self.parent = parent 
        self.direction = direction
        self.depth = depth 
        
    #for comparison        
    def __eq__(self, other ):
        return True if self.loc  == other.loc else False 
                
    def __neq__(self, other ):
        return True if self.loc  != other.loc else False 
                
    #for debugging 
    def __str__(self):
        return str(self.loc)

    def __repr__(self):
        return str(self.loc)
                
# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:

    def __init__(self):
        # define class level variables, will be remembered between turns
        self.orig_hive = None 
        self.directions = ['n','e','s','w']
        self.grid = None;
        self.water_nodes = set()
        self.priority = 'FOOD'
        self.explored = set();
        self.water = set();
        self.hive_loc = (999,999)
        self.turn = 0 ;       
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        pass
  
    #if there is an ant there, it cant be water and it cant be food either 
    def update_water(self,ants):
        
        #print("Updating water ");
        water = set();
        for loc in ants.my_ants():  
            water.add(  ants.destination(loc, d) for d in self.directions if not ants.passable( ants.destination(loc, d) ) )

        for loc in ants.enemy_ants():  
            water.add(  ants.destination(loc, d) for d in self.directions if not ants.passable( ants.destination(loc, d) ) )
         
        self.water.update( water )
        #print(self.water)
                
    def is_explored( self,loc):
        if loc == self.hive_loc: return True  
        return True if loc in self.explored else False 
        
    def update_explored( self, ants ):
        for loc in ants.my_ants():
            self.explored.add( loc )               
                
    def get_neighbours( self, ants, loc ):
        availale_locs  = [ ]
        available_dirs = [ ]  
        for d in self.directions:
            new_loc = ants.destination(loc, d)
        
            if ants.passable( new_loc ) and new_loc not in self.water :
                availale_locs.append( new_loc )
                available_dirs.append( d )
       
        #[1,2,3,4] 
        return availale_locs,available_dirs
  
  
    def get_ant_food_map( self, ants, busy_ants, busy_locations, max_depth_search = 10 ):
        ant_to_food = {}
        targeted_ants = set();
        
        aux = [] 
        for food_loc in ants.food():
            
            max_depth_search_this_food = max_depth_search
            
            for ant_loc in ants.my_ants():
                #print("Finding path from food", food_loc, " to ant", ant_loc) 
                path, depth  = self.breadth_search( ants,ant_loc,food_loc,max_depth = max_depth_search_this_food );
                path_length = len( path )
                
                if path_length > 0: 
                    aux.append((ant_loc,food_loc,path_length, path[1].direction))
                    max_depth_search_this_food = min( depth, max_depth_search_this_food)
                    #print("adjusting max deopth search ", max_depth_search_this_food)
        
        #list of tuples ant,food,dist sorted by dist between ant and food 
        aux = sorted(  aux, key = lambda t: t[2] )
        
        for tuple_item in aux:
            
            ant_loc   = tuple_item[0];
            
            if ant_loc not in targeted_ants:
                direction = tuple_item[3];
                targeted_ants.add( ant_loc )
                ant_to_food[ant_loc]=direction
                busy_ants.append( ant_loc) 
                
        #ant location : direction to move [s,n,w,e]
        return ant_to_food 
 
    def breadth_search( self, ants, loc1, target_loc, max_depth = 10 ):                
        end_node = None 
        path = []
        expanded_depth = -1;
        
        if loc1 == target_loc: return [ loc1 ], 0  
        
        frontier = [ AntNode(loc = loc1, parent = None, direction = None, depth = 0 ) ]
        explored = set();
                     
        continue_search = True 
        while continue_search:
           
            n1   = frontier[ 0 ]
            #print("Start cycle frontier ",frontier,expanded_depth );
            expanded_depth = n1.depth 
            loc1 = n1.loc
            frontier.pop( 0 )
            if loc1 not in explored:
                explored.add( loc1 )           
     
            neigh_locs,neigh_dirs = self.get_neighbours( ants, loc1 );
            index = -1 
            for loc2 in neigh_locs:
                index = index + 1 
                direction = neigh_dirs[ index ] 
                
                if loc2 not in explored: 
                    n2 = AntNode( loc = loc2 , parent = n1, direction = direction, depth = n1.depth + 1 );
    
                    if target_loc == loc2:
                        end_node = n2
                        #print("Found target ", loc2, " neighbour of ", n1 )
                    else:
                        if n2 not in frontier:
                            frontier.append( n2 )
                   
            #food is too far, forget about it 
            if expanded_depth >= max_depth: 
                continue_search = False
                #print("Reached expanded search",expanded_depth, loc1, target_loc);

            #nowhere else to check 
            if len( frontier ) < 1:  continue_search = False
            
            #found one node that matches the criteria 
            if end_node:
                continue_search = False
                path.append( end_node )
                parent = end_node.parent
                while parent:
                    path.append( parent  )
                    parent = parent.parent
                                    
                path.reverse()
                #print("*****path found *****. Path",path,"Length:", len(path), "depth:",expanded_depth,"->", loc1, target_loc )
        
        return path,  expanded_depth
                                                     
 
    def send_food_seekers( self, ants, busy_ants, busy_locations,max_depth_search = 10 ):
        #print("FoodSeekers: Total ants ", len(ants.my_ants()), " Total food ", len(ants.food()))
        
        if len(ants.food()) < 1: return 0 
        
         
        moving_ants = 0       
        ant_food_map = self.get_ant_food_map( ants, busy_ants, busy_locations,max_depth_search )
         
        for ant_loc in  ant_food_map:
            move_direction = ant_food_map.get( ant_loc )
            new_loc = ants.destination(ant_loc, move_direction)
            
            if new_loc not in busy_locations:
                ants.issue_order((ant_loc, move_direction))
                busy_locations.append( new_loc )
                moving_ants = moving_ants + 1 
                
                if ant_loc not in busy_ants:
                    busy_ants.append( ant_loc )
                print("EATER ant ", ant_loc, " is moving ", move_direction, " to cell ",new_loc )

        return moving_ants

    #not water, not busy and not one to avoid 
    def get_available_walk_directions( self, ants, ant_loc, busy_locations, target_loc = None, try_avoid_loc = None ):  
        available_locs    = []
        target_loc_dist   = {}
        avoid_loc_dist    = {}    
        aux = ['s','n','w','e']
        random.shuffle( aux )
              
        for d in aux:
            
            new_loc = ants.destination(ant_loc, d)
            c1 = ants.passable(new_loc)
            c2 = True#ants.unoccupied(new_loc)
            c3 = True if new_loc not in busy_locations else False 
            c4 = False if try_avoid_loc and new_loc == try_avoid_loc else True;
                              
            if c1 and c2 and c3 and c4: 
                available_locs.append( d )
                if target_loc: 
                    dist = ants.distance( target_loc, new_loc )
                    target_loc_dist[ d ] = dist 
                                   
        if target_loc: 
            w = sorted( target_loc_dist.items(), key = lambda x: x[1])
            available_locs =[ k[0] for k in w ]
                
        return available_locs
      

    def send_explorersOLD( self,ants, busy_ants, busy_locations ):
      
      moving_ants = 0 
      locs = [ ant_loc for ant_loc in ants.my_ants() if ant_loc not in busy_ants ]
      
      for ant_loc in locs:
        dirs = self.get_available_walk_directions( ants, ant_loc, busy_locations, target_loc = None, try_avoid_loc = self.hive_loc )
               
        found_where_to = False; 
        distances = [0,0,0,0]
        index = -1 
        #if there is a nearby not-explored location just walk there and flag it as busy 
        for d in dirs:
            index = index  +  1
            new_loc =  ants.destination(ant_loc, d)
            distances[index] = 1 + ants.distance( new_loc, self.hive_loc )
                        
            #if the cell is unexplored just go there 
            if not self.is_explored( new_loc ):
                    ants.issue_order( (ant_loc, d) )
                    busy_locations.append( new_loc )
                    moving_ants = moving_ants + 1 
                    busy_ants.append( ant_loc )
                    found_where_to = True 
                    break;
                    
        
        #if all the immediate cells are explored go to the one further aways the hive 
        if not found_where_to:       
            #move the explorer 
            winner_dir = dirs[ random.randint(0, len(dirs)-1) ] #dirs [ distances.index( max(distances) )  ] 
            new_loc = ants.destination(ant_loc, winner_dir )
            ants.issue_order( (ant_loc, winner_dir) )
            busy_locations.append( new_loc )
            moving_ants = moving_ants + 1 
            busy_ants.append( ant_loc )
               
                        
      
    def send_explorers( self,ants, busy_ants, busy_locations ):
    
        #for each ant that is not busy 
        hive_loc = ants.my_hills()[0] if len(ants.my_hills()) else (99999,99999)
        
        #move the ants that are not busy to non busy locations as far as possible from the hive. 
        moving_ants = 0 
        frozen_ants = 0;

        #print("Explorers receive busy ants ", busy_ants )
        for ant_loc in  ants.my_ants():
     
            if ant_loc not in busy_ants:
                #print("Checking ant ", ant_loc )
                dirs = self.get_available_walk_directions( ants, ant_loc, busy_locations, target_loc = None, try_avoid_loc = hive_loc )
                   
                if len(dirs) > 0:
                    distances = [0,0,0,0]
                    scores    = [0,0,0,0]
                    explored  =  [True,True,True,True];
                    i = -1; 
                    for d in dirs:
                        i = i + 1 
                        new_loc =  ants.destination(ant_loc, d)
                        
                        distance_to_hive = ants.squared_distance( ant_loc, self.hive_loc )
                        distances[i] = 1 + distance_to_hive
                        was_explored = self.is_explored( new_loc )                
                        
                        if was_explored == False:
                            scores[i]    = scores[i] + 10
                            explored[i] = False
                        
                        else: 
                            explored[i] = True 
                        
                    max_dist_cell = distances.index(max(distances))
                    scores[max_dist_cell] = scores[max_dist_cell] + 5 
                                      
                                      
                    #move the explorer 
                    winner_dir = dirs [ scores.index( max(scores) )  ] 
                    new_loc = ants.destination(ant_loc, winner_dir )
                    ants.issue_order( (ant_loc, winner_dir) )
                    busy_locations.append( new_loc )
                    moving_ants = moving_ants + 1 
                    busy_ants.append( ant_loc )
                    print("Explorer ant loc", ant_loc, " is moving ", winner_dir, " scores ", scores, "dirs = ",dirs , "explored", explored)
                    
                    
                    
                else:
                    frozen_ants = frozen_ants + 1 
            

    def do_turn(self, ants):
    
        self.turn = self.turn   + 1 
        print(30*"-")
        print("-------------------------TURN ", self.turn , "--ants",len(ants.my_ants()),"-----------------------")
        print(30*"-")
    
    
        if ants.my_hills() :
            hive_loc = ants.my_hills()[0] 
            self.hive_loc = ants.my_hills()[0] 

       
        self.update_explored( ants )
        self.update_water( ants )
    
        #first thing we will do it to try to get something from the environment.
        #check all the positions that each ant can move to and flag unknown obstacles. 
        #this affects tremendously the search for food 
        
        busy_ants = [] 
        busy_locations = [] 
        #in this version the only thing we do is to search for food but we prioritize the closer foods.
        #this code returns the food index sorted by closeness to any ant, and the ant it is closer to it. 
        #will look like { 0: 3, 1: 11, 3: 4 ...} where key is food index  and value is ant index
        
            
        self.send_food_seekers( ants, busy_ants, busy_locations,max_depth_search = 10 )
                       
        ##free_ants = len(ants.my_ants()) - len(busy_ants)
        self.send_explorers( ants, busy_ants, busy_locations )
            
      
    
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
