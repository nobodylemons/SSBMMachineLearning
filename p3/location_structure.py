'''
Created on Sep 28, 2017

@author: Robert
'''

class LocationStruct(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.first_map = {}
        self.size = 0;
        self.all_locations = []
        
    def add(self, input_data, obj):
        self.add_recurs(input_data.copy(), self.first_map, obj)
        self.all_locations.append(input_data)
    
    def add_recurs(self, input_data, str_map, obj):
        dat = input_data.pop(0)
        if input_data.__len__()>0:
            if not str_map.__contains__(dat):
                str_map[dat] = {}
            self.add_recurs(input_data, str_map[dat], obj)
        else:
            str_map[dat] = obj
            self.size = self.size+1
                
    def get(self, input_data):
        temp_map = self.first_map
        for dat in input_data:
            temp_map = temp_map[dat]
        return temp_map
    
    def __contains__(self, input_data):
        temp_map = self.first_map
        for dat in input_data:
            if temp_map.__contains__(dat):
                temp_map = temp_map[dat]
            else:
                return False
        return True
            
            
            
            