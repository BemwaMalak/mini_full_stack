import React, { useState } from 'react';
import { Medication } from '../../services/medicationService';
import styles from './MedicationItem.module.scss';
import { useAuth } from '../../hooks/useAuth';
import { useDeleteMedication } from '../../hooks/useDeleteMedication';
import { useEditMedication } from '../../hooks/useEditMedication';
import RefillRequestDialog from '../RefillRequestDialog/RefillRequestDialog';
import EditMedicationDialog from '../EditMedicationDialog/EditMedicationDialog';

interface MedicationItemProps {
  medication: Medication;
}

const MedicationItem: React.FC<MedicationItemProps> = ({ medication }) => {
  const { user } = useAuth();
  const { deleteMedication, loading: deleteLoading } = useDeleteMedication();
  const { editMedication, loading: editLoading } = useEditMedication();
  const [isRefillDialogOpen, setRefillDialogOpen] = useState(false);
  const [isEditDialogOpen, setEditDialogOpen] = useState(false);

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete ${medication.name}?`)) {
      await deleteMedication(medication.id);
    }
  };

  const handleEdit = () => {
    setEditDialogOpen(true);
  };

  const handleRequestRefill = () => {
    setRefillDialogOpen(true);
  };

  const handleCloseRefillDialog = () => {
    setRefillDialogOpen(false);
  };

  const handleCloseEditDialog = () => {
    setEditDialogOpen(false);
  };

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

      <div className={styles.actions}>
        {user?.role === 'ADMIN' && (
          <>
            <button
              onClick={handleEdit}
              disabled={editLoading}
              className={styles.editButton}
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              disabled={deleteLoading}
              className={styles.deleteButton}
            >
              Delete
            </button>
          </>
        )}
        <button onClick={handleRequestRefill} className={styles.refillButton}>
          Request Refill
        </button>
      </div>

      {isRefillDialogOpen && (
        <RefillRequestDialog
          medicationId={medication.id}
          onClose={handleCloseRefillDialog}
        />
      )}

      {isEditDialogOpen && (
        <EditMedicationDialog
          medication={medication}
          onSave={editMedication}
          onClose={handleCloseEditDialog}
        />
      )}
    </div>
  );
};

export default MedicationItem;
