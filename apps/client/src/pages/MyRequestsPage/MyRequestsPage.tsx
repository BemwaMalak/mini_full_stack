import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import {
  fetchRefillRequests,
  RefillRequest,
} from '../../services/refillRequestsService';
import Spinner from '../../components/Spinner/Spinner';
import styles from './MyRequestsPage.module.scss';
import { RESPONSE_MESSAGES } from '../../constants/responseMessages';

const MyRequestsPage: React.FC = () => {
  const [requests, setRequests] = useState<RefillRequest[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadRequests = async () => {
      setLoading(true);
      try {
        const response = await fetchRefillRequests();
        if (response.ok) {
          const data = await response.json();
          setRequests(data.data);
          toast.success(RESPONSE_MESSAGES['S009']); // Refill requests loaded successfully
        } else {
          const errorData = await response.json();
          const errorCode = errorData.code || 'E000';
          toast.error(RESPONSE_MESSAGES[errorCode]);
        }
      } catch {
        toast.error(RESPONSE_MESSAGES['E000']);
      } finally {
        setLoading(false);
      }
    };

    loadRequests();
  }, []);

  return (
    <div className={styles.myRequestsPage}>
      <h1>My Refill Requests</h1>
      {loading ? (
        <Spinner loading={true} />
      ) : requests.length > 0 ? (
        <ul className={styles.requestList}>
          {requests.map((request) => (
            <li key={request.id} className={styles.requestItem}>
              <p>Medication: {request.medication.name}</p>
              <p>Quantity: {request.quantity}</p>
              <p>Status: {request.status}</p>
              <p>
                Requested At:{' '}
                {new Date(request.requested_at).toLocaleString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit',
                  hour12: true,
                })}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No refill requests found.</p>
      )}
    </div>
  );
};

export default MyRequestsPage;
