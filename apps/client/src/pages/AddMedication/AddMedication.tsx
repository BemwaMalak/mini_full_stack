import React, { useState } from 'react';
import NavigationBar from '../../components/NavigationBar/NavigationBar';
import { useAddMedication } from '../../hooks/useAddMedication';
import { CreateMedicationPayload } from '../../services/medicationService';
import Spinner from '../../components/Spinner/Spinner';
import styles from './AddMedication.module.scss';

const AddMedication: React.FC = () => {
  const { addMedication, loading, error } = useAddMedication();
  const [newMedication, setNewMedication] = useState<CreateMedicationPayload>({
    name: '',
    dosage: '',
    quantity: 0,
    instructions: '',
    image: null,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value, type, files } = e.target as HTMLInputElement;

    if (type === 'file') {
      setNewMedication((prev) => ({
        ...prev,
        [name]: files && files.length > 0 ? files[0] : null,
      }));
    } else {
      setNewMedication((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await addMedication(newMedication);
    setNewMedication({
      name: '',
      dosage: '',
      quantity: 0,
      instructions: '',
      image: null,
    });
  };

  return (
    <>
      <NavigationBar />
      <div className={styles.container}>
        <h1 className={styles.title}>Add New Medication</h1>
        {loading && <Spinner loading={loading} />}
        {error && <p className={styles.error}>{error}</p>}
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="name" className={styles.label}>
              Name:
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={newMedication.name}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Enter medication name"
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="dosage" className={styles.label}>
              Dosage:
            </label>
            <input
              type="text"
              id="dosage"
              name="dosage"
              value={newMedication.dosage}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="e.g., 500mg"
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="quantity" className={styles.label}>
              Quantity:
            </label>
            <input
              type="number"
              id="quantity"
              name="quantity"
              value={newMedication.quantity}
              onChange={handleChange}
              required
              min="1"
              className={styles.input}
              placeholder="Enter quantity"
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="instructions" className={styles.label}>
              Instructions:
            </label>
            <textarea
              id="instructions"
              name="instructions"
              value={newMedication.instructions}
              onChange={handleChange}
              required
              className={styles.textarea}
              placeholder="Enter instructions"
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="image" className={styles.label}>
              Image (optional):
            </label>
            <input
              type="file"
              id="image"
              name="image"
              accept="image/*"
              onChange={handleChange}
              className={styles.inputFile}
            />
          </div>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={loading}
          >
            {loading ? 'Adding...' : 'Add Medication'}
          </button>
        </form>
      </div>
    </>
  );
};

export default AddMedication;
