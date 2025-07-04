
import FullChat, { Message } from './Dialogue/FullChat';
import { useState, useRef, useEffect } from 'react';
import CodeEditor from './Editor';

const WS_URL = 'ws://localhost:8000/ws/chat/';


const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([{from: "bot", content: "Hello, I am a bot. How can I help you?"}])
  const [currPlot, setCurrPlot] = useState<string>("")
  const [currCode, setCurrCode] = useState<string>("")
  const [lastCodeFromBot, setLastCodeFromBot] = useState<string>("")

  // WebSocket ref and reconnect logic
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);

  // Track if unmounting to avoid reconnecting after unmount
  const isUnmounting = useRef(false);

  const connectWebSocket = () => {
    // Only connect if not already open or connecting
    if (
      socketRef.current &&
      (socketRef.current.readyState === WebSocket.OPEN || socketRef.current.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    const ws = new WebSocket(WS_URL);
    socketRef.current = ws;

    ws.onopen = () => {
      // Optionally notify connection
    };

    ws.onmessage = function(e) {
      const data = JSON.parse(e.data);
      const message = data['message'];
      const html = data['html'];
      const code = data['code'];
      const error = data['error'];
      if (code) {
        setCurrCode(code)
        setLastCodeFromBot(code)
      }
      if (html) {
        setCurrPlot(html)
      }
      if (error) {
        // Format error message for chat display
        let errorMsg = `❌ Error: ${error}`;
        if (data.details) {
          errorMsg += `\nDetails: ${data.details}`;
        }
        if (data.traceback) {
          errorMsg += `\n\n<details><summary>Show Traceback</summary><pre style='white-space:pre-wrap;'>${data.traceback}</pre></details>`;
        }
        addBotMessage(errorMsg);
      } else if (message) {
        addBotMessage(message);
      }
    };

    ws.onclose = () => {
      // Only reconnect if not unmounting
      if (!isUnmounting.current && !reconnectTimeout.current) {
        reconnectTimeout.current = setTimeout(() => {
          connectWebSocket();
          reconnectTimeout.current = null;
        }, 2000); // 2 seconds
      }
    };

    ws.onerror = () => {
      // Only close if not already closed
      if (ws.readyState !== WebSocket.CLOSED && ws.readyState !== WebSocket.CLOSING) {
        ws.close(); // Will trigger onclose and reconnect
      }
    };
  };

  useEffect(() => {
    isUnmounting.current = false;
    connectWebSocket();
    return () => {
      isUnmounting.current = true;
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const addBotMessage = (text : string) => {
    setMessages(m => [{from: "bot", content:text},  ...m])
  }

  const addUserMessage = (text : string) => {
    sendMessage(text)
    setMessages(m => [{from: "user", content:text},  ...m])
  }


  const sendMessage = (message : string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({
        'message': message
      }));
    } else {
      addBotMessage("Connection lost. Please wait while we reconnect...");
    }
  }

  const executeCode = (code : string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({
        'code': code
      }));
    } else {
      addBotMessage("Connection lost. Please wait while we reconnect...");
    }
  }

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
