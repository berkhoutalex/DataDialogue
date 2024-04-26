import './App.css'
import { Routes, Route } from 'react-router-dom'

import Chat from './components/Chat'
import Settings from './components/Settings'
import NavBar from './components/NavBar'

function App () {
  const myWidth = 200
  return (
    <div className='App' style={{height:"95vh"}}>
      <NavBar
        drawerWidth={myWidth}
        content={
          <Routes>
            <Route path='/' element={<Chat />} />
            <Route path='/settings' element={<Settings />} />
          </Routes>
        }
      />
    </div>
  )
}

export default App
