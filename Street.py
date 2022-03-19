
import re
import logging
import logging.config
import yaml
import pandas as pd
import id_generator

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("sampleLogger")



class Street:
    def __init__(self, list_str: list):
        self.data_path = "data/place_list.csv"
        self.name = self.__extract_address(list_str)
        self.id = self.__lookup_id(self.name)


    def __extract_address(self, list_str: list) -> str:
        if len(list_str) == 0:
            raise ValueError("Unable to detect a street! The ticket may not have it, it might have been misread or the RegEx might be incomplete")
        if len(list_str) > 1:
            logger.warning("detected more than one street, only the first entry will be taken. filtered_text_list content: " + ' --- '.join(list_str))

        # remove 'n' if present
        address = re.sub(  r" n[.,;:]?", '', list_str[0])

        #places_df = pd.read_csv(places_data_path, encoding='utf-8')
        #place_id = place_id_from_street(street, places_df)

        return address

    def __lookup_id(self, street_name):
        data = pd.read_csv(self.data_path, delimiter=',')

        place_entry = data[ data["street"] == street_name ]

        if place_entry.empty: #The street is missing, add it
            logger.info(f"The street {street_name} is missing from the dataset, thus it will be added")
            street_id = id_generator.next_id(data["id"].max(), 3)
            new_street = pd.DataFrame({"id": [street_id], "street": [street_name]})
            new_data = pd.concat([data, new_street])
            new_data.to_csv(self.data_path, mode='w', index=False)
        else:
            street_id = place_entry["id"].iloc[0]

        return street_id

    def __str__(self) -> str:
        #return f"street {self.name} (ID {self.id})"
        return self.id