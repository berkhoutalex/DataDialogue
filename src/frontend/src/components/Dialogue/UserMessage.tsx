import React from "react";
import { Message } from "./Message";

export function UserMessage({
    avatar,
    children,
  }: {
    avatar: React.ReactNode;
    children: React.ReactNode;
  }) {
    return (
      <Message avatar={avatar} origin="user">
        {children}
      </Message>
    );
  }
  