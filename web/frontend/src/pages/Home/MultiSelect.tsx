import CreatableSelect from 'react-select/creatable';
import { ControlProps, CSSObjectWithLabel, GroupBase } from 'react-select';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';
import { Dispatch, SetStateAction } from 'react';

interface OptionType {
  label: string;
  value: string;
}

type CustomStyles = {
  control: (
    base: CSSObjectWithLabel,
    props: ControlProps<OptionType, boolean, GroupBase<OptionType>>
  ) => CSSObjectWithLabel;
};

const customStyles: CustomStyles = {
  control: (base) => ({
    ...base,
      "&:hover": {
        border: "1px solid #ff8b67",
        boxShadow: "0px 0px 6px #ff8b67"
      }
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