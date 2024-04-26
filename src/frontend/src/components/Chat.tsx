import FullChat, { Message } from './Dialogue/FullChat';
import { useState } from 'react';
import CodeEditor from './Editor';

const chatSocket = new WebSocket(
  'ws://'
  + "localhost:8000"
  + '/ws/'
  + 'chat/'
);

const Chat = () => {
  
  const addBotMessage = (text : string) => {
    setMessages(m => [{from: "bot", content:text},  ...m])
  }

  const addUserMessage = (text : string) => {
    sendMessage(text)
    setMessages(m => [{from: "user", content:text},  ...m])
  }

  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    const html = data['html'];
    const code = data['code'];
    if (code) {
      setCurrCode(code)
      setLastCodeFromBot(code)
    }
    if (html) {
      setCurrPlot(html)
    }
    if (message){
      addBotMessage(message);
    }
  };

  const sendMessage = (message : string) => {
    chatSocket.send(JSON.stringify({
      'message': message
    }));
  }

  const executeCode = (code : string) => {
    chatSocket.send(JSON.stringify({
      'code': code
    }));
  }

  const [messages, setMessages] = useState<Message[]>([{from: "bot", content: "Hello, I am a bot. How can I help you?"}])
  const [currPlot, setCurrPlot] = useState<string>("")
  const [currCode, setCurrCode] = useState<string>("")
  const [lastCodeFromBot, setLastCodeFromBot] = useState<string>("")

  
  const setCode = (value : string | undefined ) => {
    if (value) {
      setCurrCode(value)
    }
    
  }
  

  const codeEditorProps = {
    currCode,
    setCode : setCode,
    resetCode : () => setCurrCode(lastCodeFromBot),
    runCode : (value : string) => executeCode(value)
  }


  return (
    <div style={{display:"flex", flexDirection:"row", height:"100%"}}>
      <div style={{display:"flex", flexDirection:"column", width:"50%", height:"100%"}}>
        <FullChat messages={messages} addMessage={addUserMessage} />
      </div>

      <div style={{display:"flex", flexDirection:"column", width:"50%", height:"100%"}}>
          <div style={{height:"50%", width:"100%"}}>
            <iframe srcDoc={currPlot} title="Plots" height={"100%"} width={"100%"}/>
          </div>
          <div style={{height:"50%", overflow:"auto"}}>
            <CodeEditor {...codeEditorProps} />
          </div>

      </div>
    </div>
    
  )
}

export default Chat
