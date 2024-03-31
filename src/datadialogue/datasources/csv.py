

import os
from src.datadialogue.datasources.source import Source


class CSVDataSource(Source):
  
  file_schemas = {}
  
  def __init__(self, files_path):
    self.files_path = files_path
    self.path_to_files_with_headers()
    
  def path_to_files_with_headers(self):
    for file in os.listdir(self.files_path):
      if file.endswith(".csv"):
        file_path = os.path.join(self.files_path, file)
        with open(file_path, "r") as f:
          header = f.readline()
          header = header.replace("\n", "")
          r1 = f.readline()
          self.file_schemas[file_path] = header + "\n" + r1
                    
  def file_and_headers(self,file_name):
    return f"{ file_name }: { self.file_schemas[file_name] }"
          
  def data_to_prompt(self):
    files = [self.file_and_headers(file) for file in self.file_schemas.keys()]
    return [
        { 
          "role": "system",  
          "content": "You have access to the following files given as FileName:{Headers and first row} " + ", ".join(files),
        }
      ]