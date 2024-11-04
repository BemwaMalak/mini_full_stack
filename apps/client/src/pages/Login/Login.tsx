import React, { useState } from 'react';
import { useLogin } from '../../hooks/useLogin';
import Spinner from '../../components/Spinner/Spinner';
import styles from './Login.module.scss';
import { CSSTransition } from 'react-transition-group';
import './animations.scss';

const Login = (): React.JSX.Element => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, error, loading } = useLogin();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login({ username, password });
  };

  return (
    <div className={styles.loginContainer}>
      {loading && <Spinner loading={loading} />}
      <CSSTransition
        in={!loading}
        timeout={300}
        classNames="fade"
        unmountOnExit
      >
        <div className={styles.formWrapper}>
          <h2 className={styles.title}>Login</h2>
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.inputGroup}>
              <label className={styles.label}>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className={styles.input}
              />
            </div>
            <div className={styles.inputGroup}>
              <label className={styles.label}>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={styles.input}
              />
            </div>
            <button type="submit" disabled={loading} className={styles.button}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
            {error && <p className={styles.errorMessage}>{error}</p>}
          </form>
        </div>
      </CSSTransition>
    </div>
  );
};

export default Login;
