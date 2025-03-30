import { useState, ChangeEvent, FormEvent } from 'react';

type FormHandler<T> = {
  values: T;
  handleChange: (e: ChangeEvent<HTMLInputElement>) => void;
  handleSubmit: (onSubmit: (values: T) => void) => (e: FormEvent) => void;
  reset: (newValues?: Partial<T>) => void;
  setValues: (newValues: Partial<T>) => void;
};

/**
 * A custom hook for form handling
 * @param initialValues The initial values for the form
 * @returns Form state and handlers
 */
export const useForm = <T extends Record<string, any>>(initialValues: T): FormHandler<T> => {
  const [values, setValues] = useState<T>(initialValues);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    
    setValues(prev => ({
      ...prev,
      [name]: type === 'number' ? (value ? Number(value) : undefined) : value,
    }));
  };

  const handleSubmit = (onSubmit: (values: T) => void) => (e: FormEvent) => {
    e.preventDefault();
    onSubmit(values);
  };

  const reset = (newValues?: Partial<T>) => {
    setValues({ ...initialValues, ...newValues });
  };

  return {
    values,
    handleChange,
    handleSubmit,
    reset,
    setValues: (newValues: Partial<T>) => setValues(prev => ({ ...prev, ...newValues })),
  };
}; 