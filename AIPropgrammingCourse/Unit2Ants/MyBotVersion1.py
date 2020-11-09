#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        self.orig_hive = None 
        self.directions = ['n','e','s','w']
                
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        #self.get_original_hive( ants )
        pass 

    def get_original_hive( self, ants ):  
        #pass 
        if self.orig_hive == None: 
            self.orig_hive = list(ants.my_hills())[0]
            print("updated hive to ",  self.orig_hive )
                  
 
 
 
    
    
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):

        dirs = list( self.directions )    
        orders = {}    
        def check_move_direction(loc, direction ):
            new_loc = ants.destination(loc, direction)
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                return True, new_loc
            return False, new_loc 
        
        for food_loc in ants.food():
            print("food location ", food_loc )
     
        #print("\n\nthis is my bot\n\n",  ants.ant_list );
        # loop through all my ants and try to give them orders
        # the ant_loc is an ant location tuple in (row, col) form
  
        for loc in ants.my_ants():
        
            # try all directions in random order (uninformed)         
            random.shuffle(dirs)
            found_dir = False;
            for direction in dirs:
                valid, new_loc = check_move_direction(loc, direction)
                if valid:
                    ants.issue_order((loc, direction))
                    orders[new_loc] = loc
                    found_dir = True 
                    print("new loc ", new_loc )
                    break;
                    
            print("and found diretion ", direction ); 
            
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
