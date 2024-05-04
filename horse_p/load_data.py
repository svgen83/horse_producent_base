
import json                    

                       
                      

 # load JSON data from file
                      

with open('db.json', 'r') as file:
    data = json.load(file)
# key to remove
                      

key_to_remove = "content_type"
# checking if the key exists before removing
for i in data:                     
    if key_to_remove in i['fields']:
        removed_value = i['fields'].pop(key_to_remove)
        print(f"Removed key '{key_to_remove}' with value: {removed_value}")
                      
# saving the updated JSON data back to the file
                      
with open('output.json', 'w') as file:
    json.dump(data, file, indent=2)
                      

