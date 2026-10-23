
import { useEffect, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Line,
  LineChart,
} from 'recharts'
import './App.css'
import AIChat from './AIChat'

const API_URL = 'http://127.0.0.1:8000'

type CategoryRevenue = {
  category: string
  order_count: number
  units_sold: number
  total_revenue: number
}

type MonthlyRevenue = {
  month: string
  order_count: number
  units_sold: number
  total_revenue: number
}

type TopCustomer = {
  customer_id: number
  customer_name: string
  company: string | null
  order_count: number
  total_revenue: number
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-DE', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value)
}

function App() {
  const [categories, setCategories] = useState<CategoryRevenue[]>([])
  const [monthly, setMonthly] = useState<MonthlyRevenue[]>([])
  const [customers, setCustomers] = useState<TopCustomer[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true)
        setError('')

        const endpoints = [
          `${API_URL}/analytics/revenue-by-category`,
          `${API_URL}/analytics/monthly-revenue`,
          `${API_URL}/analytics/top-customers?limit=10`,
        ]

        const responses = await Promise.all(
          endpoints.map((endpoint) => fetch(endpoint)),
        )

        if (responses.some((response) => !response.ok)) {
          throw new Error('The API returned an error. Check your backend.')
        }

        const [categoryData, monthlyData, customerData] = await Promise.all(
          responses.map((response) => response.json()),
        )

        setCategories(categoryData)
        setMonthly(
          monthlyData.map((item: MonthlyRevenue) => ({
            ...item,
            month: new Date(item.month).toLocaleDateString('en-GB', {
              month: 'short',
              year: '2-digit',
              timeZone: 'UTC',
            }),
          })),
        )
        setCustomers(customerData)
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load dashboard data.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  const totalRevenue = categories.reduce(
    (sum, item) => sum + Number(item.total_revenue),
    0,
  )
  const totalOrders = categories.reduce(
    (sum, item) => sum + Number(item.order_count),
    0,
  )
  const totalUnits = categories.reduce(
    (sum, item) => sum + Number(item.units_sold),
    0,
  )

  if (loading) {
    return (
      <main className="app-shell">
        <div className="status-message">Loading your business analytics…</div>
      </main>
    )
  }

  if (error) {
    return (
      <main className="app-shell">
        <div className="error-panel">
          <h2>Unable to load analytics</h2>
          <p>{error}</p>
          <p>
            Ensure PostgreSQL and FastAPI are running, then refresh this page.
          </p>
        </div>
      </main>
    )
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">A</div>
          <div>
            <strong>AI Ops</strong>
            <span>OPERATIONS COPILOT</span>
          </div>
        </div>

        <nav className="navigation">
          <a className="nav-link active" href="#overview">Overview</a>
          <a className="nav-link" href="#revenue">Revenue analytics</a>
          <a className="nav-link" href="#customers">Customers</a>
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          PostgreSQL connected
        </div>
      </aside>

      <section className="main-content">
        <header className="page-header" id="overview">
          <div>
            <p className="eyebrow">BUSINESS INTELLIGENCE</p>
            <h1>Operations overview</h1>
            <p className="subtitle">
              Your business performance, all in one place.
            </p>
          </div>
          <div className="date-label">
            <span className="status-dot" />
            Live database analytics
          </div>
        </header>

        <section className="metrics-grid" aria-label="Business metrics">
          <article className="metric-card">
            <p>Total revenue</p>
            <h2>{formatCurrency(totalRevenue)}</h2>
            <span>Completed orders across all categories</span>
          </article>

          <article className="metric-card">
            <p>Completed orders</p>
            <h2>{totalOrders.toLocaleString('en-GB')}</h2>
            <span>Orders included in revenue analytics</span>
          </article>

          <article className="metric-card">
            <p>Units sold</p>
            <h2>{totalUnits.toLocaleString('en-GB')}</h2>
            <span>Units across completed orders</span>
          </article>
        </section>

        <section className="charts-grid" id="revenue">
          <article className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">REVENUE BREAKDOWN</p>
                <h2>Revenue by category</h2>
              </div>
              <span className="panel-tag">By category</span>
            </div>

            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={categories}
                  margin={{ top: 12, right: 8, left: 4, bottom: 4 }}
                >
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="category" tickLine={false} axisLine={false} />
                  <YAxis
                    tickFormatter={(value: number) =>
                      new Intl.NumberFormat('en', {
                        notation: 'compact',
                      }).format(value)
                    }
                    tickLine={false}
                    axisLine={false}
                    width={48}
                  />
                  <Tooltip
                    formatter={(value) => formatCurrency(Number(value))}
                  />
                  <Bar
                    dataKey="total_revenue"
                    name="Revenue"
                    fill="#6478e8"
                    radius={[6, 6, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </article>

          <article className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">REVENUE TREND</p>
                <h2>Monthly performance</h2>
              </div>
              <span className="panel-tag">By month</span>
            </div>

            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={monthly}
                  margin={{ top: 12, right: 12, left: 4, bottom: 4 }}
                >
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="month" tickLine={false} axisLine={false} />
                  <YAxis
                    tickFormatter={(value: number) =>
                      new Intl.NumberFormat('en', {
                        notation: 'compact',
                      }).format(value)
                    }
                    tickLine={false}
                    axisLine={false}
                    width={48}
                  />
                  <Tooltip
                    formatter={(value) => formatCurrency(Number(value))}
                  />
                  <Line
                    type="monotone"
                    dataKey="total_revenue"
                    name="Revenue"
                    stroke="#2b9b83"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </article>
        </section>

        <section className="panel customers-panel" id="customers">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">CUSTOMER PERFORMANCE</p>
              <h2>Top customers</h2>
            </div>
            <span className="panel-tag">Top 10 by revenue</span>
          </div>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Customer</th>
                  <th>Company</th>
                  <th>Orders</th>
                  <th className="number-cell">Total revenue</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer) => (
                  <tr key={customer.customer_id}>
                    <td>
                      <div className="customer-name">
                        <span className="avatar">
                          {customer.customer_name.charAt(0).toUpperCase()}
                        </span>
                        {customer.customer_name}
                      </div>
                    </td>
                    <td>{customer.company || '—'}</td>
                    <td>{customer.order_count}</td>
                    <td className="number-cell revenue-cell">
                      {formatCurrency(Number(customer.total_revenue))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

<AIChat />

        <footer className="page-footer">
          AI Operations Copilot <span>•</span> Powered by FastAPI and PostgreSQL
        </footer>
      </section>
    </main>
  )
}

export default App
 