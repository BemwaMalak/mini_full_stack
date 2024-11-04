import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useRefillRequestAggregate } from '../../hooks/useRefillRequestAggregate';
import Spinner from '../Spinner/Spinner';
import styles from './RefillRequestAggregateChart.module.scss';
import { toast } from 'react-toastify';

const COLORS = [
  '#3498db',
  '#2ecc71',
  '#e74c3c',
  '#9b59b6',
  '#f39c12',
  '#d35400',
];

const RefillRequestAggregateChart: React.FC = () => {
  const { data, loading, error } = useRefillRequestAggregate();

  if (error) {
    toast.error(error); // Display error if there is one
  }

  return (
    <div className={styles.chartContainer}>
      <h2>Refill Requests per Medication</h2>
      {loading ? (
        <Spinner loading={loading} />
      ) : (
        <>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart
              data={data}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="refill_request_count" fill="#3498db" />
            </BarChart>
          </ResponsiveContainer>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={data}
                dataKey="refill_request_count"
                nameKey="name"
                outerRadius={120}
                fill="#3498db"
                label
              >
                {data.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
};

export default RefillRequestAggregateChart;
