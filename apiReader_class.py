# -*- coding: utf-8 -*-

import requests
import constants


class ApiReader():  
    """ 
    ApiReader 's object is dedicated to api requests. Its attributes are 
    params elements of the requests.get method, so that special attribute 
    __dict__ allows to automatically build up the attributes dict the requests
    function needs, while each param remains easily upgradable 
    """
    

    def __init__(self):
        
        self.action = "process"
        self.tagtype_0 = "categories"
        self.tag_contains_0 = "contains"
        self.tag_0 = ""
        self.sort_by = "completeness"
        self.page_size = 1000
        self.json = 1
        
        
    def get_data(self, url=constants.url, categories=constants.categories) :
        """
        This func runs a get request to the api, iterating on
        each category defined in constant var 'categories', and automatically
        cleans the data received by calling the data_cleaner object method.

        Then returns a clean_data list which can be processed like this:

        clean_data[list_index=category][list_index=product][dict_key=field]
        """
        
        clean_data = list()
        for key, val in categories.items() :
            self.__dict__["tag_0"] = val
            response = requests.get(url, params = self.__dict__)
            clean_data.append(self.data_cleaner(response.json(), key))
        return clean_data 
        
                      
    def data_cleaner(self, data, category): 
        """
        This func automatically receives raw api json type objects, 
        corresponding to a predefined 1/10 category of food, and returns a 
        complete and clean list of data, composed by the requirred size 
        and fields. Params are the data itself, and the name of the
        currently processed category
        """
        
        cleaned_data = list()
        products_count = 0

        for product in data["products"]:
            # this try block is here to avoid what seems to be
            # an api failure : when a product's field is empty, the field name
            # itself can't be used for key indexation : an empty required
            # field in the requests.Response object will drive to a KeyError
            try:
                if product["product_name_fr"] is not None \
                and product["url"] is not None \
                and product["nutrition_grade_fr"] is not None \
                and product["stores"] is not None \
                and product["generic_name_fr"] is not None :
                    
                    if products_count >= constants.product_nb_per_category:
                        break
                    elif product["product_name_fr"] != "" \
                    and product["url"] != "" \
                    and product["nutrition_grade_fr"] != "" \
                    and product["stores"] != "" \
                    and product["generic_name_fr"] != "":
                        cleaned_data.append({
                                "category" : category,
                                "product_name_fr" : product["product_name_fr"],
                                "url" : product["url"],
                                "nutrition_grade_fr" : 
                                    product["nutrition_grade_fr"],
                                "stores" : product["stores"].split(","),
                                "description" : product["generic_name_fr"]
                                })
                        
                        for i, store_name in enumerate(cleaned_data[
                                len(cleaned_data) - 1]['stores']):
                            cleaned_data[len(cleaned_data) - 1]['stores'][i] =\
                                store_name.strip().lower().capitalize()
                        
                        products_count += 1
                    
                    else :
                        continue
            
            except KeyError:
                continue           

        return cleaned_data

                         
if __name__=="__main__":
    api_reader = ApiReader()
    clean_data = list(api_reader.get_data())
    print(clean_data, len(clean_data), sep="\n") # is ok
    print(clean_data[0], len(clean_data[0]), sep="\n") # is ok
    




