import { Select, Option } from '@material-tailwind/react';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';

interface Props {
  value: string;
  options: Optionselect[];
  setValue(value: Optionselect): void;
}

export default function SingleSelect(props: Props) {
  const { value, setValue, options } = props;

  const handleChange = (value: string | undefined) => {
    if (value) {
      const optionItem = options.find((option) => option.value === value);
      if (optionItem) {
        setValue(optionItem);
      }
    }
  };

  return (
    <Select className={styles.singleselect} placeholder="Additional element" value={value} onChange={handleChange}>
      {options.map((option) => (
        <Option key={option.value} value={option.value}>
          {option.label}
        </Option>
      ))}
    </Select>
  );
}
