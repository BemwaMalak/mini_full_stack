import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import Spinner from '../Spinner/Spinner';
import styles from './NavigationBar.module.scss';
import { useAuth } from '../../hooks/useAuth';
import { useLogout } from '../../hooks/useLogout';

const NavigationBar: React.FC = () => {
  const { isAuthenticated, user, loading, error } = useAuth();
  const { logout } = useLogout();

  useEffect(() => {
    if (error) {
      toast.error(error as string);
    }
  }, [error]);

  return (
    <>
      <Spinner loading={loading} />
      <nav className={styles.navbar}>
        <div className={styles.navContainer}>
          <Link to="/" className={styles.brand}>
            Pharmacy App
          </Link>
          <ul className={styles.navLinks}>
            {isAuthenticated ? (
              <>
                <li>
                  <span className={styles.greeting}>
                    Hello, {user?.username}!
                  </span>
                </li>
                <li>
                  <Link to="/home" className={styles.navLink}>
                    Home
                  </Link>
                </li>
                {user?.role !== 'ADMIN' && (
                  <li>
                    <Link to="/my-requests" className={styles.navLink}>
                      My Refill Requests
                    </Link>
                  </li>
                )}
                {user?.role === 'ADMIN' && (
                  <>
                    <li>
                      <Link to="/dashboard" className={styles.navLink}>
                        Dashboard
                      </Link>
                    </li>
                    <li>
                      <Link to="/register" className={styles.navLink}>
                        Register New User
                      </Link>
                    </li>
                    <li>
                      <Link to="/add-medication" className={styles.navLink}>
                        Add Medication
                      </Link>
                    </li>
                  </>
                )}
                <li>
                  <button onClick={logout} className={styles.navButton}>
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
              </>
            )}
          </ul>
        </div>
      </nav>
    </>
  );
};

export default NavigationBar;
