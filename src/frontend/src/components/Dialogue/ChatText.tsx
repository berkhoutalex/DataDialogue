import { Paper } from "@mui/material";
import { styled } from "@mui/material/styles";
import { Origin } from "./Shared";

export const ChatText = styled(Paper)<{ origin: Origin }>(
    ({ theme, origin }) => ({
      ...theme.typography.body2,
      padding: theme.spacing(1),
      marginTop: theme.spacing(1),
      backgroundColor: origin === "user" ? "#4B0082" : "#5A5A5A",
      color: "#FFFFFF",
      borderRadius: "15px",
      borderTopLeftRadius: origin === "user" ? "2px" : undefined,
      borderTopRightRadius: origin === "bot" ? "2px" : undefined,
      wordBreak: "break-word",
    })
  );