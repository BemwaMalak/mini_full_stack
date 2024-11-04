import React, { useState } from 'react';
import {
  Medication,
  UpdateMedicationPayload,
} from '../../services/medicationService';
import styles from './EditMedicationDialog.module.scss';

interface EditMedicationDialogProps {
  medication: Medication;
  // eslint-disable-next-line no-unused-vars
  onSave: (id: number, data: UpdateMedicationPayload) => Promise<void>;
  onClose: () => void;
}

const EditMedicationDialog: React.FC<EditMedicationDialogProps> = ({
  medication,
  onSave,
  onClose,
}) => {
  const [formData, setFormData] = useState<UpdateMedicationPayload>({
    name: medication.name,
    dosage: medication.dosage,
    quantity: medication.quantity,
    instructions: medication.instructions,
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSave(medication.id, formData);
    onClose();
  };

  return (
    <div className={styles.dialogOverlay}>
      <div className={styles.dialogContent}>
        <h2>Edit Medication</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name || ''}
              onChange={handleInputChange}
            />
          </label>
          <label>
            Dosage:
            <input
              type="text"
              name="dosage"
              value={formData.dosage || ''}
              onChange={handleInputChange}
            />
          </label>
          <label>
            Quantity:
            <input
              type="number"
              name="quantity"
              value={formData.quantity || 0}
              onChange={handleInputChange}
            />
          </label>
          <label>
            Instructions:
            <textarea
              name="instructions"
              value={formData.instructions || ''}
              onChange={handleInputChange}
            />
          </label>
          <div className={styles.actions}>
            <button type="submit" className={styles.saveButton}>
              Save
            </button>
            <button
              type="button"
              onClick={onClose}
              className={styles.cancelButton}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditMedicationDialog;
