import { Avatar, Badge, TextField, styled } from "@mui/material";
import { ChatBox } from "./ChatBox";

import userImg from "./user.png";
import botImg from "./bot.png";
import { UserMessage } from "./UserMessage";
import { BotMessage } from "./BotMessage";
import { FormEvent, useRef } from "react";
import React from "react";

const BotAvatar = () => (
  <StyledBadge
    overlap="circular"
    anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
  >
    {" "}
    <Avatar src={botImg} />

  </StyledBadge>
)

const UserAvatar = () => (
  <StyledBadge
    overlap="circular"
    anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
  >
    {" "}
    <Avatar src={userImg} />

  </StyledBadge>
)

const StyledBadge = styled(Badge)(({ theme }) => ({
  "& .MuiBadge-badge": {
    backgroundColor: "#44b700",
    color: "#44b700",
    boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
    "&::after": {
      position: "absolute",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      borderRadius: "50%",
      animation: "ripple 1.2s infinite ease-in-out",
      border: "1px solid currentColor",
      content: '""',
    },
  },
  "@keyframes ripple": {
    "0%": {
      transform: "scale(.8)",
      opacity: 1,
    },
    "100%": {
      transform: "scale(2.4)",
      opacity: 0,
    },
  },
}));

interface Message {
  from: "bot" | "user";
  content: string;
}

interface FullChatProps {
  messages: Message[];
  addMessage: (text: string) => void;
}


function FullChat(props: FullChatProps) {

  const [message, setMessage] = React.useState("");

  const onNewMessage = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    props.addMessage(message);
    setMessage("");
  }
  return (
    <div style={{ display:"flex", flexDirection:"column", marginLeft: "0", backgroundColor: "#141414", border: "1px solid #000000", width:"100%", height:"100%"}}>
      <ChatBox>
        {props.messages.map((m, i) =>
          m.from === "user" ? (
            <UserMessage key={i} avatar={<UserAvatar />}>
              <p style={{whiteSpace:"pre-wrap"}}>{m.content}</p>
            </UserMessage>
          ) : (
            <BotMessage key={i} avatar={<BotAvatar />}>
              <p style={{whiteSpace:"pre-wrap"}}>{m.content}</p>
            </BotMessage>
          )
        )}
      </ChatBox>
      <form onSubmit={(e) => onNewMessage(e)}>
        <TextField
          id="outlined-basic"
          variant="outlined"
          multiline={true}
          sx={{ width: "100%", backgroundColor: "#FFFFFF", textWrap: "wrap"}}
          placeholder="Enter your prompt here"
          value={message}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setMessage(event.target.value);
          }}
          onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
              if (e.key === "Enter") {
                e.preventDefault();
                props.addMessage(message);
                setMessage("");
            }
            }
          }
        />
      </form>
    </div>
  );
}

export default FullChat;
export type { Message };