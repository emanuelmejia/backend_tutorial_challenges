import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Private = () => {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    
    if (!token) {
      navigate('/login');
    } else {
      setIsAuthenticated(true);
    }
  }, [navigate]);

  if (!isAuthenticated) return null;

  return (
    <div className="container mt-5">
      <div className="alert alert-success shadow-sm" role="alert">
        <h4 className="alert-heading">¡Bienvenid@ al dashboard de usuario!</h4>
        <p>
          Estás viendo esta página porque ingresaste exitosamente y tienes un token de JWT válido
        </p>
        <hr />
        <p className="mb-0">
          Desde aquí ya podemos hacer requests autenticados al backend agregando el token a tus headers de fetch para la API.
        </p>
      </div>
    </div>
  );
};

export default Private;