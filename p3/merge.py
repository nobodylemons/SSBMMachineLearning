import os
import pickle
import time
'''
Created on Oct 24, 2017

@author: Robert
'''

def mergeTwo(tree1, tree2):
    if not tree1:
        return tree2
    if not tree2:
        return tree1
    all_locations_tree1 = tree1.all_locations
    for location1 in all_locations_tree1:
        if tree2.__contains__(location1):
            tree2obj = tree2.get(location1)
            tree1obj = tree2.get(location1)
            for i in range(tree1obj.q_arr.__len__()):
                tree1weight = tree1obj.weight_arr[i]
                tree2weight = tree2obj.weight_arr[i]
                weightTotal = tree1weight + tree2weight
                finalq = 0
                if weightTotal is not 0:
                    finalq = (tree1obj.q_arr[i]*tree1weight + tree2obj.q_arr[i]*tree2weight)/weightTotal
                tree2obj.q_arr[i]=finalq
                tree2obj.weight_arr[i]=weightTotal
        else:
            tree2.add(location1,tree1.get(location1))
    return tree2

def mergeAll(locationsTrees):
    retTree = None
    for tree in locationsTrees:
        retTree = mergeTwo(retTree, tree)
    return retTree

# package_loc = os.path.dirname(os.path.realpath(__file__))
# package_loc = os.path.dirname(package_loc)
# package_loc = os.path.dirname(package_loc)

while(True):
    package_loc = "/Users/Robert/Documents/docker/smashparallel"
    paths = []
    i = 0
    
    #get paths of trees
    while os.path.isdir(package_loc+"/"+str(i)):
        tree_path = package_loc+"/"+str(i)+"/tree"
        print(tree_path)
        paths.append(tree_path)
        i = i + 1
    #Pause
    for tree_path in paths:
        os.mkdir(os.path.dirname(tree_path)+"/pause")
    #Nodes confirm they are done writing trees
    i = 0
    for tree_path in paths:
        while not os.path.isdir(os.path.dirname(tree_path)+"/done"):
            print("Waiting for process",str(i)," to write tree")
            time.sleep(.1)
        i = i + 1
    #Read trees
    trees = []
    
    for tree_path in paths:
        trees.append(pickle._load(open(tree_path, 'rb')))
        print("Loaded Tree")
    #merge trees
    tree = mergeAll(locationsTrees=trees)
    print("Merged Trees")
    #Replace original trees with merged trees
    for tree_path in paths:
        pickle.dump(tree, open(tree_path, 'wb'), pickle.HIGHEST_PROTOCOL)
        print("Wrote tree to bots")
    #Unpause, and remove confirmation
    for tree_path in paths:
        print("Removing pause directory")
        os.rmdir(os.path.dirname(tree_path)+"/pause")
        os.rmdir(os.path.dirname(tree_path)+"/done")
    time.sleep(500)
