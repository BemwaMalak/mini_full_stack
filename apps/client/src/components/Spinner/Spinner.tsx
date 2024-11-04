import React from 'react';
import { ClipLoader } from 'react-spinners';
import styles from './Spinner.module.scss';

interface SpinnerProps {
  loading: boolean;
}

const Spinner: React.FC<SpinnerProps> = ({ loading }) => {
  return loading ? (
    <div className={styles.spinnerOverlay}>
      <ClipLoader color="#ffffff" loading={loading} size={50} />
    </div>
  ) : null;
};

export default Spinner;
