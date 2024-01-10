import CreatableSelect from 'react-select/creatable';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';

interface Props {
  placeholder?: string;
  label: string;
  setValues(value: MultiValue<string>): void;
}

export default function MultiSelect(props: Props) {
  const { label, placeholder, setValues } = props;

  const onChange = (option: MultiValue<string>) => {
    setValues(option);
  };

  return (
    <div className={styles.Multi}>
      <label className={styles.Label}>{label}</label>
      <CreatableSelect placeholder={placeholder} isMulti onChange={onChange} options={[]} />
    </div>
  );
}
