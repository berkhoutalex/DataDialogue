import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  currCode: string;
  setCode: (value: string | undefined) => void;
  resetCode : () => void;
  runCode : (value : string) => void;
}

const CodeEditor = (props : CodeEditorProps) => {
  const {currCode, setCode, resetCode, runCode} = props;

  return (
    <div style={{display:"flex", flexDirection:"column", height:"100%", width:"100%"}}>
      <div style={{display:"flex", flexDirection:"row", justifyContent:"flex-end", paddingRight:"1rem"}}>
        <button onClick={resetCode}>Reset</button>
        <button onClick={() => runCode(currCode)}>Run</button>
      </div>
      <Editor defaultLanguage="python" value={currCode} onChange={setCode} />
    </div>
  )
}

export default CodeEditor;