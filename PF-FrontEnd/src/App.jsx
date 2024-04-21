import { useState } from 'react'
import './App.css'
import { Route, Routes } from 'react-router-dom'
import Menu from '../pages/Menu'
import Chart from '../pages/Chart'

function App() {

  return (
    <Routes>
      <Route path='/' element={<Menu/>}></Route>
      <Route path='/visualize/:id' element={<Chart/>}></Route>
    </Routes>
  )
}

export default App
