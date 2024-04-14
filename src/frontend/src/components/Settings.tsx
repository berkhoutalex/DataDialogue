import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { Button, TextField } from '@mui/material';
import axios from 'axios';

type ModelProvider = "OpenAI" | "Anthropic" | "Ollama"

interface SettingsResponse {
  provider: ModelProvider;
  model: string;
  apiKey: string;

}

function supportedModels(model : ModelProvider) {
  if (model === "OpenAI") {
    return ["gpt-3.5-turbo", "gpt-4.0-turbo"];
  } else if (model === "Anthropic") {
    return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"];
  } else {
    return ["wizardcoder", "wizardcoder:7b-python", "deepseek-coder", "codellama", "llama2"]
  }
}

function requestSettings(setResponse : (response : SettingsResponse) => void) {
  axios.get('http://localhost:8000/settings/').then((response) => {
    const settings = {
      provider: response.data.provider,
      model: response.data.model,
      apiKey: response.data.key
    }
    setResponse(settings);
  }
  )
}



const Settings = () => {

  const [modelProvider, selectModelProvider] = React.useState<ModelProvider>("OpenAI");
  const [model, setModel] = React.useState<string>("gpt-3.5-turbo");
  const [apiKey, setApiKey] = React.useState<string>("");

  function saveSettings() {
    axios.patch('http://localhost:8000/settings/', {
      provider: modelProvider,
      model: model,
      apiKey: apiKey
    }).then((response) => {
      console.log(response);
    })
  }

  React.useEffect(() => {
    requestSettings((response) => {
      selectModelProvider(response.provider);
      setModel(response.model);
      setApiKey(response.apiKey);
    });
  }, []);

  function requestKey(model : string) {
    axios.get(`http://localhost:8000/key/${model}/`).then((response) => {
      setApiKey(response.data.key);
    })
  }

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.value === "OpenAI") {
      selectModelProvider("OpenAI");
      setModel("gpt-3.5-turbo")
      requestKey("OpenAI");
    } else if (event.target.value === "Anthropic") {
      selectModelProvider("Anthropic");
      setModel("claude-3-opus-20240229")
      requestKey("Anthropic");
    }
    else {
      selectModelProvider("Ollama");
      setModel("wizardcoder")
      requestKey("Ollama");
    }
  };

  const ControlledRadioButtonsGroup = () => {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Model</FormLabel>
        <RadioGroup
          aria-label="model"
          name="model"
          value={modelProvider}
          onChange={handleChange}
        >
          <FormControlLabel value="OpenAI" control={<Radio />} label="OpenAI" />
          <FormControlLabel value="Anthropic" control={<Radio />} label="Anthropic" />
          <FormControlLabel value="Ollama" control={<Radio />} label="Ollama" />
        </RadioGroup>
      </FormControl>
    );
  }

  const handleModelChange = (event: SelectChangeEvent) => {
    setModel(event.target.value);
  }

  const ModelSelect = () => {
    return (
      <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
          <InputLabel id="demo-simple-select-label">Model</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={model}
            label="Model"
            onChange={handleModelChange}
          >
            {supportedModels(modelProvider).map((m) => {
              return <MenuItem value={m}>{m}</MenuItem>
            })}
          </Select>
        </FormControl>
      </Box>
    );
  }
  
  const ApiKeyForm = () => {
    return (
      <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
        <TextField
          id="outlined-basic"
          variant="outlined"
          sx={{ width: "100%", backgroundColor: "#FFFFFF" }}
          placeholder="Enter your api key"
          value={apiKey}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setApiKey(event.target.value);
          }}
        />
        </FormControl>
      </Box>
    );
  }

  const SaveButton = () => {
    return (
      <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
          <Button variant="contained" color="primary" onClick={saveSettings}>
            Save
          </Button>
        </FormControl>
      </Box>
    );
  }



  return (
    <div style={{display:"flex", flexDirection:"column"}}>
      <h1>Settings</h1>
      <ControlledRadioButtonsGroup />
      <ModelSelect />
      <ApiKeyForm />
      <SaveButton />

    </div>
  )
}

export default Settings;