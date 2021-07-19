import CreatableSelect from 'react-select/creatable';
import styles from './Home.module.css';

interface Props {
    placeholder: string;
    label: string;
    setValues(value: any): void;
}

export default function MultiSelect(props: Props) {
    const { label, placeholder, setValues } = props;

    return (
        <div className={styles.Multi}>
            <label className={styles.Label}>{label}</label>
            <CreatableSelect
                placeholder={placeholder}
                isMulti
                onChange={setValues}
                options={[]}
            />
        </div>
    );
}