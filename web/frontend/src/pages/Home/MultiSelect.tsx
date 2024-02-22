import CreatableSelect from 'react-select/creatable';
import { ControlProps, CSSObjectWithLabel, GroupBase } from 'react-select';
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
          control: (base: CSSObjectWithLabel, props: ControlProps<Optionselect, boolean, GroupBase<Optionselect>>) => ({
            ...base,
            boxShadow: props.isFocused ? 'none' : base.boxShadow,
            borderColor: props.isFocused ? '#ccc' : base.borderColor,
            '&:hover': {
              borderColor: props.isFocused ? '#212121' : base.borderColor,
              border: props.isFocused ? '2px solid' : base.borderColor
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
