import React from "react";
import { ChatBubble } from "./ChatBubble";
import { MessageIcon } from "./MessageIcon";
import { Origin } from "./Shared";

export function Message({
    avatar,
    origin,
    children,
  }: {
    avatar: React.ReactNode;
    origin: Origin;
    children: React.ReactNode;
  }) {
    const flexDirection = origin === "user" ? "row" : "row-reverse";
    return (
      <div
        style={{ minWidth: "100%", padding: "0.5rem", flexDirection:flexDirection}}
      >
        <MessageIcon>{avatar}</MessageIcon>
        <ChatBubble origin={origin}>{children}</ChatBubble>
      </div>
    );
  }