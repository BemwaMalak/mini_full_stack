import React, { useState } from 'react';
import styles from './RefillRequestDialog.module.scss';
import { useAddRefillRequest } from '../../hooks/useAddRefillRequest';
import Spinner from '../Spinner/Spinner';

interface RefillRequestDialogProps {
  medicationId: number;
  onClose: () => void;
}

const RefillRequestDialog: React.FC<RefillRequestDialogProps> = ({
  medicationId,
  onClose,
}) => {
  const [quantity, setQuantity] = useState(1);
  const { addRefillRequest, loading } = useAddRefillRequest();

  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuantity(parseInt(e.target.value, 10));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await addRefillRequest(medicationId, quantity);
    onClose();
  };

  return (
    <div className={styles.dialogOverlay}>
      <div className={styles.dialogContent}>
        <h2>Request Refill</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Quantity:
            <input
              type="number"
              min="1"
              value={quantity}
              onChange={handleQuantityChange}
            />
          </label>
          <div className={styles.actions}>
            <button
              type="submit"
              className={styles.saveButton}
              disabled={loading}
            >
              {loading ? <Spinner loading={loading} /> : 'Request'}
            </button>
            <button
              type="button"
              onClick={onClose}
              className={styles.cancelButton}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RefillRequestDialog;
