import { useState } from 'react';
import { apiFetch } from '../api';
import { useAuth } from '../AuthContext';

export default function Dashboard() {
  const { logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);

  async function handleSearch() {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch('/products/search', { method: 'POST' });
      setProducts(data.products);
    } catch (err) {
      setError('Error al buscar productos');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: '1rem' }}>
      <button onClick={logout}>Cerrar sesión</button>
      <h2>Dashboard</h2>
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Buscando...' : 'Buscar productos'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginTop: '1rem' }}>
        {products.map((p, idx) => (
          <div key={idx} style={{ border: '1px solid #ccc', padding: '0.5rem', width: '200px' }}>
            <img src={p.image} alt={p.name} style={{ maxWidth: '100%' }} />
            <p>{p.name}</p>
            <p>Proveedor: ${p.supplier_price}</p>
            <p>Amazon: ${p.amazon_price}</p>
            <p>Estimado ventas: {p.estimated_sales}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
