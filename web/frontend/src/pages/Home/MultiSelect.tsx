import CreatableSelect from 'react-select/creatable';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';
import { Dispatch, SetStateAction } from 'react';

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
        styles={{
          control: (provided, state) => ({
            ...provided,
            boxShadow: state.isFocused ? 'none' : provided.boxShadow,
            borderColor: state.isFocused ? '#ccc' : provided.borderColor,
            '&:hover': {
              borderColor: state.isFocused ? '#212121' : provided.borderColor,
              border: state.isFocused ? '2px solid' : provided.borderColor
            }
          })
        }}
        placeholder={placeholder}
        isMulti
        onChange={(newValues) => setValues(newValues)}
        options={emptyOptions}
        className={styles.custumcreateselect}
      />
    </div>
  );
}
