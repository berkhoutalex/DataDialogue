import React from "react";
import { Message } from "./Message";

export function BotMessage({
    avatar,
    children,
  }: {
    avatar: React.ReactNode;
    children: React.ReactNode;
  }) {
    return (
      <Message avatar={avatar} origin="bot">
        {children}
      </Message>
    );
  }
  