import * as React from 'react';
import FormControl from '@mui/material/FormControl';
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
  dataSource: string;
  dataSourcePath: string;

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
      apiKey: response.data.key,
      dataSource: response.data.dataSource,
      dataSourcePath: response.data.dataSourcePath
    }
    setResponse(settings);
  }
  )
}

const Settings = () => {

  const [modelProvider, selectModelProvider] = React.useState<ModelProvider>("OpenAI");
  const [model, setModel] = React.useState<string>("gpt-3.5-turbo");
  const [apiKey, setApiKey] = React.useState<string>("");
  const [dataSource, setDataSource] = React.useState<string>("csvs");
  const [dataSourcePath, setDataSourcePath] = React.useState<string>("");

  function saveSettings() {
    axios.patch('http://localhost:8000/settings/', {
      provider: modelProvider,
      model: model,
      apiKey: apiKey,
      dataSource: dataSource,
      dataSourcePath: dataSourcePath
    }).then((response) => {
      console.log(response);
    })
  }

  React.useEffect(() => {
    requestSettings((response) => {
      selectModelProvider(response.provider);
      setModel(response.model);
      setApiKey(response.apiKey);
      setDataSource(response.dataSource);
      setDataSourcePath(response.dataSourcePath);
    });
  }, []);

  function requestKey(model : string) {
    axios.get(`http://localhost:8000/key/${model}/`).then((response) => {
      setApiKey(response.data.key);
    })
  }

  const handleChange = (event: SelectChangeEvent) => {
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

  const ProviderSelect = () => {
    return (
      <Box sx={{ minWidth: 120, margin: "1rem" }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Model Provider</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={modelProvider}
          label="Model"
          onChange={handleChange}
        >
          <MenuItem value="OpenAI">OpenAI</MenuItem>
          <MenuItem value="Anthropic">Anthropic</MenuItem>
          <MenuItem value="Ollama">Ollama</MenuItem>
        </Select>
      </FormControl>
    </Box>
    );
  }

  const handleModelChange = (event: SelectChangeEvent) => {
    setModel(event.target.value);
  }

  const ModelSelect = () => {
    return (
      <Box sx={{ minWidth: 120, margin: "1rem" }}>
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
  function handleDataSourceChange(event: SelectChangeEvent) {
    setDataSource(event.target.value);
  }

  const DataSourceSelect = () => {
    return (
      <Box sx={{ minWidth: 120, margin: "1rem" }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Data Source</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={dataSource}
          label="DataSource"
          onChange={handleDataSourceChange}
        >
          <MenuItem value="csvs">CSVs</MenuItem>
          <MenuItem value="sqlite">SQLite</MenuItem>
        </Select>
      </FormControl>
    </Box>
    );
  }

  function handleDataSourcePathChange(event: React.ChangeEvent<HTMLInputElement>) {
    setDataSourcePath(event.target.value);
  }

  const SaveButton = () => {
    return (
      <Box sx={{ minWidth: 120, margin: "1rem" }}>
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
      <div style = {{display:"flex", flexDirection:"row", justifyContent:"flex-start"}}>
        <ProviderSelect />
        <ModelSelect />
        <Box sx={{ minWidth: 120, margin: "1rem" }}>
          <FormControl fullWidth>
          <TextField
            id="outlined-basic"
            variant="outlined"
            sx={{ width: "100%", backgroundColor: "#FFFFFF" }}
            placeholder="Enter your api key"
            value={apiKey}
            label="API Key"
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setApiKey(event.target.value);
            }}
          />
          </FormControl>
        </Box>
      </div>

      <div style = {{display:"flex", flexDirection:"row", justifyContent:"flex-start"}}>
        <DataSourceSelect />
        <Box sx={{ minWidth: 120, margin: "1rem" }}>
          <FormControl fullWidth>
          <TextField
            id="outlined-basic"
            variant="outlined"
            sx={{ width: "100%", backgroundColor: "#FFFFFF" }}
            placeholder="Enter the path to your data source"
            value={dataSourcePath}
            label="Data Source Path"
            onChange={handleDataSourcePathChange}
          />
          </FormControl>
        </Box>
      </div>
      
      <SaveButton />

    </div>
  )
}

export default Settings;