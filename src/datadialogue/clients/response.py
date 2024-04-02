import re

class CodeResponse():

  def __init__(self, prompt: str, raw_response:str):
    self.raw_response = raw_response
    self.code = self.extract_code()
    self.prompt = prompt
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
    exec(self.code)