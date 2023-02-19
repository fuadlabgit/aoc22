
import numpy as np 


class RollingArray:
    # a rolling array which deletes parts of itself after a certain height 

    def __init__(self):
        """
        very long array 

        [ . . . . . .  .]
        [ . . . . . .  .]
        [ . . . . . .  .]
        [ . . . . . .  .]
        [ . . . . . .  .]
        [ . . . . . .  .]
        [ . . . . . .  .]
        [ . . . . . .  .]
        [ # # # # # # # ] < y + y_offset

              ^
              x
        
        [ . . . . . . . .]
        """

        self.n_max = 20000
        self.data = np.array(7,self.n_max)
        self.offset = 0

    def get_index(self,i,j):

    
    def roll(self):
        # 
        

    
    

