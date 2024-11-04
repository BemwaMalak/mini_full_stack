import React from 'react';
import { Medication } from '../../services/medicationService';
import styles from './MedicationItem.module.scss';

interface MedicationItemProps {
  medication: Medication;
}

const MedicationItem: React.FC<MedicationItemProps> = ({ medication }) => {
  return (
    <div className={styles.medicationItem}>
      {medication.image && (
        <img
          src={medication.image}
          alt={medication.name}
          className={styles.medicationImage}
        />
      )}
      <h3 className={styles.medicationName}>{medication.name}</h3>
      <p className={styles.medicationDosage}>Dosage: {medication.dosage}</p>
      <p className={styles.medicationQuantity}>
        Quantity: {medication.quantity}
      </p>
      <p className={styles.medicationInstructions}>
        Instructions: {medication.instructions}
      </p>
      <p className={styles.medicationAddedBy}>
        Added by: {medication.added_by}
      </p>
      <p className={styles.medicationDates}>
        Created at: {new Date(medication.created_at).toLocaleString()}
      </p>
      <p className={styles.medicationDates}>
        Updated at: {new Date(medication.updated_at).toLocaleString()}
      </p>
    </div>
  );
};

export default MedicationItem;
