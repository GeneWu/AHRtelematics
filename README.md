# Telematics data analysis

1. feature.py is used to generate features for each trip
2. Vertex is an object that store the generated features
3. Edge is an object grouping similar vertices
4. graph is used to represent the telematics dataset


## Rule

Currently rules are predefined and hard coded.

The rule name and output of the rule define a type of edge.

To create a new rule:
>1. create a class and inherit the Rule class
>2. define the rule name and instanitate the edge variables
>3. overwrite the classify method, which return name + "_" + output

##Optimization

Now it take long long time to construct the graph,
several ways to speed it up.

1. After the feature set has been fixed, we can create npy file to store the computed features. And to construct new graph, just need to load the npy file which is way more faster than re-compute it.
2. To use less memory, we can build a data structure (hashtable) using vertex id. And to store the graph,
we dont need to store the whole object but only the vertex id and look it up in the hashtable.
