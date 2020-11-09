#!/usr/bin/env python
from ants import *
from Graph import GraphNode
from Graph import Graph, RectGrid
#import random
import time
 
 
 

            
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
        
        self.turn = 0 ;
        
    

                
            
    
                
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        #self.get_original_hive( ants )
        self.grid = RectGrid(3,3)#ants.cols, ants.rows);
        
        #grid = self.grid
        #for hcol in range( grid.cols ):
        #    for vrow in range( grid.rows ):
        #        cell_index = hcol + vrow * grid.cols
        #        this_node = grid.get_node_from_indices( hcol, vrow )
        #        #this_node.data = str(cell_index) + "("+str(hcol)+","+str(vrow)+")";
        

    def get_original_hive( self, ants ):  
        #pass 
        if self.orig_hive == None: 
            self.orig_hive = list(ants.my_hills())[0]
            print("updated hive to ",  self.orig_hive )
                  
 
    def update_water(self,ants):
        for loc in ants.my_ants():
            if not ants.passable( loc ):
                self.water.add( loc )
             
            
 
    def get_food_ant_map( self, ants ):    
        grid = self.grid 
        #in this version the only thing we do is to search for food.
        #for each visible food, there must be one ant that is the closest to the food       
        
        #we will try to attack every food item if we have enough ants but will prioritize the closer foods.
        #this code simple finds the closest foods and sort them by food index 
        
        #food_list = [ ants.food() ]
        
        #print("total foods ", len( ants.food())," total ants ", len(ants.my_ants()))
        food_ant_dict = {}
        food_index = -1; 
        for food_loc in ants.food(): #this is a location 
            food_index = food_index + 1 
            #food_ant_dict[ food_index ] = list()
            food_ant_dict[ food_loc ] = list()
            
            #####food_node = grid.get_node_from_indices( food_loc[1], food_loc[0] )
            
            min_path_length = None  #for this food 
            ant_index = -1 
            for ant_loc in ants.my_ants(): #this is a location 
                and_index = ant_index + 1 
                vrow = ant_loc[0]
                hcol = ant_loc[1]
                ######ant_node = grid.get_node_from_indices( hcol, vrow )
                
                #slow way 
                #path_ant_food = grid.first_search_path( ant_node, food_node, max_depth = 20, sort_function = None  )
                #path_length = len( path_ant_food )
                #quick_way 
                path_length = ants.distance(ant_loc, food_loc)
            
                #it may be the case that the food is not reachable within the search distance 
                #it may also happen that more than one food has the same closest ant 
                #more ants thant food, more food than ants 
                if not min_path_length or   min_path_length > path_length: 
                    min_path_length = path_length
                    #closest_ant = ant_loc 
    
                food_ant_dict[ food_loc ].append( min_path_length )
                #print("This food: closest ant ", closest_ant," path length ", min_path_length )
 
 
        food_ant_dict =   sorted(food_ant_dict.items(), key=lambda pair: min(pair[1]) )
        xx = { item[0]:item[1] for item in food_ant_dict}
        food_ant_dict = xx;
        
        #for each food, get its closest non-asigned ant 
        asigned_ants = set()
        for food_loc in food_ant_dict:
            ant_list = food_ant_dict.get( food_loc )
            
            #some other food took already some ants. 
            aux = 0
            for asigned in asigned_ants:
                ant_list[ asigned ] = 99999999
                aux = aux + 1 
                
            if aux < len(ant_list) and min(ant_list) < 99999999:
                #from whatever is left, pick the closest ant. 
                closest_ant_index = ant_list.index(min(ant_list))
                asigned_ants.add( closest_ant_index )
                food_ant_dict[ food_loc ] = [closest_ant_index]
            else: 
                food_ant_dict[ food_loc ] = []               
              
              
        #print("food searching resulted in ", food_ant_dict ) 
        food_ant_dict = { k:v[0] for k,v in food_ant_dict.items() if len(v)>0}            
     
        #print("Returning ", food_ant_dict ) 
        return food_ant_dict

    def walk_ant( self, ants, ant_loc, busy_locations):
        pass
    

    def get_available_walk_directions( self, ants, ant_loc, busy_locations, target_loc = None, try_avoid_loc = None ):
    
        available_locs    = []
        target_loc_dist   = {}
        avoid_loc_dist    = {}
        
        aux = ['s','n','w','e']
        random.shuffle( aux )
        
        
        for d in aux:
            
            new_loc = ants.destination(ant_loc, d)

            c1 = ants.passable(new_loc)
            c2 = ants.unoccupied(new_loc)
            c3 = True if new_loc not in busy_locations else False 
            c4 = True #False if try_avoid_loc and new_loc == try_avoid_loc else True;
                      
           
            if c1 and c2 and c3 and c4: 
                available_locs.append( d )
                if target_loc: 
                    dist = ants.distance( target_loc, new_loc )
                    target_loc_dist[ d ] = dist 
                    
                    
        if target_loc: 
            w = sorted( target_loc_dist.items(), key = lambda x: x[1])
            available_locs =[ k[0] for k in w ]
            
        # The locations are now sorted based on the closeness to the target food.
        # Yet, lets do a second pass and eliminate those that would end up on top of locs to avoid         
            
            
        return available_locs








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
  
  
    def breadth_search( self, ants, loc1, target_loc, max_depth = 50 ): 
        
        class AntNode():
            def __init__(self, loc, parent, direction):
                self.loc = loc
                self.parent = parent 
                self.direction = direction
                self.depth = 0
                
            def __str__(self):
                return str(self.loc)

            def __repr__(self):
                return str(self.loc)
                
        end_node = None 
        path = []
        expanded_depth = -1;
        if loc1 == target_loc: return [ loc1 ] 
        
        frontier = [ AntNode(loc = loc1, parent = None, direction = None ) ]
        explored = set();
              
        #print("Finding path from ant ", loc1, " to ", target_loc ) 
        
        continue_search = True
        while continue_search:
            expanded_depth = expanded_depth +  1 
            #print("Start cycke frontier ",expanded_depth );
            
            
            n1   = frontier[ 0 ]
            #print("parent in this cicle ", n1.loc ) 
            loc1 = n1.loc
            frontier.pop( 0 )
      
            #new_loc = ants.destination(loc, d)

            index = -1 
            neigh_locs,neigh_dirs = self.get_neighbours( ants, loc1 );
            aux = [] 
            for loc2 in neigh_locs:
                
                index = index + 1 
                direction = neigh_dirs[ index ] 
                
                if loc2 not in explored:
                    n2 = AntNode( loc = loc2 , parent = n1, direction = direction );
                    #print("Added n2 ", n2.loc," with parent ", n2.parent, "n1 = ",n1);
                    
                    if target_loc == loc2:
                        end_node = n2
                    else:
                        #aux.append( n2 )
                        frontier.append( n2 )
            #aux.reverse();
            #for i in aux: frontier.insert( 0, i )
            #print("End cycke frontier ", frontier);
            
            
      
            
            if expanded_depth >= max_depth: 
                continue_search = False
                #print("Reached expanded search",expanded_depth, loc1, target_loc);
                
            if len( frontier ) < 1:  continue_search = False
            
            if end_node:
                
                #print("**************node found***************");
                continue_search = False
                path.append( end_node )
                parent = end_node.parent
                while parent:
                    path.append( parent  )
                    parent = parent.parent
                    
                    
                path.reverse()
                #print("*****path found ******", len(path),loc1, target_loc )
        
        return path 
                    
                    
    def send_food_seekers( self, ants, busy_ants, busy_locations ):
        #print("FoodSeekers: Total ants ", len(ants.my_ants()), " Total food ", len(ants.food()))
        
        if len(ants.food()) < 1: return 0 
        
        moving_ants = 0 
        
        ant_food_map = self.get_ant_food_map( ants, busy_ants, busy_locations )
         
         
        #print("ant  food map ",  ant_food_map )
         
        for ant_loc in  ant_food_map:
            move_direction = ant_food_map.get( ant_loc )
            new_loc = ants.destination(ant_loc, move_direction)
            
            if new_loc not in busy_locations:
                ants.issue_order((ant_loc, move_direction))
                busy_locations.append( new_loc )
                moving_ants = moving_ants + 1 
                busy_ants.append( ant_loc )
                print("EATER ant ", ant_loc, " is moving ", move_direction, " to cell ",new_loc )
                    
                #print("ant ", ant_loc, " moving in direction ", move_direction, " to cell ",new_loc ) 
            
        
        return moving_ants
        
    def get_ant_food_map( self, ants, busy_ants, busy_locations ):
        ant_to_food = {}
        targeted_foods = set();
     
        for ant_loc in ants.my_ants():
 
            #print("--checking ant ",ant_loc )
            closest_dist = 9999999999;
            closest_food = None
            closest_path = None 
            food_found = False;
            for food_loc in ants.food():
             
                
                if food_loc not in targeted_foods:
                    there_is_food = True
                    #print("-----checking food", food_loc)
                    #d = ants.distance( ant_loc, food_loc )
                    path = self.breadth_search( ants,ant_loc, food_loc );
                    path_length = len( path )
                        
                    if len( path ) > 0: 
                        food_found = True 
                        #print("-----path length returned ", path_length )
                    
                        if path_length <= closest_dist : 
                            #print("path returned by the search ", path )
                            #print("It is the closest path", path, path_length)
                            #print("food",food_loc, " path legnth ", len(path), "path",path)
                            closest_dist = path_length
                            closest_food = food_loc 
                            closest_path = path 
                            
                        else: 
                            pass#print("food",food_loc, " path legnth ", len(path))
            
                 
            if food_found:
                targeted_foods.add( closest_food )
                
                #print("------Found path ", closest_path," for ant ", ant_loc)
                #print("Start+0 path ", closest_path[0].loc,"parent",closest_path[0].parent, "dir ",closest_path[0].direction)
                #print("Start+1 path ", closest_path[1].loc,"parent",closest_path[1].parent, "dir ",closest_path[1].direction)
                #print("Start+2 path ", closest_path[2].loc,"parent",closest_path[2].parent, "dir ",closest_path[2].direction)
                
                
                ant_to_food[ ant_loc ] = closest_path[1].direction
                
           

             
        return ant_to_food
                    
                

    def send_explorers( self,ants, busy_ants, busy_locations ):
        #for each ant that is not busy 
        #then get a list of the ant's available cells to walk to
        #pick if any the furthest from the hive that is not already explored and it is not water and nobody is going there. 
        #print("sending explorers....");
        hive_loc = ants.my_hills()[0] if len(ants.my_hills()) else (99999,99999)
        
        #move the ants that are not busy to non busy locations as far as possible from the hive. 
        moving_ants = 0 
        frozen_ants = 0;
        ant_index = -1;
        for ant_loc in  ants.my_ants():
            ant_index = ant_index + 1 
            if ant_index not in busy_ants:
                dirs = self.get_available_walk_directions( ants, ant_loc, busy_locations, target_loc = None, try_avoid_loc = hive_loc )
                #print("ant index is not busy ", ant_index, "getting its available directions, dirs = ", dirs )
                # 
                 
                if len(dirs) > 0:
                    distances = [0,0,0,0]
                    scores    = [0,0,0,0]
                    explored  =  [0,0,0,0];
                    i = -1; 
                    for d in dirs:
                        i = i + 1 
                        new_loc =  ants.destination(ant_loc, d)
                        
                        #distances[i] = 1.0 + ants.distance( ant_loc, hive_loc )
                        
                        was_explored = self.is_explored( new_loc ) 
                        
                        if was_explored == True:
                            scores[i]    = scores[i] -1
                            explored[i] = True
                        else:
                            scores[i]    = scores[i] +1
                            explored[i] = False
                        
                        scores[i]    = scores[i] + (-1 if new_loc==hive_loc else 1) 
                        
                  
                    #aux = max(distances)
                    #print("aux=",aux)
                      
                    #distances = [ int( d/aux ) for d in distances ] 
                    #for i in range(len(distances)): 
                    #    scores[i] = scores[i] + distances[i]
                    #i = distances.index(max(distances))
                    #scores[i] = scores[i] + 1 
                    
                    winner_dir = dirs [ scores.index( max(scores) )  ] 
                    new_loc = ants.destination(ant_loc, winner_dir )
                    ants.issue_order( (ant_loc, winner_dir) )
                    busy_locations.append( new_loc )
                    moving_ants = moving_ants + 1 
                    busy_ants.append( ant_loc )
                    
                    print("Explorer ant ", ant_index, "loc", ant_loc, " is moving ", winner_dir, " scores ", scores, "dirs = ",dirs , "explored", explored)
                    
                else:
                    frozen_ants = frozen_ants + 1 
                    
    def is_explored( self,loc):
        return True if loc in self.explored else False 
        
    def update_explored( self, ants ):
        for loc in ants.my_ants():
            self.explored.add( loc )


    def do_turn(self, ants):
    
        self.turn = self.turn   + 1 
        print("-------------------------TURN ", self.turn , "--ants",len(ants.my_ants()),"-----------------------")
    
        if ants.my_hills() :
            hive_loc = ants.my_hills()[0] 
            self.water.add( hive_loc ) 
            #print("initialized hive pos ",hive_loc  )
       
       
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
        
        if self.priority == 'FOOD':
            
            self.send_food_seekers( ants, busy_ants, busy_locations )
            
            
            ##free_ants = len(ants.my_ants()) - len(busy_ants)
            ##if free_ants:
            self.send_explorers( ants, busy_ants, busy_locations )
            
            #free_ants = len(ants.my_ants()) - len(busy_ants)
            #if free_ants:
            #    self.send_killers( ants, busy_ants, busy_locations )
        
        elif self.priority == 'KILL':
            self.send_killers( ants, busy_ants, busy_locations )
            self.send_explorers( ants, busy_ants, busy_locations )
            self.send_food_seekers( ants, busy_ants, busy_locations )
            
        else: 
            self.send_explorers( ants, busy_ants, busy_locations )
        
        
        
        #food_ant_dict = self.get_food_ant_map( ants )
        #print("food_ant_dict = ", food_ant_dict)
        
        
        #priority: 1-food 2-unseen 3-away from hive. All under the condition that loc is not selected 
        
        
        #all the ants asigned for food, go for the food if possible, the rest do a random walk.
        #if in the search for food, an ant cant for any reason, then random walk. 
        
        #direction = 'n'
        #for loc in ants.my_ants():
        #    ants.issue_order((loc, direction))
            #orders[new_loc] = loc
      
        
            
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn_old(self, ants):
    
        #print("grid rows = ", self.grid.rows, " grid cols ", self.grid.cols )
    
        #self.directions = ['n','s','e','w']
        dirs = list( self.directions )    
        orders = {}    
        def check_move_direction(loc, direction ):
            new_loc = ants.destination(loc, direction)
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                return True, new_loc
            return False, new_loc 
        
        #for food_loc in ants.food():
        #    print("food location ", food_loc )
     
        #print("\n\nthis is my bot\n\n",  ants.ant_list );
        # loop through all my ants and try to give them orders
        # the ant_loc is an ant location tuple in (row, col) form
  
        for loc in ants.my_ants():
        
            #print("and loc ", loc )
            # try all directions in random order (uninformed)         
            random.shuffle(dirs)
            found_dir = False;
            for direction in dirs:
                valid, new_loc = check_move_direction(loc, direction)
                if valid:
                    ants.issue_order((loc, direction))
                    orders[new_loc] = loc
                    found_dir = True 
                    #print("new loc ", new_loc )
                    break;
                    
            #print("and found diretion ", direction ); 
            
                # the destination method will wrap around the map properly
                # and give us a new (row, col) tuple
                ##new_loc = ants.destination(ant_loc, direction)
                # passable returns true if the location is land
                ##if (ants.passable(new_loc)):
                ##    # an order is the location of a current ant and a direction
                ##    ants.issue_order((ant_loc, direction))
                ##    # stop now, don't give 1 ant multiple orders
                ##    break
            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break
            
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
