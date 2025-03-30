import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './App.css'
import SearchPage from './pages/SearchPage'
import PropertiesPage from './pages/PropertiesPage'
import ScraperPage from './pages/ScraperPage'
import { Home, NotFound } from './components'

// Create a client
const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="app-container">
          <header className="app-header">
            <div className="header-content">
              <NavLink to="/" className="app-logo">
                <img src="/dark_theme_logo_inverted.png" alt="Scooby In The House" className="logo-image" />
              </NavLink>
              <nav className="app-nav">
                <NavLink to="/" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Home</NavLink>
                <NavLink to="/properties" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Properties</NavLink>
                <NavLink to="/scraper" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Scraper</NavLink>
              </nav>
            </div>
          </header>
          
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/properties" element={<PropertiesPage />} />
              <Route path="/scraper" element={<ScraperPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          
          <footer className="app-footer">
            <div className="footer-content">
              <div className="footer-logo">
                <img src="/dark_theme_logo_inverted.png" alt="Scooby In The House" className="footer-logo-image" />
              </div>
              <p className="footer-text">&copy; {new Date().getFullYear()} Scooby In The House. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
