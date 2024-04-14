import { Grid } from "@mui/material";
import React from "react";

export function MessageIcon({ children }: { children: React.ReactNode }) {
    return (
      <Grid item paddingLeft={1} paddingRight={1}>
        {children}
      </Grid>
    );
}