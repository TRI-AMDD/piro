import CreatableSelect from 'react-select/creatable';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';
import { Dispatch, SetStateAction } from 'react';
import { CSSObject } from '@emotion/react';

const customStyles = {
  control: (base: CSSObject) => ({
    ...base,
    borderColor: '#757575', // default border color
    '&:hover': {
      borderColor: '#212121',
      border: '1px solid #212121' // border color on hover
    },
    boxShadow: 'none'
  })
};

interface Props {
  placeholder?: string;
  setValues: Dispatch<SetStateAction<MultiValue<Optionselect>>>;
}

export default function MultiSelect(props: Props) {
  const { placeholder, setValues } = props;
  const emptyOptions: Optionselect[] = [];

  return (
    <div className={styles.Multi}>
      <CreatableSelect
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
