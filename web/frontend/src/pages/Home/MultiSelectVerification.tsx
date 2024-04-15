import CreatableSelect from 'react-select/creatable';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';
import { Dispatch, SetStateAction } from 'react';
import { CSSObject } from '@emotion/react';
import { elements } from './elements';
import { useState } from 'react';
const customStyles = {
  control: (base: CSSObject) => ({
    ...base,
    borderColor: '#757575',
    borderWidth: '1px',
    boxShadow: '0 0 0 1px white',
    '&:hover': {
      borderColor: '#212121',
      boxShadow: '0 0 0 1px black'
    }
  })
};

interface Props {
  placeholder?: string;
  setValues: Dispatch<SetStateAction<MultiValue<Optionselect>>>;
}
interface Option {
  value: string;
  label: string;
}
const options: Option[] = elements.map((element) => ({ value: element, label: element }));

export default function MultiSelectVerification(props: Props) {
  const [error, setError] = useState<string>('');
  const handleInputChange = (inputValue: string) => {
    if (!inputValue) {
      setError('');
      return;
    }

    if (!options.find((option) => option.value.toLowerCase() === inputValue.toLowerCase())) {
      setError('Not an element');
    } else {
      setError('');
    }
    return inputValue.charAt(0).toUpperCase() + inputValue.slice(1).toLowerCase();
  };
  const { placeholder, setValues } = props;
  const emptyOptions: Optionselect[] = [];
  const formatCreateLabel = (inputValue: string) => `Add element... ${inputValue}`;
  return (
    <div className={styles.Multi}>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <CreatableSelect
        id="additional-elements"
        isValidNewOption={(inputValue) => (options.find((option) => option.value === inputValue) ? true : false)}
        onInputChange={handleInputChange}
        formatCreateLabel={formatCreateLabel}
        styles={customStyles}
        placeholder={placeholder}
        isMulti
        onChange={(newValues) => setValues(newValues)}
        options={emptyOptions}
        className={styles.custumcreateselect}
      />
    </div>
  );
}
