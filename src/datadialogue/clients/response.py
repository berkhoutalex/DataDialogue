import re

class CodeResponse():

  def __init__(self, prompt: str, raw_response:str):
    self.raw_response = raw_response
    self.code = self.extract_code()
    print(self.code)
    self.prompt = prompt
    self.extras = self.extract_extras()
    

    
  def extract_code(self):
    code = re.search(r"```python(.*?)```", self.raw_response, re.DOTALL)
    code2 = re.search(r"```(.*?)```", self.raw_response, re.DOTALL)
    code3 = re.search(r"\[PYTHON\](.*?)\[\/PYTHON\]", self.raw_response, re.DOTALL)
    if code3 and code3.group(1) != "":
      return code3.group(1)
    elif code and code.group(1) != "":
      return code.group(1)
    elif code2 and code2.group(1) != "":
      return code2.group(1)
    else:
      return None
  def extract_extras(self):
    extras = re.sub(r"```(.*?)```", "", self.raw_response, re.DOTALL)
    return extras.strip()
    
  def __str__(self):
    return self.raw_response
  
  def execute(self):
    exec(self.code)