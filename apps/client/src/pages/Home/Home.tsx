import React from 'react';
import NavigationBar from '../../components/NavigationBar/NavigationBar';
import MedicationList from '../../components/MedicationList/MedicationList';
import { useFetchMedications } from '../../hooks/useFetchMedications';
import styles from './Home.module.scss';
import Spinner from '../../components/Spinner/Spinner';

const Home: React.FC = () => {
  const { medications, loading, error } = useFetchMedications();

  return (
    <>
      <NavigationBar />
      <div className={styles.homeContainer}>
        <h1 className={styles.title}>Current Medications</h1>
        {loading && <Spinner loading={loading} />}
        {error && <p className={styles.error}>{error}</p>}
        {!loading && !error && <MedicationList medications={medications} />}
      </div>
    </>
  );
};

export default Home;
