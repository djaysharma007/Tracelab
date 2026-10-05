import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchAlgorithms } from '../api/client';
import { Search, ArrowRight, Play } from 'lucide-react';
import Header from '../components/Header';

export default function Catalogue() {
  const [algorithms, setAlgorithms] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlgorithms()
      .then(data => {
        setAlgorithms(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filtered = algorithms.filter(alg =>
    alg.name.toLowerCase().includes(search.toLowerCase()) ||
    alg.category.toLowerCase().includes(search.toLowerCase()) ||
    alg.id.toLowerCase().includes(search.toLowerCase())
  );

  // Group by category
  const categories = {};
  filtered.forEach(alg => {
    if (!categories[alg.category]) {
      categories[alg.category] = [];
    }
    categories[alg.category].push(alg);
  });

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--color-paper)' }}>
      <Header />

      <main style={{ flex: 1, maxWidth: 1080, width: '100%', margin: '0 auto', padding: '32px 20px' }}>
        {/* Typographic Intro */}
        <div style={{ marginBottom: 28 }}>
          <h1 style={{ fontSize: 32, fontFamily: 'var(--font-heading)', color: 'var(--color-ink)', marginBottom: 8 }}>
            Algorithm Catalogue
          </h1>
          <p style={{ color: 'var(--color-ink-muted)', fontSize: 16 }}>
            Select an algorithm from the 28 laboratory implementations to launch step-by-step state playback, performance profiling, and complexity analysis.
          </p>
        </div>

        {/* Filter Box */}
        <div style={{ marginBottom: 24, position: 'relative', maxWidth: 400 }}>
          <Search size={18} style={{ position: 'absolute', left: 12, top: 10, color: 'var(--color-ink-muted)' }} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Filter algorithms or category..."
            style={{
              width: '100%',
              padding: '8px 12px 8px 38px',
              border: '1px solid var(--color-camel)',
              borderRadius: 'var(--radius)',
              background: 'var(--color-ink)',
              color: '#ffffff',
              fontSize: 14
            }}
          />
        </div>

        {/* Typographic Index Table */}
        {loading ? (
          <div style={{ padding: 40, textAlign: 'center', color: 'var(--color-ink-muted)' }}>Loading algorithm catalogue...</div>
        ) : (
          Object.entries(categories).map(([catName, algList]) => (
            <section key={catName} style={{ marginBottom: 32 }}>
              <h2 style={{
                fontSize: 18,
                fontFamily: 'var(--font-heading)',
                borderBottom: '2px solid var(--color-line)',
                paddingBottom: 6,
                marginBottom: 12,
                color: 'var(--color-ink)'
              }}>
                {catName} ({algList.length})
              </h2>

              <div style={{ border: '1px solid var(--color-line)', borderRadius: 'var(--radius)', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead>
                    <tr style={{ background: 'var(--color-almond-silk)', fontSize: 12, textTransform: 'uppercase', color: 'var(--color-ink-muted)' }}>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--color-line)' }}>Algorithm</th>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--color-line)' }}>Average Complexity</th>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--color-line)' }}>Space Complexity</th>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--color-line)' }}>Compare Group</th>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--color-line)', textAlign: 'right' }}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {algList.map((alg) => (
                      <tr
                        key={alg.id}
                        style={{
                          borderBottom: '1px solid var(--color-line)',
                          transition: 'background 0.1s ease-out'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = 'var(--color-almond-silk)'}
                        onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                      >
                        <td style={{ padding: '12px 16px', fontWeight: 600 }}>
                          <Link to={`/lab/${alg.id}`} style={{ color: 'var(--color-ink)', textDecoration: 'none' }}>
                            {alg.name}
                          </Link>
                        </td>
                        <td style={{ padding: '12px 16px', fontFamily: 'var(--font-mono)', fontSize: 13 }}>
                          {alg.complexity.average}
                        </td>
                        <td style={{ padding: '12px 16px', fontFamily: 'var(--font-mono)', fontSize: 13 }}>
                          {alg.complexity.space}
                        </td>
                        <td style={{ padding: '12px 16px', fontSize: 13, color: 'var(--color-ink-muted)' }}>
                          {alg.compare_group ? (
                            <span style={{ border: '1px solid var(--color-line)', padding: '2px 8px', borderRadius: 12 }}>
                              {alg.compare_group}
                            </span>
                          ) : (
                            '—'
                          )}
                        </td>
                        <td style={{ padding: '12px 16px', textAlign: 'right' }}>
                          <Link to={`/lab/${alg.id}`} style={{ textDecoration: 'none' }}>
                            <button className="btn-primary" style={{ padding: '4px 12px', fontSize: 12, display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                              <Play size={12} />
                              <span>Open Lab</span>
                            </button>
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          ))
        )}
      </main>
    </div>
  );
}
