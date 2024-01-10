import CreatableSelect from 'react-select/creatable';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';
import { Option } from './TypeProps';
import { Dispatch, SetStateAction } from 'react';

interface Props {
  placeholder?: string;
  label: string;
  setValues: Dispatch<SetStateAction<MultiValue<Option>>>;
}

export default function MultiSelect(props: Props) {
  const { label, placeholder, setValues } = props;
  const emptyOptions: Option[] = [];

  return (
    <div className={styles.Multi}>
      <label className={styles.Label}>{label}</label>
      <CreatableSelect
        placeholder={placeholder}
        isMulti
        onChange={(newValues) => setValues(newValues)}
        options={emptyOptions}
      />
    </div>
  );
}
