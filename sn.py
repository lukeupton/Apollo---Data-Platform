import csv

class SN():
    def __init__(self) -> None:
        self.names_dict_filepath = 'config\SN.csv'
        self.names_dict = {}
        self.load_names_dict()
        
    def load_names_dict(self):
        with open(self.names_dict_filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = row.pop(reader.fieldnames[0])
                self.names_dict[key] = row["default"]
        self.sort_names()

    def set_name(self,name,value):
        if name in self.names_dict:
            self.names_dict[str(name)] = value
        else:
            print(name, "does not exist.")

    def get_name(self,name):
        if name in self.names_dict:
            return self.names_dict[str(name)]
        else:
            print(name, "does not exist. Returning 0.")
            return 0
        
    def sort_names(self):
        self.names_dict = dict(sorted(self.names_dict.items()))

    def get_all_names(self):
        keys = list(self.names_dict.keys())
        return keys
