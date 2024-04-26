import React from "react";export function ChatBox({ children }: { children: React.ReactNode }) {
  return (
    <div style={{display:"flex", flexDirection:"column-reverse", height:"100%", overflowY:'scroll', width:"100%", paddingBottom:"1rem"}}>
      {children}
    </div>
  )
}