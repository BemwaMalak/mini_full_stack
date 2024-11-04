import React from 'react';
import RefillRequestAggregateChart from '../../components/RefillRequestAggregateChart/RefillRequestAggregateChart';
import styles from './Dashboard.module.scss';
import NavigationBar from '../../components/NavigationBar/NavigationBar';

const DashboardPage: React.FC = () => {
  return (
    <div className={styles.dashboardPage}>
      <NavigationBar />
      <h1>Admin Dashboard</h1>
      <RefillRequestAggregateChart />
    </div>
  );
};

export default DashboardPage;
