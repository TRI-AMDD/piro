import { Select, Option } from '@material-tailwind/react';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';
import { useState } from 'react';
import useOnClickOutside from './outsideclick';

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
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const wrapperRef = useOnClickOutside(() => setIsOpen(false));
  const handleClick = () => {
    if (isOpen === true) {
      setIsOpen(false);
    }
    if (isOpen === false) {
      setIsOpen(true);
    }
  };
  return (
    <div className={styles.singleselect}>
      <div className={styles.singleselectmargin}>
        <Select
          placeholder="Additional element"
          value={value}
          onChange={handleChange}
          label="hi"
          ref={wrapperRef}
          className={`border ${isOpen ? 'border-2 border-dark-black' : ''}`}
          labelProps={{
            style: {
              visibility: 'hidden' // Hide the existing label
            }
          }}
          onClick={handleClick}
        >
          {options.map((option) => (
            <Option key={option.value} value={option.value} className={styles.fontforoption}>
              {option.label}
            </Option>
          ))}
        </Select>
      </div>
    </div>
  );
}
