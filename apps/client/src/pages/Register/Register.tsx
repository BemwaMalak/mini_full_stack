import React, { useState } from 'react';
import { useRegister } from '../../hooks/useRegister';
import Spinner from '../../components/Spinner/Spinner';
import styles from './Register.module.scss';
import { CSSTransition } from 'react-transition-group';
import './animations.scss';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

const Register = (): React.JSX.Element => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { register, error, loading } = useRegister();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await register({ username, email, password, role });
  };

  return (
    <div className={styles.registerContainer}>
      {loading && <Spinner loading={loading} />}
      <CSSTransition
        in={!loading}
        timeout={300}
        classNames="fade"
        unmountOnExit
      >
        <div className={styles.formWrapper}>
          <h2 className={styles.title}>Register</h2>
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.inputGroup}>
              <label className={styles.label} htmlFor="username">
                Username:
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className={styles.input}
              />
            </div>
            <div className={styles.inputGroup}>
              <label className={styles.label} htmlFor="email">
                Email:
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className={styles.input}
              />
            </div>
            <div className={styles.inputGroup}>
              <label className={styles.label} htmlFor="password">
                Password:
              </label>
              <div className={styles.passwordWrapper}>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className={styles.input}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className={styles.toggleButton}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
            </div>
            <div className={styles.inputGroup}>
              <label className={styles.label} htmlFor="role">
                Role:
              </label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                required
                className={styles.input}
              >
                <option value="" disabled>
                  Select role
                </option>
                <option value="USER">User</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>
            <button type="submit" disabled={loading} className={styles.button}>
              {loading ? 'Registering...' : 'Register'}
            </button>
            {error && <p className={styles.errorMessage}>{error}</p>}
          </form>
        </div>
      </CSSTransition>
    </div>
  );
};

export default Register;
