import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { Link, useLocation } from 'react-router-dom'
import { Chat, Settings } from '@mui/icons-material';

interface NavBarProps {
  drawerWidth: number;
  content: React.ReactNode;
}


export default function NavBar (props : NavBarProps) {
  const { drawerWidth, content } = props
  const location = useLocation()
  const path = location.pathname
  const [open, setOpen] = React.useState(false)

  const changeOpen = () => {
    setOpen(!open)
  }

  const myDrawer = (
    <div >
      <Toolbar />
      <Box sx={{ overflow: 'auto'}}>
        <List>
          <ListItem disablePadding>
            <ListItemButton component={Link} to='/' selected={'/' === path}>
              <ListItemIcon>
                <Chat />
              </ListItemIcon>
              <ListItemText primary={'Chat'} />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to='/settings'
              selected={'/settings' === path}
            >
              <ListItemIcon>
                <Settings />
              </ListItemIcon>
              <ListItemText primary={'Settings'} />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </div>
  )

  return (
    <Box sx={{ display: 'flex', height:"100%" }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Data Dialogue
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant='permanent'
        sx={{
          display: { xs: 'none', sm: 'block' },
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: 'border-box'
          }
        }}
      >
        {myDrawer}
      </Drawer>
      <Drawer
        variant='temporary'
        open={open}
        onClose={changeOpen}
        sx={{
          display: { xs: 'block', sm: 'none' },
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: 'border-box'
          }
        }}
      >
        {myDrawer}
      </Drawer>
      <Box component='main' sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {content}
      </Box>
    </Box>
  );
}
