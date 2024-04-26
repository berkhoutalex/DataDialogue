import { Grid } from "@mui/material";
import React from "react";
import { ChatText } from "./ChatText";
import { Origin } from "./Shared";

export function ChatBubble({
    origin,
    children,
  }: {
    origin: Origin;
    children: React.ReactNode;
  }) {
    return (
      <Grid xs={8} item>
        <ChatText origin={origin}>{children}</ChatText>
      </Grid>
    );
  }