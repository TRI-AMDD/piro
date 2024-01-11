import Select from 'react-select';
import styles from './Home.module.css';
import { Option } from './TypeProps';

interface Props {
  placeholder?: string;
  label: string;
  options: Option[];
  setValue(value: Option): void;
}

export default function SingleSelect(props: Props) {
  const { label, setValue, options } = props;

  const handleChange = (option?: Option | Option[] | null) => {
    if (option && !Array.isArray(option)) {
      setValue(option);
    }
  };

  return (
    <div className={styles.Multi}>
      <label className={styles.Label}>{label}</label>
      <Select defaultValue={options[0]} onChange={handleChange} options={options} />
    </div>
  );
}
