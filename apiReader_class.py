import requests


class ApiReader():

	"""
	!!! ADD A DOCSTRING !!!
	"""
    
    url = "https://fr-en.openfoodfacts.org/cgi/search.pl"
    
    categories = {
    "Barres_chocolatées" : "chocolate-bars",
    "Pâtes_à_tartiner_aux noisettes_et_au_cacao" : "cocoa-and-hazelnuts-spreads",
    "Sodas_au_cola" : "colas",
    "Pizzas_surgelées" : "frozen-pizzas",
    "Barres_énergétiques" : "energy-bars",
    "Biscuits_au_chocolat" : "chocolate-biscuits",
    "Biscuits_fourrés" : "filled-biscuits",
    "Plats_au_bœuf" : "beef-dishes",
    "Plats_préparés_en_conserve" : "canned-meals",
    "Lasagnes_préparées" : "prepared-lasagne"
    }
    
    
    def __init__(self):
        
        self.action = "process"
        self.tagtype_0 = "categories"
        self.tag_contains_0 = "contains"
        self.tag_0 = ""
        self.sort_by = "completeness"
        self.page_size = 500
        self.json = 1
        
        
    def get_data(self) :

        """
        This func runs a get request to the api, iterating on
        each category defined in classvar 'categories', and automatically
        cleans the data received by calling the data_cleaner class method.

        Then returns a clean_data list, in which each first index is related to
        a category, which is itself a list made up of dictionnaries, where a
        dictionnary corresponds with a product, and its keys to product fileds, 
        i.e. columns in db :

        clean_data[list_index/category][list_index/product][dict_key/field]
        """
        


        
        clean_data = list()
        for key, val in self.categories.items() :
            self.__dict__["tag_0"] = val
            response = requests.get(self.url, params = self.__dict__)
            clean_data.append(self.data_cleaner(response.json(), key))
        return clean_data 
        
            
            

    def data_cleaner(self, data, category):

        """
        This func automatically receives raw api json type objects, 
        corresponding to a predefined 1/10 category of food, and returns a 
        complete and clean list of data, of the requirred size and fields
        """
        
        cleaned_data = list()
        products_count = 0

        for product in data["products"]:
            # this strange try block is here to avoid which seems to be
            # an api failure : when a product's field is empty, the field name
            # itself can't be used for key indexation : an empty requirred 
            # field in the requests.Response object will drive to a KeyError
            try:
                product["product_name_fr"] is not None
                product["url"] is not None
                product["nutrition_grade_fr"] is not None
                product["stores"] is not None
                # !!! HAVE TO FIND AND ADD A DECENT DESCRIPTION FIELD                           
            except KeyError:
                continue
            
            
            # after the precedent try block on None values, necessity to
            # test empty strings now, to be sure to get non-empty strings : 
            # e.g. a test like "product[stores] is not None" will send back
            # empty fields for stores, unless None is replaced by ""
            if products_count >= 70:
                break
            elif product["product_name_fr"] != "" \
               and product["url"] != "" \
               and product["nutrition_grade_fr"] != "" \
               and product["stores"] != "" :
                cleaned_data.append({
                    "category" : category,
                    "product_name_fr" : product["product_name_fr"],
                    "url" : product["url"],
                    "nutrition_grade_fr" : product["nutrition_grade_fr"],
                    "stores" : product["stores"]})
                products_count += 1
            else :
                continue
        return cleaned_data

            
 
                
api_reader = ApiReader()
clean_data = list(api_reader.get_data())      
print(clean_data, len(clean_data), sep="\n")



