'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import './sidebar.css';

type Role = 'ADMIN' | 'ANALYST' | 'VIEWER' | null;

export default function Sidebar() {
  const pathname = usePathname();

  const [role, setRole] = useState<Role>(null);
  const [open, setOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  /* ================= LOAD ROLE FROM TOKEN ================= */

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const token = localStorage.getItem('access_token');

    if (!token) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setRole(null);
      return;
    }

    try {
      const parts = token.split('.');
      if (parts.length < 2) {
        setRole(null);
        return;
      }

      const payloadBase64 = parts[1];
      const decoded = JSON.parse(atob(payloadBase64)) as { role?: string };

      if (
        decoded.role === 'ADMIN' ||
        decoded.role === 'ANALYST' ||
        decoded.role === 'VIEWER'
      ) {
        setRole(decoded.role);
      } else {
        setRole(null);
      }
    } catch (err) {
      console.warn('Token decode failed', err);
      setRole(null);
    }
  }, []);

  /* ================= LOGOUT ================= */

  function handleLogout() {
    try {
      localStorage.removeItem('access_token');
    } catch {}

    window.location.href = '/login';
  }

  /* ================= GROUPED MENU ================= */

  const menuGroups = [
    {
      title: 'Overview',
      items: [
        {
          name: 'Dashboard',
          path: '/dashboard',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },
        {
          name: 'Command Center',
          path: '/command-center',
          roles: ['ADMIN'],
        },
        {
          name: 'Attack Map',
          path: '/attack-map',
          roles: ['ADMIN', 'ANALYST'],
        },
        {
          name: 'Geo Map',
          path: '/geo-map',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },
        {
          name: 'Country Heatmap',
          path: '/country-heatmap',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },
      ],
    },

    {
      title: 'Monitoring',
      items: [
        {
          name: 'Logs',
          path: '/logs',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },
        {
          name: 'Alerts',
          path: '/alerts',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },
        {
          name: 'Incidents',
          path: '/incidents',
          roles: ['ADMIN', 'ANALYST'],
        },
        {
          name: 'Live Network',
          path: '/live-network',
          roles: ['ADMIN', 'ANALYST'],
        },
        {
          name: 'Live Attack Stream',
          path: '/live-attacks',
          roles: ['ADMIN', 'ANALYST'],
        },
      ],
    },

    {
      title: 'Detection & Intelligence',
      items: [
        {
          name: 'Threat Intel',
          path: '/threat-intel',
          roles: ['ADMIN', 'ANALYST'],
        },
        {
          name: 'MITRE Map',
          path: '/mitre-map',
          roles: ['ADMIN', 'ANALYST'],
        },
        {
          name: 'IP Analyzer',
          path: '/ip-analyzer',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },

        // 🔥 NEW FEATURES ADDED HERE
        {
          name: 'Threat Hunting',
          path: '/hunting',
          roles: ['ADMIN', 'ANALYST'],
        },
        {
          name: 'Advanced Search',
          path: '/search',
          roles: ['ADMIN', 'ANALYST', 'VIEWER'],
        },
      ],
    },

    {
      title: 'Investigation',
      items: [
        {
          name: 'Attack Timeline',
          path: '/attack-timeline',
          roles: ['ADMIN', 'ANALYST'],
        },
      ],
    },

    {
      title: 'Management',
      items: [
        {
          name: 'Compliance Reports',
          path: '/compliance',
          roles: ['ADMIN'],
        },
        {
          name: 'Audit Logs',
          path: '/audit-logs',
          roles: ['ADMIN'],
        },

        // 🔥 OPTIONAL ENTERPRISE FEATURE
        {
          name: 'Assets',
          path: '/assets',
          roles: ['ADMIN', 'ANALYST'],
        },
      ],
    },

    {
      title: 'Advanced',
      items: [
        {
          name: 'AI Prediction',
          path: '/ai-prediction',
          roles: ['ADMIN'],
        },
      ],
    },
  ];

  return (
    <>
      <button className="menu-toggle" onClick={() => setOpen(!open)}>
        ☰
      </button>

      {open && (
        <div className="sidebar-overlay" onClick={() => setOpen(false)} />
      )}

      <aside
        className={`sidebar ${open ? 'open' : ''} ${collapsed ? 'collapsed' : ''}`}
      >
        <div>
          <div className="sidebar-header">
            <div className="logo-area">
              🛡
              {!collapsed && (
                <span className="logo-text">AttackSurface SOC</span>
              )}
            </div>

            <button
              className="collapse-btn"
              onClick={() => {
                const newState = !collapsed;
                setCollapsed(newState);

                if (typeof document !== 'undefined') {
                  document.documentElement.style.setProperty(
                    '--sidebar-width',
                    newState ? '80px' : '260px'
                  );
                }
              }}
            >
              {collapsed ? '➡' : '⬅'}
            </button>
          </div>

          <nav className="sidebar-nav">
            {menuGroups.map((group) => (
              <div key={group.title} className="sidebar-group">
                {!collapsed && (
                  <div className="sidebar-group-title">{group.title}</div>
                )}

                {group.items
                  .filter((item) => !role || item.roles.includes(role))
                  .map((item) => {
                    const active =
                      pathname === item.path ||
                      pathname?.startsWith(item.path + '/');

                    return (
                      <Link
                        key={item.path}
                        href={item.path}
                        onClick={() => setOpen(false)}
                        className={
                          active ? 'sidebar-link active' : 'sidebar-link'
                        }
                      >
                        {!collapsed && <span>{item.name}</span>}
                      </Link>
                    );
                  })}
              </div>
            ))}
          </nav>
        </div>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={handleLogout}>
            🚪 {!collapsed && 'Logout'}
          </button>
        </div>
      </aside>
    </>
  );
}
