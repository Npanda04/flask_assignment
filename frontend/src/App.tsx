import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { LandingPage } from "./pages/LandingPage"
import { UserFormPage } from './pages/UserFormPage'
import { UserUpdateFormPage } from './pages/UserUpdateFormPage'


function App() {


  return (
    <>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/userform" element={<UserFormPage />} />
          <Route path="/userform/:userId" element={<UserUpdateFormPage />} />
        </Routes>
      </BrowserRouter>
    </>

  )
}

export default App
