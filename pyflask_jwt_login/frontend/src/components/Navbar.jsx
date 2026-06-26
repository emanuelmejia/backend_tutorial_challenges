import { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation(); 
  const [isOpen, setIsOpen] = useState(false); // Estado para el menú móvil

  const isAuthenticated = !!sessionStorage.getItem('token');

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    setIsOpen(false); // Cierra el menú al salir
    navigate('/login');
  };

  const closeMenu = () => setIsOpen(false); // Función para cerrar el menú al hacer clic en un link

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div className="container">
        <Link className="navbar-brand fw-bold" to={isAuthenticated ? "/private" : "/login"}>
          <i className={isAuthenticated ? "fa-solid fa-lock-open" : "fa-solid fa-lock"}></i>
        </Link>
        
        {/* Botón de hamburguesa para móviles */}
        <button 
          className="navbar-toggler" 
          type="button" 
          onClick={() => setIsOpen(!isOpen)}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        
        {/* Contenedor colapsable usando el estado de React */}
        <div className={`collapse navbar-collapse ${isOpen ? 'show' : ''}`}>
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {!isAuthenticated && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login" onClick={closeMenu}>Login</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/signup" onClick={closeMenu}>Signup</Link>
                </li>
              </>
            )}
            
            {isAuthenticated && (
              <li className="nav-item">
                <Link className="nav-link" to="/private" onClick={closeMenu}>Acceso Autorizado</Link>
              </li>
            )}
          </ul>

          {isAuthenticated && (
            <button className="btn btn-outline-danger" onClick={handleLogout}>
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;