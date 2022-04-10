''' All data scrapping and preprocessing has been done separately and kept 
under a private repository which won't be made public. To give graders an idea
of the work done in that notebook, I am including one of the functions that
preprocesses a listing location and produces a usable location tree. I will not 
be adding the rest. Results can be appreciated by looking at the sample raw_marina.csv file, which 
is itself the product of a lot of pre-processing, and specifically at the column ´location´ and 
how that column is transformed into subsequent columns [sub_location_1,sub_location_2,sub_location_3]'''

# function to fix formatting in location column and split into sublocations
location = merged_df.location.iloc[1]
def fix_location(location):
    '''
    Transform a location string into its corresponding location tree, made
    of the three components of a location.
    
    INPUT
    location: str: Marina Quay North 3.8 /56 Reviews Dubai - Dubai Marina - Marina Quays
    OUTPUT
    list: ['marina quay north', 'marina quays', 'dubai marina']

    '''
    # find index of Reviews, to be removed
    idx = location.find('Reviews')
    # means reviews not found, then remove Dubai
    if idx == -1: 
        idx = location.find('Dubai')
        back_shift = 1
        forward_shift = len('Dubai')
    else: # Reviews was found
        back_shift = 9
        forward_shift = len('Reviews Dubai')
    # slicing indeces
    start_slice = idx - back_shift
    end_slice = idx + forward_shift
    # slice the string to remove unwanted text
    location_amend = location[:start_slice] + location[end_slice:]
    # check number of sublocations by counting occurences of '-'
    if location_amend.count('-') == 2:
        unordered_tokens = location_amend.split('-')
        ordering = [1, 2, 0]
        tokens = [unordered_tokens[i].lower().strip() for i in ordering]
    elif location_amend.count('-') == 1:
        unordered_tokens = location_amend.split('-') + ['']
        ordering = [1, 0, 2]
        tokens = [unordered_tokens[i].lower().strip() for i in ordering]
    else:
        tokens = [location_amend.lower().strip()] + ['', '']
    #return tokens[0], tokens[1], tokens[2]
    return tokens