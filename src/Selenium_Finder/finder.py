from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

class Finder:
    
    def __init__(self, driver, options = {}):
        self.driver = driver
        self.global_wait = options["global_wait"] if "global_wait" in options.keys() else 10
        self.iterable_each_wait = options["iterable_each_wait"] if "iterable_each_wait" in options.keys() else 1
        self.wait = WebDriverWait(driver, self.global_wait)
        self.data_map = {};
        
    def iterable_callback(self, selector, mapping, parent_key):
        elems_arr = []
        for elem in WebDriverWait(self.driver, self.global_wait).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))):
            elem_obj = {}
            for key in mapping.keys():
                try:
                    elem_obj[key] = WebDriverWait(elem, self.iterable_each_wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, mapping[key]))).text
                except TimeoutException:
                    continue
            if len(elem_obj.keys()) > 0:
                elems_arr.append(elem_obj)
        self.data_map[parent_key] = elems_arr
                
    def find_single_map(self, json_map, key):
        if json_map["type"] == "clickable":
            elem = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, json_map["elem"])))
            elem.click()
            if "effect" in json_map.keys():
                self.find_single_map(json_map["effect"], key)
        if json_map["type"] == "iterable":
            self.iterable_callback(json_map["elem"], json_map["map"], key)
        if json_map["type"] == "typable":
            el = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, json_map["elem"])))
            el.send_keys(json_map["text"])
            if "enter" in json_map.keys():
                el.send_keys(Keys.RETURN)
        if json_map["type"] == "text":
            self.data_map[key] = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, json_map["elem"]))).text
        if json_map["type"] == "value":
            self.data_map[key] = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, json_map["elem"]))).get_attribute(json_map["value"])
        if json_map["type"] == "attribute":
            self.data_map[key] = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, json_map["elem"]))).get_attribute(json_map["attribute"])
    
    def find_with_maping(self, mapping):
        for key in mapping.keys():
            self.find_single_map(mapping[key], key)
            if "with_refresh" in mapping[key].keys():
                self.driver.refresh()
                
    def load_mapping(self, json_path):
        with open(json_path, 'r') as json_mapping:
            self.mapping = json.load(json_mapping)
            print(self.mapping)
    
    def get_mapping(self):
        return self.mapping
        
    def set_mapping(self, new_mapping):
        self.mapping = new_mapping
        
    def by_json_scheme(self):
        self.find_with_maping(self.mapping)
        
    def get_mapped_data(self):
        return self.data_map
        