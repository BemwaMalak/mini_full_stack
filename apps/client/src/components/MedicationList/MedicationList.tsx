import React from 'react';
import { Medication } from '../../services/medicationService';
import MedicationItem from '../MedicationItem/MedicationItem';
import styles from './MedicationList.module.scss';

interface MedicationListProps {
  medications: Medication[];
}

const MedicationList: React.FC<MedicationListProps> = ({ medications }) => {
  if (medications.length === 0) {
    return <p className={styles.noMedications}>No medications found.</p>;
  }

  return (
    <div className={styles.medicationList}>
      {medications.map((medication) => (
        <MedicationItem key={medication.id} medication={medication} />
      ))}
    </div>
  );
};

export default MedicationList;
