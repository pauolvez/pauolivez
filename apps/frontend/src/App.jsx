import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import EnVenta from './pages/EnVenta';
import Finanzas from './pages/Finanzas';
import Perfil from './pages/Perfil';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './ProtectedRoute';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <nav style={{ padding: '8px' }}>
          <Link to="/">Dashboard</Link> |{' '}
          <Link to="/enventa">En venta</Link> |{' '}
          <Link to="/finanzas">Finanzas</Link> |{' '}
          <Link to="/perfil">Perfil</Link>
        </nav>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/enventa"
            element={
              <ProtectedRoute>
                <EnVenta />
              </ProtectedRoute>
            }
          />
          <Route
            path="/finanzas"
            element={
              <ProtectedRoute>
                <Finanzas />
              </ProtectedRoute>
            }
          />
          <Route
            path="/perfil"
            element={
              <ProtectedRoute>
                <Perfil />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
