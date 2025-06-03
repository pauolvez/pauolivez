import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import EnVenta from './pages/EnVenta';
import Finanzas from './pages/Finanzas';
import Perfil from './pages/Perfil';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/enventa" element={<EnVenta />} />
        <Route path="/finanzas" element={<Finanzas />} />
        <Route path="/perfil" element={<Perfil />} />
      </Routes>
    </BrowserRouter>
  );
}
