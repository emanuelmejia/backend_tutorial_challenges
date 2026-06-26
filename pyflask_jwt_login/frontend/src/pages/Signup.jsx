import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        alert('Usuario creado con éxito');
        navigate('/login');
      } else {
        const data = await response.json();
        alert(data.msg);
      }
    } catch (error) {
      console.error('Error during signup:', error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card shadow-sm bg-dark text-white border-secondary">
            <div className="card-body p-4">
              <h2 className="text-center mb-4">Crear Cuenta</h2>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input 
                    type="email" 
                    className="form-control" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    required 
                  />
                </div>
                <div className="mb-4">
                  <label className="form-label">Password</label>
                  <input 
                    type="password" 
                    className="form-control" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required 
                  />
                </div>
                <button type="submit" className="btn btn-success w-100">
                  Sign Up
                </button>
              </form>
              <div className="text-center mt-3">
                <small>¿Ya tienes una cuenta? <Link to="/login">Log in</Link></small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;