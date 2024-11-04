import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styles from './NavigationBar.module.scss';
import { useAuth } from '../../contexts/AuthContext';

const NavigationBar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.navContainer}>
        <Link to="/" className={styles.brand}>
          MedicationApp
        </Link>
        <ul className={styles.navLinks}>
          {isAuthenticated ? (
            <>
              <li>
                <Link to="/home" className={styles.navLink}>
                  Home
                </Link>
              </li>
              <li>
                <button onClick={handleLogout} className={styles.navButton}>
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/login" className={styles.navLink}>
                  Login
                </Link>
              </li>
              <li>
                <Link to="/register" className={styles.navLink}>
                  Register
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default NavigationBar;
