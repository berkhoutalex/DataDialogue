import re

class CodeResponse():
  def __init__(self, raw_response:str):
    self.raw_response = raw_response
    self.code = self.extract_code()
    self.extras = self.extract_extras()
    
  def extract_code(self):
    code = re.search(r"```python(.*?)```", self.raw_response, re.DOTALL)
    return code.group(1) if code else None
  
  def extract_extras(self):
    extras = re.sub(r"```python(.*?)```", "", self.raw_response, re.DOTALL)
    return extras.strip()
    
  def __str__(self):
    return self.raw_response
  
  def execute(self):
    print(self.extras)
    exec(self.code)