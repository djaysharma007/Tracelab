import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutGrid, BarChart2, FlaskConical } from 'lucide-react';

export default function Header({ algorithmName, category }) {
  const location = useLocation();

  return (
    <header style={{
      height: 56,
      borderBottom: '1px solid var(--color-line)',
      background: 'var(--color-paper)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 20px',
      zIndex: 10
    }}>
      {/* Brand Title */}
      <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10 }}>
        <FlaskConical size={22} color="var(--color-rose-deep)" />
        <span style={{ fontFamily: 'var(--font-heading)', fontSize: 20, fontWeight: 700, color: 'var(--color-ink)' }}>
          TraceLab
        </span>
      </Link>

      {/* Active Algorithm Title if in Lab route */}
      {algorithmName && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 15, fontWeight: 600 }}>{algorithmName}</span>
          {category && (
            <span style={{ fontSize: 12, color: 'var(--color-ink-muted)', border: '1px solid var(--color-line)', padding: '2px 8px', borderRadius: 12 }}>
              {category}
            </span>
          )}
        </div>
      )}

      {/* Navigation Links */}
      <nav style={{ display: 'flex', gap: 12 }}>
        <Link to="/" style={{ textDecoration: 'none' }}>
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            background: location.pathname === '/' ? 'var(--color-almond-silk)' : 'transparent',
            borderColor: location.pathname === '/' ? 'var(--color-camel)' : 'var(--color-line)'
          }}>
            <LayoutGrid size={16} />
            <span>Catalogue</span>
          </button>
        </Link>
        <Link to="/compare" style={{ textDecoration: 'none' }}>
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            background: location.pathname === '/compare' ? 'var(--color-almond-silk)' : 'transparent',
            borderColor: location.pathname === '/compare' ? 'var(--color-camel)' : 'var(--color-line)'
          }}>
            <BarChart2 size={16} />
            <span>Compare</span>
          </button>
        </Link>
      </nav>
    </header>
  );
}
